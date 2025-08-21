import random
import pandas as pd

from copy import deepcopy
from dataclasses import dataclass
from typing import Dict, List, Set


class BingoSheetGenerator:
    @dataclass
    class Config:
        sheet_size: int
        participant: str
        participants: Set[str]
        generic_facts: List[str]
        specific_facts: Dict[str, list[str]]
        specific_fact_indexes: Set[int]

    @staticmethod
    def generate(config: Config) -> pd.DataFrame:
        num_grids = config.sheet_size**2

        num_specific_fact_grids = len(config.specific_fact_indexes)
        num_generic_fact_grids = num_grids - num_specific_fact_grids

        # Pick generic facts
        generic_fact_indexes = set([i for i in range(num_grids)]) - config.specific_fact_indexes
        assert (num_generic_fact_grids == len(generic_fact_indexes))
        generic_facts = random.sample(config.generic_facts, num_generic_fact_grids)
        random.shuffle(generic_facts)

        # Pick specific facts
        specific_facts_no_pariticipant = deepcopy(config.specific_facts)
        if config.participant in specific_facts_no_pariticipant:
            del specific_facts_no_pariticipant[config.participant]
        specific_names = list(specific_facts_no_pariticipant.keys())
        sampled_specific_names = random.sample(specific_names, num_specific_fact_grids)
        random.shuffle(sampled_specific_names)
        sampled_facts = [random.sample(specific_facts_no_pariticipant[name], 1)[0] for name in sampled_specific_names]

        # Create sheet
        sheet = ["" for _ in range(num_grids)]
        for idx, gen_fact in zip(generic_fact_indexes, generic_facts):
            sheet[idx] = gen_fact
        for idx, gen_fact in zip(config.specific_fact_indexes, sampled_facts):
            sheet[idx] = gen_fact
        assert (not any([len(fact) == 0 for fact in sheet]))

        sheet_size = config.sheet_size
        data = [sheet[i * sheet_size:i * sheet_size + sheet_size] for i in range(sheet_size)]
        columns = [str(i) for i in range(sheet_size)]

        return pd.DataFrame(data=data, columns=columns)
