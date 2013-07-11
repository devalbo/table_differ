
var $container = $("#dataTable");
var $console = $("#example1console");
var $parent = $container.parent();

$container.handsontable({
  startRows: 8,
  startCols: 6,
  rowHeaders: true,
  colHeaders: true,
  minSpareRows: 4,
  contextMenu: true,
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
        col_count: col_count};

    updateData["table"] = thisTableData;
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