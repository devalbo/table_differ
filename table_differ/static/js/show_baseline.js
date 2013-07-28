
var $container = $("#dataTable");
var $console = $("#example1console");
//var $parent = $container.parent();
var comparison_classes = null;
var comparison_data = null;

var compareRenderer = function (instance, td, row, col, prop, value, cellProperties) {
    if (comparison_classes != null) {

        try {
            td.className = comparison_classes[row][col];
            td.innerHTML = comparison_data[row][col];
        } catch(e) {
            td.className = "compare-literal";
        }
    }

};

function get_css_class_for_comparison_type(comparison_type) {
    switch (comparison_type) {
        case "0":
            return "compare-literal";
            break;
        case "1":
            return "compare-regex";
            break;
        case "2":
            return "compare-ignore";
            break;
        default:
            alert("Oops - invalid comparison type: " + comparison_type);
    }

}

function get_default_class() {
    var selected = $("#comparisonTypes input[type='radio']:checked");
    var selectedValue = selected.val();
    return get_css_class_for_comparison_type(selectedValue);
}

$container.handsontable({
    startRows: 8,
    startCols: 6,
    rowHeaders: true,
    colHeaders: true,
    contextMenu: {
        callback: function (key, options) {
          var updateAction = null;
          if (key === 'ignore') {
            setTimeout(function () {
              //timeout is used to make sure the menu collapsed before alert is shown
              var selected = handsontable.getSelected();
              updateAction = {update_type: "ignore_cells_in_region",
                              update_args: {
                                  region: selected
                              } };
              postUpdateAction(updateAction);
            }, 100);
          }
        },
        items: {
            "ignore": {name: 'Ignore Differences'},
            "hsep1": "---------",
            "row_above": {},
            "row_below": {},
            "remove_row": {},
            "add_row": {},
            "hsep2": "---------",
            "col_left": {},
            "col_right": {},
            "remove_col": {},
        },
    },
    afterCreateRow: function(index) {
        if (comparison_classes != null) {
            var new_classes_row = [];
            for (var i = 0; i <= handsontable.countCols() - 1; i++) {
               new_classes_row.push(get_default_class());
            }
            comparison_classes.splice(index, 0, new_classes_row);
        }
    },
    afterRemoveRow: function(index, num_rows) {
        if (comparison_classes != null) {
            comparison_classes.splice(index, num_rows);
        }
    },
    afterCreateCol: function(index) {
        if (comparison_classes != null) {
            var new_classes_row = [];
            for (var i = 0; i <= handsontable.countRows() - 1; i++) {
                comparison_classes[i].splice(index, 0, get_default_class());
            }
        }
    },
    afterRemoveCol: function(index, num_cols) {
        if (comparison_classes != null) {
            var new_classes_row = [];
            for (var i = 0; i <= handsontable.countRows() - 1; i++) {
                comparison_classes[i].splice(index, num_cols);
            }
        }

    },
    cells: function (row, col, prop) {
        this.renderer = compareRenderer; //uses function directly
    },
});

var handsontable = $container.data('handsontable');


$(document).ready( function() {
	updateBaselineContents();
});

$('#baseline-id').change( function() {
	updateBaselineContents();
});

function updateBaselineContents() {

	$.ajax({
		url: "/baselines/" + baseline_id + "/data",
	}).done(function(res, textStatus) {
		if (res.data) {
            comparison_data = res.data;
            comparison_classes = res.comparison_classes;
            handsontable.loadData(res.data);
        }
        else {
            // data.form contains the HTML for the replacement form
            $("#myform").replaceWith(data.form);
        }
	}).fail(function() {
		alert('failure :(');
	});
}

$('#update').click(function() {
	var updateData = {};
    var table_data = handsontable.getData();
    var row_count = table_data.length;
    var col_count = table_data[0].length;
    var grid_data = [];
    var grid_data_index = 0;

    for (i = 0; i < row_count; i++) {
        for (j = 0; j < col_count; j++) {
            if (table_data[i][j] === null) {
                grid_data[grid_data_index] = "";
            } else {
                grid_data[grid_data_index] = table_data[i][j];
            }
            grid_data_index++;
        }
    }

    var thisTableData = {
        grid_data: grid_data,
        row_count: row_count,
        col_count: col_count,
    };

    updateData["table"] = thisTableData;
    updateData["comparison_classes"] = comparison_classes;
    updateData["baselineName"] = $("#baseline_name").val();
    var selected = $("#comparisonTypes input[type='radio']:checked");
    var selectedValue = selected.val();
    updateData["comparisonType"] = selectedValue;

	$.ajax({
	  url: "/baselines/" + baseline_id,
	  data: JSON.stringify(updateData), //returns all cells' data
	  dataType: 'json',
	  contentType: 'application/json',
	  type: 'POST',
	  success: function (data, textStatus) {
		//alert(textStatus);
		if (data.redirect_url) {
            window.location.href = data.redirect_url;
        }
        else {
            // data.form contains the HTML for the replacement form
            $("#myform").replaceWith(data.form);
        }
	  },
	  error: function (data, textStatus) {
	    alert(JSON.stringify(data));
		$console.text('Save error. POST method is not allowed on GitHub Pages. Run this example on your own server to see the success message.');
	  }
	});

});
