import df2img
import os
import logging
import pandas as pd
import sys

from dataclasses import dataclass
from pathlib import Path
from typing import Set, Tuple


class SheetDrawer:
    """
    Methods and dataclasses to render a bingo sheet into a printable file
    format
    """

    SUPPORTED_EXPORT_FORMATS: Set[str] = {".png", ".pdf", "jpg"}

    @dataclass
    class Config:
        """
        Configuration of how the bingo sheet is rendered

        Attributes:
            title_font: Font of the title
            title_font_size: Font size of the title
            cell_font: Font of the facts in each cell
            cell_font_size: Font size of the facts in each cell
            cell_height: Height of each cell. Increase accordingly if facts
            overflow out of cell
            fig_size: Size of the entire bingo sheet. Increase accordingly if
            only a portion of the table is rendered in the drawn sheet
        """

        title_font: str = "Times New Roman"
        title_font_size: int = 16
        cell_font: str = "Times New Roman"
        cell_font_size: int = 14
        cell_height: int = 200
        fig_size: Tuple[int, int] = (1000, 2000)

    @staticmethod
    def draw_table(
        sheet: pd.DataFrame, config: Config, export_path: Path, title: str
    ) -> bool:
        """
        Write a bingo sheet to a file

        Arguments:
            sheet: Bingo sheet
            config: Drawer config
            export_path: Location to save file to (end of the path needs to
            end with and extension specified in class variable
            SUPPORTED_EXPORT_FORMATS)
            title: Title that will be shown above the table

        Returns:
            Boolean on whether the bingo sheet has been saved successfully
            to the specified export_path
        """

        if export_path.suffix not in SheetDrawer.SUPPORTED_EXPORT_FORMATS:
            logging.error(
                f"Failed to draw bingo sheet at {export_path}. "
                f"Export path has invalid extension {export_path.suffix}. "
                f"Supported extentions: {SheetDrawer.SUPPORTED_EXPORT_FORMATS}"
            )
            return False

        # Disable prints because the drawing of the sheet has a lot of verbose
        sys.stdout = open(os.devnull, "w")

        fig = df2img.plot_dataframe(
            sheet,
            print_index=False,
            tbl_header_visible=True,
            title=dict(
                font_color="black",
                font_family=config.title_font,
                font_size=config.title_font_size,
                text=title,
            ),
            tbl_header=dict(
                align="center",
                line_color="black",
            ),
            tbl_cells=dict(
                font_family=config.cell_font,
                font_size=config.cell_font_size,
                height=config.cell_height,
                align="center",
                line_color="black",
            ),
            fig_size=config.fig_size,
        )

        df2img.save_dataframe(fig=fig, filename=str(export_path))

        # Revert standard output back to normal
        sys.stdout = sys.__stdout__

        return True
