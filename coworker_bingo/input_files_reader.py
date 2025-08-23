import logging
import pandas as pd

from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set


class InputFilesReader:
    """
    Methods to read the data required to generate the co-worker bingo sheets
    """

    @staticmethod
    def read_generic_facts(txt_file_path: Path) -> Optional[List[str]]:
        """
        Read the generic facts .txt file

        Arguments:
            txt_file_path -- Path to the generic facts text file

        Returns:
            List of generic facts. None if there was an error reading the file
        """
        generic_facts = None
        try:
            with open(txt_file_path, "r") as file:
                generic_facts = [line.strip() for line in file]
        except FileNotFoundError:
            logging.error(
                f"Generic facts file '{txt_file_path}' was not found."
            )

        return generic_facts

    @staticmethod
    def read_participant_names_and_specific_facts(
        csv_file_path: Path, name_col: str
    ) -> Optional[Tuple[Set[str], Dict[str, List[str]]]]:
        """
        Read the specific facts csv file

        Arguments:
            csv_file_path -- Path to the specific facts csv file
            name_col -- Label of the column in the csv table that indicates the
            name of the participants

        Returns:
            A tuple where the first element is a unique set of participant
            names. The second element a dictionary where the key is the
            participant name and the value is a list of facts that belong to
            him/her. None if there was an error reading the file
        """

        df = None

        try:
            df = pd.read_csv(csv_file_path)
        except FileNotFoundError:
            logging.error(
                f"Specific facts file '{csv_file_path}' was not found."
            )

        if df is None:
            return None

        participants_list = df[name_col].to_list()
        participants = set(participants_list)

        if len(participants_list) == 0:
            logging.error("No participants found.")
            return None

        if len(participants) != len(participants_list):
            logging.error(
                "Participant names are not unique. Ensure that there are no "
                "duplicate names."
            )
            return None

        specific_facts = dict()
        for _, row in df.iterrows():
            row_dict = row.to_dict()
            if name_col not in row_dict:
                continue
            name = row_dict[name_col]
            if name not in participants:
                continue
            single_participant_personal_fact = [
                val
                for col, val in row_dict.items()
                if col != name_col and not pd.isnull(val)
            ]
            if len(single_participant_personal_fact) > 0:
                specific_facts[name] = single_participant_personal_fact

        return (participants, specific_facts)
