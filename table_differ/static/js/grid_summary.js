
var $container = $("#gridsummary");
var $console = $("#example1console");
var $parent = $container.parent();
var mismatch_coords = [];

var errorRenderer = function (instance, td, row, col, prop, value, cellProperties) {
    td.style.fontWeight = 'bold';
    td.style.color = 'yellow';
    td.style.background = 'pink';
};

$container.handsontable({
  startRows: 8,
  startCols: 6,
  rowHeaders: true,
  colHeaders: true,
  minSpareRows: 6,
  contextMenu: true,
  cells: function (row, col, prop) {
//    this.renderer = cellRenderer; //uses function directly
  },
});

var handsontable = $container.data('handsontable');


//$('#compare').click(function() {
$('#results').ready(function() {
	$.ajax({
	  url: "/data/new_results/" + comparison_id,
	  dataType: 'json',
	  contentType: 'application/json',
	  type: 'GET',
	  success: function (res, textStatus) {
		if (res.data) {
            handsontable.loadData(res.data["cells"]);
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

