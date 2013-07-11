
$(document).ready(function() {
    $('#resultsTable').dataTable( {
        "sDom": "<'row'<'span5 offset1'l><'span4 offset1'f>r>t<'row'<'span5 offset1'i><'span3 offset1'p>>",
//        "sPaginationType": "full_numbers"
    } );
} );

$.extend( $.fn.dataTableExt.oStdClasses, {
    "sWrapper": "dataTables_wrapper form-inline"
} );