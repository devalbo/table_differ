var $container = $("#results-grid");
var $console = $("#example1console");
var $parent = $container.parent();

var comparison_results_data = null;

var cellRenderer = function (instance, td, row, col, prop, value, cellProperties) {

    if (comparison_results_data != null) {
        var item_data = comparison_results_data["cells"];
        var item_styles = comparison_results_data["cell_statuses"];

        try {
            td.className = item_styles[row][col];
            td.innerHTML = item_data[row][col];
        } catch(e) {
            td.className = "unexpected";
        }
    }
};

$container.handsontable({
    startRows: 0,
    startCols: 0,
    rowHeaders: true,
    colHeaders: true,
    minSpareRows: 0,
    contextMenu:
        {
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
              } else if (key === 'use_actual') {
                setTimeout(function () {
                  //timeout is used to make sure the menu collapsed before alert is shown
                  var selected = handsontable.getSelected();
                  updateAction = {update_type: "use_actual_in_region",
                                  update_args: {
                                      region: selected
                                  } };
                  postUpdateAction(updateAction);
                }, 100);
              }

            },
            items: {
                "use_actual": {name: 'Set Expected to Actual in Baseline'},
                "ignore": {name: 'Ignore Cell Differences in Baseline'},
            }
        },
    cells: function (row, col, prop) {
        this.renderer = cellRenderer; //uses function directly
    },

});

var handsontable = $container.data('handsontable');


$(document).ready( function() {
	updateTableContents();
});

function updateTableContents() {

	$.ajax({
        url: result_grid_data_url,
        dataType: 'json',
	    contentType: 'application/json',
	    type: 'GET',

	}).done(function(res, textStatus) {
		if (res.data) {
            comparison_results_data = res.data;
            handsontable.loadData(res.data["cells"]);
        }
	}).fail(function() {
		alert('failure :(');
	});
}

function postUpdateAction(updateAction) {
  if (updateAction != null) {
    $.ajax({
      url: update_result_grid_data_url,
      data: JSON.stringify(updateAction), //returns all cells' data
      dataType: 'json',
      contentType: 'application/json',
      type: 'POST',
      success: function (data, textStatus) {
        if (data.redirect_url) {
            // data.redirect contains the string URL to redirect to
            window.location.href = data.redirect_url;
        }
      },
      error: function (data, textStatus) {
        alert(JSON.stringify(data));
        $console.text('Save error. POST method is not allowed on GitHub Pages. Run this example on your own server to see the success message.');
      }
    });
  }

}