
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

$('#compare').click(function() {

	$.ajax({
	  url: "/test_sheet_data",
	  dataType: 'json',
	  contentType: 'application/json',
	  type: 'GET',
	  success: function (res, textStatus) {
		alert(res.data);
		if (res.data) {
            handsontable.loadData(res.data);
            $console.text('Data loaded');
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