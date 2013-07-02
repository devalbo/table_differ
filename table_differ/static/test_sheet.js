
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
	var baselineData = {
		baseline_id: $('#baseline-id').val()
	};
	
	$.ajax({
		url: "data",
		type: 'POST',
		dataType: 'json',
		data: baselineData
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