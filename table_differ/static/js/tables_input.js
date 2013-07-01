
var dataTableIds = ["dataTable1", "dataTable2"];
var handsonDataTables = [];
for (var i = 0; i < dataTableIds.length; i++) {
	var data = [
		["", "", "", "", ""],
		["", "", "", "", ""],
		["", "", "", "", ""],
		["", "", "", "", " "],
		];
	var dataTableJqueryId = "#" + dataTableIds[i];
	$(dataTableJqueryId).handsontable({
		data: data,
		startRows: 6,
		startCols: 8,
		minSpareRows: 1,
		minSpareCols: 1,
		contextMenu:
				{
					callback: function (key, options) {
					  if (key === 'ignore') {
						setTimeout(function () {
						  //timeout is used to make sure the menu collapsed before alert is shown
						  alert("Will add code to call back to td_persist");
						}, 100);
					  }
					},
					items: {
						"ignore": {name: 'Ignore Cell Differences'},
						"hsep": "---------",
						"row_above": {},
						"row_below": {},
						"hsep1": "---------",
						"col_left": {},
						"col_right": {},
						"hsep2": "---------",
						"remove_row": {},
						"remove_col": {},
						"hsep3": "---------",
						"undo": {},
						"redo": {}
					}
				}
	});
	handsonDataTables[i] = $(dataTableJqueryId).data('handsontable');
//    $('#dataTable1 table').addClass('table');
//    $('#dataTable2 table').addClass('table');
}

function post_to_url(path, params, method) {
    method = method || "post"; // Set method to post by default, if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
         }
    }

    document.body.appendChild(form);
    form.submit();
}

$('#compare').click(function() {
	var tableData = {};
	for (var td_index = 0; td_index < dataTableIds.length; td_index++) {
		var table_data = handsonDataTables[td_index].getData();
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
			col_count: col_count};
		tableData[dataTableIds[td_index]] = thisTableData;
	}
	
	$.ajax({
	  url: "copy-paste-compare",
	  data: JSON.stringify(tableData), //returns all cells' data
	  dataType: 'json',
	  contentType: 'application/json',
	  type: 'POST',
	  success: function (data, textStatus) {
		//alert(textStatus);
		if (data.redirect_url) {
            // data.redirect contains the string URL to redirect to
			//alert("Redirect to " + data.redirect_url);
            window.location.href = data.redirect_url;
        }
        else {
            // data.form contains the HTML for the replacement form
            $("#myform").replaceWith(data.form);
        }
		//if (res.result === 'ok') {
		//  $console.text('Data saved');
		//}
		//else {
		//  $console.text('Save error');
		//}
	  },
	  error: function (data, textStatus) {
	    alert(JSON.stringify(data));
		$console.text('Save error. POST method is not allowed on GitHub Pages. Run this example on your own server to see the success message.');
	  }
	});

});