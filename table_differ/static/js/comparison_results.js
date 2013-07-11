var $container = $("#results-grid");
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
	updateTableContents();
});

function updateTableContents() {

	$.ajax({
        url: "/results/data/" + comparison_id,
        dataType: 'json',
	    contentType: 'application/json',
	    type: 'GET',

	}).done(function(res, textStatus) {
		if (res.data) {
            handsontable.loadData(res.data["cells"]);
        }
	}).fail(function() {
		alert('failure :(');
	});
}