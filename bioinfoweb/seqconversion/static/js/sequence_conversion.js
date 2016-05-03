
$(document).ready(function() {
	
	// Clear sequence field function
	$("#clear").click(function(){
		var elem = document.getElementById("seqField");
		elem.value = "";
	});

	var elem = document.getElementById("seqField");
	elem.value = document.getElementById("origSeqField").innerHTML;

	// Validate inputs in the textbox
	$("#seqField").on('change keyup paste', function() {
		var $th = $(this);
		$th.val($th.val().replace(/[^ATCGYRWSKMDVHBXNatcgyrwskmdvhbxn]/g, function(){ return '';}))
	});

});

