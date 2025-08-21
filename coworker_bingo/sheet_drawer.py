import df2img
import os
import pandas as pd
import sys

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


class SheetDrawer:
    @dataclass
    class Config:
        title_font: str = "Times New Roman"
        title_font_size: int = 16
        cell_font: str = "Times New Roman"
        cell_font_size: int = 14
        cell_height: int = 200
        fig_size: Tuple[int, int] = (1000, 2000)

    @staticmethod
    def draw_table(sheet: pd.DataFrame, config: Config, export_path: Path, header: str) -> None:

        # Disable prints because the drawing of the sheet has a lot of verbose
        sys.stdout = open(os.devnull, 'w')

        fig = df2img.plot_dataframe(sheet,
                                    print_index=False,
                                    tbl_header_visible=True,
                                    title=dict(
                                        font_color="black",
                                        font_family=config.title_font,
                                        font_size=config.title_font_size,
                                        text=header,
                                    ),
                                    tbl_header=dict(
                                        align="center",
                                        line_color="black",
                                    ),
                                    tbl_cells=dict(font_family=config.cell_font,
                                                   font_size=config.cell_font_size,
                                                   height=config.cell_height,
                                                   align="center",
                                                   line_color="black"),
                                    fig_size=config.fig_size)

        df2img.save_dataframe(fig=fig, filename=str(export_path))

        # Revert standard output back to normal
        sys.stdout = sys.__stdout__
