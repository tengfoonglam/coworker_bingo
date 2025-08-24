import logging
import sys

from coworker_bingo import BingoSheetGenerator, InputFilesReader, SheetDrawer
from progress.bar import Bar

import coworker_bingo.scripts.config as cfg


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")

    generic_facts = InputFilesReader.read_generic_facts(
        txt_file_path=cfg.GENERIC_FACTS_FILE_PATH
    )

    if generic_facts is None:
        logging.error("Failed to load generic facts file. Exiting.")
        return 1

    logging.info(f"Loaded {len(generic_facts)} generic facts.")

    specific_facts_read_result = (
        InputFilesReader.read_participant_names_and_specific_facts(
            csv_file_path=cfg.SPECIFIC_FACTS_FILE_PATH, name_col=cfg.NAME_COL
        )
    )

    if specific_facts_read_result is None:
        logging.error(
            "Failed to load participant names and specific facts. Exiting."
        )
        return 1

    participants, specific_facts = specific_facts_read_result

    logging.info(f"Loaded {len(participants)} participant names")
    logging.info(
        f"Detected that {len(specific_facts)} participants provided at least "
        "one specific fact."
    )

    bingo_generator_data = BingoSheetGenerator.Data(
        generic_facts=generic_facts, specific_facts=specific_facts
    )

    if not BingoSheetGenerator.check_config_and_data(
        config=cfg.BINGO_SHEET_CONFIG, data=bingo_generator_data
    ):
        logging.error("Bingo config and data is invalid. Exiting.")
        return 1

    participants_list_alphabetical = list(participants)
    participants_list_alphabetical.sort()

    total_number_sheets = len(participants) * cfg.NUMBER_PUZZLE_SETS
    progress_bar = Bar("Generating Bingo Sheets", max=total_number_sheets)

    logging.info(
        f"Generating bingo sheets for {len(participants)} participants "
        f"({cfg.NUMBER_PUZZLE_SETS} each)"
    )
    logging.info(f"Total sheets: {total_number_sheets}")

    for i in range(1, cfg.NUMBER_PUZZLE_SETS + 1):
        for participant_name in participants_list_alphabetical:
            sheet = BingoSheetGenerator.generate(
                participant_name=participant_name,
                config=cfg.BINGO_SHEET_CONFIG,
                data=bingo_generator_data,
            )
            sheet_size = cfg.BINGO_SHEET_CONFIG.sheet_size
            stem = (
                f"bingo_sheet_{participant_name}_{sheet_size}x{sheet_size}_{i}"
            )
            export_path = (
                cfg.OUTPUT_DATA_PATH / f"{stem}.{cfg.OUTPUT_EXTENSION}"
            )
            title = f"{stem} ---- Participant name: {participant_name}"
            if not SheetDrawer.draw_table(
                sheet=sheet,
                config=cfg.SHEET_DRAWER_CONFIG,
                export_path=export_path,
                title=title,
            ):
                logging.error(
                    f"Failed to save bingo sheet to {export_path}. Exiting."
                )
                return 1

            progress_bar.next()

    print("")  # Flush new text to next line after printing progress bar
    logging.info(
        "Co-worker bingo sheet generation complete, "
        f"output files can be found in {cfg.OUTPUT_DATA_PATH}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
