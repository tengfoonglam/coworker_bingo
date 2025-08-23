import config as cfg
from progress.bar import Bar

from coworker_bingo import BingoSheetGenerator, InputFilesReader, SheetDrawer


def main() -> None:

    generic_facts = InputFilesReader.read_generic_facts(txt_file_path=cfg.GENERIC_FACTS_FILE_PATH)

    if generic_facts is None:
        print("Failed to load generic facts file. Exiting.")
        return

    print(f"Loaded {len(generic_facts)} generic facts.")

    specific_facts_read_result = InputFilesReader.read_participant_names_and_specific_facts(
        csv_file_path=cfg.SPECIFIC_FACTS_FILE_PATH, name_col=cfg.NAME_COL)

    if specific_facts_read_result is None:
        print("Failed to load participant names and specific facts. Exiting.")
        return

    participants, specific_facts = specific_facts_read_result

    print(f"Loaded {len(participants)} participant names")
    print(f"Detected that {len(specific_facts)} participants provided at least one specific fact.")

    participants_list_alphabetical = list(participants)
    participants_list_alphabetical.sort()

    total_number_sheets = len(participants) * cfg.NUMBER_PUZZLE_SETS
    progress_bar = Bar("Generating Bingo Sheets", max=total_number_sheets)

    for i in range(1, cfg.NUMBER_PUZZLE_SETS + 1):
        for participant in participants_list_alphabetical:
            bingo_sheet_config = BingoSheetGenerator.Config(sheet_size=cfg.SHEET_SIZE,
                                                            participant=participant,
                                                            participants=participants,
                                                            generic_facts=generic_facts,
                                                            specific_facts=specific_facts,
                                                            specific_fact_indexes=cfg.SPECIFIC_FACT_INDEXES)
            sheet = BingoSheetGenerator.generate(config=bingo_sheet_config)
            stem = f"bingo_sheet_{participant}_{cfg.SHEET_SIZE}x{cfg.SHEET_SIZE}_{i}"
            header = f"{stem} ---- Participant name: {bingo_sheet_config.participant}"
            SheetDrawer.draw_table(sheet=sheet,
                                   config=cfg.SHEET_DRAWER_CONFIG,
                                   export_path=cfg.OUTPUT_DATA_PATH / f"{stem}.{cfg.OUTPUT_EXTENSION}",
                                   header=header)
            progress_bar.next()

    print(f"\nCo-worker bingo sheet generation complete, output files can be found in {cfg.OUTPUT_DATA_PATH}")


if __name__ == "__main__":
    main()
