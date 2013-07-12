
var dataTableIds = ["expectedTable", "actualTable"];
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
	});
	handsonDataTables[i] = $(dataTableJqueryId).data('handsontable');
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
	  url: "copy-paste",
	  data: JSON.stringify(tableData), //returns all cells' data
	  dataType: 'json',
	  contentType: 'application/json',
	  type: 'POST',
	  success: function (data, textStatus) {
		//alert(textStatus);
		if (data.redirect_url) {
            // data.redirect contains the string URL to redirect to
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