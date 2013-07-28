__author__ = 'ajb'

import os, StringIO

from PIL import Image, ImageDraw
# try:
#     from PIL import Image, ImageDraw
# except ImportError, e:
#     print "PIL module isn't available - thumbnail/image results won't be supported"


def create_comparison_image(comparison):

    im = Image.new("RGB", (comparison.max_cols, comparison.max_rows), "orange")
    draw = ImageDraw.Draw(im)

    MATCH1_COLOR = "#33FF99"
    MATCH2_COLOR = "#2EE68A"
    DIFF1_COLOR = "red"
    DIFF2_COLOR = "#E60000"
    ONE_TABLE_ONLY_COLOR = "orange"
    PADDING_COLOR = "yellow"

    for row_index in range(comparison.max_rows):
        for col_index in range(comparison.max_cols):
            if (row_index, col_index) in comparison.same_cells:
                if (row_index + col_index) % 2 == 0:
                    draw.point((col_index, row_index), MATCH1_COLOR)
                else:
                    draw.point((col_index, row_index), MATCH2_COLOR)

            elif (row_index, col_index) in comparison.diff_cells:
                if (row_index + col_index) % 2 == 0:
                    draw.point((col_index, row_index), DIFF1_COLOR)
                else:
                    draw.point((col_index, row_index), DIFF2_COLOR)

            elif (row_index, col_index) in comparison.expected_table_only_cells:
                draw.point((col_index, row_index), ONE_TABLE_ONLY_COLOR)

            elif (row_index, col_index) in comparison.actual_table_only_cells:
                draw.point((col_index, row_index), ONE_TABLE_ONLY_COLOR)

            elif (row_index, col_index) in comparison.neither_table_cell_coords:
                draw.point((col_index, row_index), PADDING_COLOR)

            else:
                raise Exception("Untreated cell: %s" % ((row_index, col_index)))

    del draw

    if comparison.max_cols > comparison.max_rows:
        width = 600
        height = (width / comparison.max_cols) * comparison.max_rows
    else:
        height = 550
        width = (height / comparison.max_rows) * comparison.max_cols
    im = im.resize((width, height))

    output = StringIO.StringIO()
    im.save(output, format= 'PNG')
    contents = output.getvalue()
    output.close()

    return contents
