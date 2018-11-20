$(document).ready(function() {
    $('#example').DataTable();
    $('#example2').DataTable();
    $('#genretable').DataTable( {
        "order": [[ 1, "desc"]]
    } );
    $('#rectable').DataTable( {
        "order": [[ 1, "desc"]]
    } );
} );
