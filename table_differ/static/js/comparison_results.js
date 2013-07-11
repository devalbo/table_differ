var $container = $("#results-grid");
var $console = $("#example1console");
var $parent = $container.parent();

$container.handsontable({
    startRows: 8,
    startCols: 6,
    rowHeaders: true,
    colHeaders: true,
    minSpareRows: 4,
    contextMenu:
        {
            callback: function (key, options) {
              if (key === 'ignore') {
                setTimeout(function () {
                  //timeout is used to make sure the menu collapsed before alert is shown
                  alert("Will add code to ignore cell value");
                }, 100);
              } else if (key === 'use_actual') {
                setTimeout(function () {
                  //timeout is used to make sure the menu collapsed before alert is shown
                  alert("Will add code to expect actual value");
                }, 100);
              }
            },
            items: {
                "use_actual": {name: 'Set Expected to Actual'},
                "ignore": {name: 'Ignore Cell Differences'},
            }
        }
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