import logging
import random
import pandas as pd

from copy import deepcopy
from dataclasses import dataclass
from typing import Dict, List, Set


class BingoSheetGenerator:
    """
    Methods and dataclasses to generate a bingo sheet as a Pandas Dataframe
    """

    @dataclass
    class Config:
        """
        Configuration for a bingo sheet

        Definition for indexes:
        Index from 0 to (total number of cells - 1) in row major order
        For example, a 3x3 bingo sheet would have the following indexes

        +---+---+---+
        | 0 | 1 | 2 |
        +---+---+---+
        | 3 | 4 | 5 |
        +---+---+---+
        | 6 | 7 | 8 |
        +---+---+---+

        Attributes:
            sheet_size: Number of cells in a rol/col the bingo sheet
            specific_fact_indexes: Indexes where a specific fact will be
            inserted into the sheet. Other cells will be filled with generic
            facts
            random_seed: Random seed to initialise the pseudorandom number
            generator
        """

        sheet_size: int
        specific_fact_indexes: Set[int]
        random_seed: int

        @property
        def num_cells(self) -> int:
            """Total number of cells in the bingo sheet

            Returns:
                Aforementioned quantity
            """
            return self.sheet_size**2

        def is_valid(self) -> bool:
            """Boolean whether the config is valid or not

            Returns:
                Aforementioned quantity
            """
            specific_fact_indexes_valid = all(
                [idx < self.num_cells for idx in self.specific_fact_indexes]
            )
            if not specific_fact_indexes_valid:
                logging.error(
                    "Invalid specific fact indexes - Values should be >= 0 "
                    f"and < total number of bingo cells ({self.num_cells})."
                )
            return specific_fact_indexes_valid

    @dataclass
    class Data:
        """_summary_"""

        generic_facts: List[str]
        specific_facts: Dict[str, list[str]]

    @staticmethod
    def check_config_and_data(config: Config, data: Data) -> bool:
        if not config.is_valid():
            return False

        # Number of specific facts check
        num_specific_fact_cells = len(config.specific_fact_indexes)
        num_participants_with_specific_facts = len(data.specific_facts)
        if num_participants_with_specific_facts < num_specific_fact_cells:
            logging.error(
                "Number of participants that provided specific facts "
                f"({num_participants_with_specific_facts}) "
                "is less than the required number of specific facts per "
                f"bingo sheet ({num_specific_fact_cells})."
            )
            return False

        # Number of generic facts check
        num_generic_facts = len(data.generic_facts)
        num_generic_fact_cells = config.num_cells - num_specific_fact_cells
        if num_generic_facts < num_generic_fact_cells:
            logging.error(
                f"Number of generic facts provided ({num_generic_facts}) "
                "is less than the required number of generic facts per "
                f"bingo sheet ({num_generic_fact_cells})."
            )
            return False

        return True

    @staticmethod
    def generate(
        participant_name: str, config: Config, data: Data
    ) -> pd.DataFrame:
        num_cells = config.num_cells
        num_specific_fact_cells = len(config.specific_fact_indexes)
        num_generic_fact_cells = num_cells - num_specific_fact_cells

        random.seed(config.random_seed)

        # Pick generic facts
        generic_fact_indexes = (
            set([i for i in range(num_cells)]) - config.specific_fact_indexes
        )
        assert num_generic_fact_cells == len(generic_fact_indexes)
        generic_facts = random.sample(
            data.generic_facts, num_generic_fact_cells
        )
        random.shuffle(generic_facts)

        # Pick specific facts (excluding the participant's own facts)
        specific_facts_no_participant = deepcopy(data.specific_facts)
        if participant_name in specific_facts_no_participant:
            del specific_facts_no_participant[participant_name]
        specific_names = list(specific_facts_no_participant.keys())
        sampled_specific_names = random.sample(
            specific_names, num_specific_fact_cells
        )
        random.shuffle(sampled_specific_names)
        sampled_facts = [
            random.sample(specific_facts_no_participant[name], 1)[0]
            for name in sampled_specific_names
        ]

        # Create sheet
        sheet = ["" for _ in range(num_cells)]
        for idx, gen_fact in zip(generic_fact_indexes, generic_facts):
            sheet[idx] = gen_fact
        for idx, gen_fact in zip(config.specific_fact_indexes, sampled_facts):
            sheet[idx] = gen_fact
        assert not any([len(fact) == 0 for fact in sheet])

        sheet_size = config.sheet_size
        data = [
            sheet[i * sheet_size : i * sheet_size + sheet_size]
            for i in range(sheet_size)
        ]
        columns = [str(i) for i in range(sheet_size)]

        return pd.DataFrame(data=data, columns=columns)
