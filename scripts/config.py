from pathlib import Path
from coworker_bingo import SheetDrawer

# Uncomment below for 5x5 Bingo Sheets
# SHEET_SIZE = 5
# NUMBER_PUZZLE_SETS = 1
# SPECIFIC_FACT_INDEXES = {0, 4, 6, 8, 12, 16, 18, 20, 24}

# Uncomment below for 6x6 Bingo Sheets
SHEET_SIZE = 6
NUMBER_PUZZLE_SETS = 1
SPECIFIC_FACT_INDEXES = {0, 5, 7, 10, 14, 15, 20, 21, 25, 28, 30, 35}

# Input data location
INPUT_FOLDER_NAME = "input_files"
GIT_ROOT_DIRECTORY = Path(__file__).resolve().parent.parent
SPECIFIC_FACTS_FILE_PATH = GIT_ROOT_DIRECTORY / INPUT_FOLDER_NAME / "specific_facts.csv"
GENERIC_FACTS_FILE_PATH = GIT_ROOT_DIRECTORY / INPUT_FOLDER_NAME / "generic_facts.txt"

# Output data location
OUTPUT_DATA_PATH = GIT_ROOT_DIRECTORY / "generated_sheets"

# Specific facts csv info
NAME_COL = "Name"

# Output/Appearance options
OUTPUT_EXTENSION = "pdf"    # Can be pdf/png/jpg

SHEET_DRAWER_CONFIG = SheetDrawer.Config(
    title_font="Arial",
    title_font_size=18,
    cell_font="Arial",
    cell_font_size=14,
    cell_height=100,    # Increase accordingly if facts overflow out of cell
    fig_size=(750, 750)    # Increase accordingly if only a portion of the table is rendered in the drawn sheet
)

# Miscellaneous options
RANDOM_SEED = 1
