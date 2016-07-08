$(document).ready(function() {

	$('#id_file_upload_selection').click(function(){
		item = $(this).val()
		$('#hidden-database-selection').val(item)
	})

})


