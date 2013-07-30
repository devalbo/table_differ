
var $container = $("#dataTable");
var $console = $("#example1console");
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

function get_default_class() {
    var selected = $("#comparisonTypes input[type='radio']:checked");
    var selectedValue = selected.val();
    return cmp_type_to_css_class[selectedValue];
}

function do_cells_update(update_type) {
    setTimeout(function () {
      //timeout is used to make sure the menu collapsed before alert is shown
      var selected = handsontable.getSelected();
      var updateAction = {update_type: update_type,
                          update_args: {
                              region: selected
                          }
      };
      postUpdateAction(updateAction);
    }, 100);

}

$container.handsontable({
    startRows: 8,
    startCols: 6,
    rowHeaders: true,
    colHeaders: true,
    contextMenu: {
        callback: function (key, options) {
          if (key === 'ignore_cells_in_region' ||
              key === 'literal_compare_cells_in_region' ||
              key === 'regex_compare_cells_in_region')
          {
              do_cells_update(key);
          }
        },
        items: {
            "ignore_cells_in_region": {name: 'Ignore Differences'},
            "literal_compare_cells_in_region": {name: 'Do Literal Comparison'},
            "regex_compare_cells_in_region": {name: 'Do Regular Expression Comparison'},
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
    afterChange: function(changes, source) {
        if (changes != null) {
            for (var i = 0; i < changes.length; i++) {
                var change = changes[i];
                var row = change[0];
                var col = change[1];
                var old_value = change[2];
                var new_value = change[3];
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
		url: baseline_grid_data_url,
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
	  }
	});

});

function postUpdateAction(updateAction) {
  if (updateAction != null) {
    $.ajax({
      url: update_baseline_grid_data_url,
      data: JSON.stringify(updateAction),
      dataType: 'json',
      contentType: 'application/json',
      type: 'POST',
      success: function (data, textStatus) {
        updateBaselineContents();
      },
      error: function (data, textStatus) {
        alert(JSON.stringify(data));
          alert(textStatus)
          updateBaselineContents();
      }
    });
  }
}