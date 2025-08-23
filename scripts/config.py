from pathlib import Path
from coworker_bingo import BingoSheetGenerator, SheetDrawer

# Sheet generation options
NUMBER_PUZZLE_SETS = 1  # Number of puzzles generated per person
RANDOM_SEED = 1

# Uncomment below for 5x5 Bingo Sheets
# BINGO_SHEET_CONFIG = BingoSheetGenerator.Config(
#     sheet_size=5,
#     specific_fact_indexes= {0, 4, 6, 8, 12, 16, 18, 20, 24},
#     random_seed=RANDOM_SEED)

# Uncomment below for 6x6 Bingo Sheets
BINGO_SHEET_CONFIG = BingoSheetGenerator.Config(
    sheet_size=6,
    specific_fact_indexes={0, 5, 7, 10, 14, 15, 20, 21, 25, 28, 30, 35},
    random_seed=RANDOM_SEED,
)

# Input data location
INPUT_FOLDER_NAME = "input_files"
GIT_ROOT_DIRECTORY = Path(__file__).resolve().parent.parent
INPUT_FOLDER = GIT_ROOT_DIRECTORY / INPUT_FOLDER_NAME
SPECIFIC_FACTS_FILE_PATH = INPUT_FOLDER / "specific_facts.csv"
GENERIC_FACTS_FILE_PATH = INPUT_FOLDER / "generic_facts.txt"

# Output data location
OUTPUT_FOLDER_NAME = "generated_sheets"
OUTPUT_DATA_PATH = GIT_ROOT_DIRECTORY / OUTPUT_FOLDER_NAME

# Specific facts csv info
NAME_COL = "Name"

# Output/Appearance options
OUTPUT_EXTENSION = "pdf"  # Can be pdf/png/jpg

SHEET_DRAWER_CONFIG = SheetDrawer.Config(
    title_font="Arial",
    title_font_size=18,
    cell_font="Arial",
    cell_font_size=14,
    cell_height=100,  # Increase accordingly if facts overflow out of cell
    fig_size=(750, 750),
    # Increase accordingly if only a portion of the table is rendered
    # in the drawn sheet
)

# Miscellaneous options
