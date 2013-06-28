__author__ = 'ajb'

import os
from PIL import Image, ImageDraw, ImageFilter
from app import app

THUMBNAIL_DIR = os.path.join(app.config['STORAGE_LOCATION'],
                             "compare_images")


def create_comparison_image(comparison, comparison_id):

    im = Image.new("RGB", (comparison.max_cols, comparison.max_rows), "orange")
    # im = Image.new("RGB", ((comparison.max_cols * 2) + 1, (comparison.max_rows * 2) + 1), "orange")
    draw = ImageDraw.Draw(im)

    MATCH_COLOR = "green"
    DIFF_COLOR = "red"
    ONE_TABLE_ONLY_COLOR = "red"
    PADDING_COLOR = "yellow"

    for row_index in range(comparison.max_rows):
        for col_index in range(comparison.max_cols):
            if (row_index, col_index) in comparison.same_cells:
                draw.point((col_index, row_index), MATCH_COLOR)

            elif (row_index, col_index) in comparison.diff_cells:
                draw.point((col_index, row_index), DIFF_COLOR)

            elif (row_index, col_index) in comparison.expected_table_only_cells:
                draw.point((col_index, row_index), ONE_TABLE_ONLY_COLOR)

            elif (row_index, col_index) in comparison.actual_table_only_cells:
                draw.point((col_index, row_index), ONE_TABLE_ONLY_COLOR)

            elif (row_index, col_index) in comparison.neither_table_cell_coords:
                draw.point((col_index, row_index), PADDING_COLOR)

            else:
                raise Exception("Untreated cell: %s" % ((row_index, col_index)))

    del draw

    im.resize((400, 400), Image.BICUBIC)

    save_location = os.path.join(THUMBNAIL_DIR,
                                 "%s.png" % comparison_id)
    im.save(save_location, "PNG")