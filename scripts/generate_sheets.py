import config as cfg
import pandas as pd

from coworker_bingo.bingo_sheet_generator import BingoSheetGenerator


def main() -> None:

    participants_list = []
    try:
        with open(cfg.PARTICIPANT_NAMES_FILE_PATH, 'r') as file:
            for line in file:
                participants_list.append(line.strip())
    except FileNotFoundError:
        print(f"Participant names file '{cfg.PARTICIPANT_NAMES_FILE_PATH}' was not found. Exiting")
        return

    participants = set(participants_list)

    if len(participants) != len(participants_list):
        print("Participant names are not unique. Exiting")
        return

    print(f"Loaded {len(participants)} participant names")

    generic_facts = []
    try:
        with open(cfg.GENERIC_FACTS_FILE_PATH, 'r') as file:
            for line in file:
                generic_facts.append(line.strip())
    except FileNotFoundError:
        print(f"Generic facts file '{cfg.GENERIC_FACTS_FILE_PATH}' was not found. Exiting")
        return

    print(f"Loaded {len(generic_facts)} generic facts")

    df = pd.read_csv(cfg.SPECIFIC_FACTS_FILE_PATH)

    specific_facts = dict()
    for _, row in df.iterrows():
        row_dict = row.to_dict()
        if cfg.NAME_COL not in row_dict:
            continue
        name = row_dict[cfg.NAME_COL]
        if name not in participants:
            continue
        specific_facts[name] = [val for key, val in row_dict.items() if key != cfg.NAME_COL and not pd.isnull(val)]

    print(f"Loaded {len(specific_facts)} sets of specific facts")

    for i in range(1, cfg.NUMBER_PUZZLE_SETS + 1):
        for participant in participants_list:
            config = BingoSheetGenerator.Config(sheet_size=cfg.SHEET_SIZE,
                                                participant=participant,
                                                participants=participants,
                                                generic_facts=generic_facts,
                                                specific_facts=specific_facts,
                                                specific_fact_indexes=cfg.SPECIFIC_FACT_INDEXES)
            sheet = BingoSheetGenerator.generate(config=config)
            label = f"bingo_sheet_{participant}_{cfg.SHEET_SIZE}x{cfg.SHEET_SIZE}_{i}"
            BingoSheetGenerator.draw_table(sheet=sheet,
                                           config=config,
                                           export_path=cfg.OUTPUT_DATA_PATH / f"{label}.png",
                                           header=label)


if __name__ == "__main__":
    main()
