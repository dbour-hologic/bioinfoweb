// The following is from the jQuery validation library
// Has various functions to help validate before submission.
$(document).ready(function() {


	$("#msae_access_id").validate({
		
		errorPlacement: function(label, element)
	   {
	   		// Error message placement below checkboxes
			if (element.attr("name") === "employee_signed" || element.attr("name") === "user_status"
				|| element.attr("name") === "user_location")
			{
				var lastRadio = $('[name="' + element.attr("name") + '"]:last');
				lastRadio.closest('label').append("<br>").append(label);
			} 
			// Error message placement below dropdown
			else if (element.attr("name") === "request_type")
			{
				element.parent().append("<br>").append(label);
			}
			else 
			{
				label.insertAfter(element);
			}
		}
		
	});

});