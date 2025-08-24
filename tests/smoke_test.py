from pathlib import Path
from typing import List

from coworker_bingo import InputFilesReader

from coworker_bingo.scripts import config as cfg
from coworker_bingo.scripts.generate_sheets import main


def get_non_gitkeep_files(folder: Path) -> List[Path]:
    """Get all files in a folder except .gitkeep

    Arguments:
        folder -- Folder to search

    Returns:
        List of Paths of files in a folder except .gitkeep
    """
    GIT_KEEP_FILENAME = ".gitkeep"
    return [
        item
        for item in folder.iterdir()
        if (item.name != GIT_KEEP_FILENAME and item.is_file())
    ]


def clear_output_folder(folder: Path) -> None:
    """Remove all files in a folder except .gitkeep

    Arguments:
        folder -- Folder to clear
    """
    files_to_remove = get_non_gitkeep_files(folder=folder)
    for item in files_to_remove:
        item.unlink()


def test_generate_sheets_script() -> None:
    """
    Simple smoke test to ensure that the main functionality of generating
    coworker bingo sheets is working

    Runs the main() function of the generate_sheet script and does some simple
    checks to ensure that the bingo sheets are generated.

    Note 1: This test will clear the generated_sheets folder
    Note 2: If the config.py was edited for personal use this might break the
            integration test
    """

    output_folder = cfg.OUTPUT_DATA_PATH

    # Remove all generated files except .gitkeep
    clear_output_folder(folder=output_folder)

    # Call main generate sheet function
    assert main() == 0

    # Load participant names
    specific_facts_read_result = (
        InputFilesReader.read_participant_names_and_specific_facts(
            csv_file_path=cfg.SPECIFIC_FACTS_FILE_PATH, name_col=cfg.NAME_COL
        )
    )
    assert specific_facts_read_result is not None
    participants, _ = specific_facts_read_result

    # Ensure expected number of files are generated
    generated_filenames = [
        f.name for f in get_non_gitkeep_files(folder=output_folder)
    ]

    expected_num_files = len(participants) * cfg.NUMBER_PUZZLE_SETS
    assert len(generated_filenames) == expected_num_files

    for participant in participants:
        number_participant_files = sum(
            1 for filename in generated_filenames if participant in filename
        )
        assert number_participant_files == cfg.NUMBER_PUZZLE_SETS

    # Cleanup
    clear_output_folder(folder=output_folder)
