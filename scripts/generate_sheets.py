import config as cfg
import pandas as pd

from coworker_bingo import BingoSheetGenerator, SheetDrawer


def main() -> None:

    generic_facts = []
    try:
        with open(cfg.GENERIC_FACTS_FILE_PATH, 'r') as file:
            for line in file:
                generic_facts.append(line.strip())
    except FileNotFoundError:
        print(f"Generic facts file '{cfg.GENERIC_FACTS_FILE_PATH}' was not found. Exiting.")
        return

    print(f"Loaded {len(generic_facts)} generic facts.")

    try:
        df = pd.read_csv(cfg.SPECIFIC_FACTS_FILE_PATH)
    except FileNotFoundError:
        print(f"Specific facts file '{cfg.SPECIFIC_FACTS_FILE_PATH}' was not found. Exiting.")
        return

    participants_list = df[cfg.NAME_COL].to_list()
    participants = set(participants_list)

    if len(participants_list) == 0:
        print("No participants found. Exiting.")

    if len(participants) != len(participants_list):
        print("Participant names are not unique. Exiting.")
        return

    print(f"Loaded {len(participants)} participant names")

    specific_facts = dict()
    for _, row in df.iterrows():
        row_dict = row.to_dict()
        if cfg.NAME_COL not in row_dict:
            continue
        name = row_dict[cfg.NAME_COL]
        if name not in participants:
            continue
        single_participant_personal_fact = [
            val for key, val in row_dict.items() if key != cfg.NAME_COL and not pd.isnull(val)
        ]
        if len(single_participant_personal_fact) > 0:
            specific_facts[name] = single_participant_personal_fact

    print(f"{len(specific_facts)} participants provided at least one specific facts.")

    for i in range(1, cfg.NUMBER_PUZZLE_SETS + 1):
        for participant in participants_list:
            bingo_sheet_config = BingoSheetGenerator.Config(sheet_size=cfg.SHEET_SIZE,
                                                            participant=participant,
                                                            participants=participants,
                                                            generic_facts=generic_facts,
                                                            specific_facts=specific_facts,
                                                            specific_fact_indexes=cfg.SPECIFIC_FACT_INDEXES)
            sheet = BingoSheetGenerator.generate(config=bingo_sheet_config)
            label = f"bingo_sheet_{participant}_{cfg.SHEET_SIZE}x{cfg.SHEET_SIZE}_{i}"
            header = f"{label} ---- Participant name: {bingo_sheet_config.participant}"
            SheetDrawer.draw_table(sheet=sheet,
                                   config=cfg.SHEET_DRAWER_CONFIG,
                                   export_path=cfg.OUTPUT_DATA_PATH / f"{label}.{cfg.OUTPUT_EXTENSION}",
                                   header=header)


if __name__ == "__main__":
    main()
