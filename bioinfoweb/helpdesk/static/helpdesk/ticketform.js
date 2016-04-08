$(document).ready(function() {	

		// Keeps track of which form is showing
		var current_selected = "default";

		// Assign the IDs of the custom fields for different categories
		var sequencing_form = $("#seq_request_form");
		var training_form = $("#type_training_form");

		// Declare the targetted forms
		sequencing_form.hide();
		training_form.hide();

		// Hides forms until necessary - Used for adding extra fields for different
		// categories. The forms then get written into a text and entered into the
		// description box, so the fields are not actually saved into the database individually

		// Holds the selected dropdown of Queue
		var selected;

		$("#id_queue").change(function() {

			selected = $("#id_queue option:selected").text();

			if ((selected) === "Training Requests") {
				current_selected = training_form;
				training_form.show();
				sequencing_form.hide();
			} else if ((selected === "Sequencing Requests")) {
				current_selected = sequencing_form;
				training_form.hide();
				sequencing_form.show();
			} else if ((selected === "In-Silico Analysis")) {
				current_selected = "default";
				training_form.hide();
				sequencing_form.hide();
			} else {
				current_selected = "default";
				training_form.hide();
				sequencing_form.hide();
			}
			
		});	


		// ________________________________________________________________
		//
		// Temporary FIX for the DJANGO refresh on failure
		// so it would show the error and still render the correct forms
		selected = $("#id_queue option:selected").text();

			if ((selected) === "Training Requests") {
				current_selected = training_form;
				training_form.show();
				sequencing_form.hide();
			} else if ((selected === "Sequencing Requests")) {
				current_selected = sequencing_form;
				training_form.hide();
				sequencing_form.show();
			} else if ((selected === "In-Silico Analysis")) {
				current_selected = "default";
				training_form.hide();
				sequencing_form.hide();
			} else {
				current_selected = "default";
				training_form.hide();
				sequencing_form.hide();
			}
		// _______________________________________________________________


		// Appends the extra fields into description of issue before sending off

		$("#forpresubmit").click(function() {
			if (current_selected != "default") {
				var sentence = $(current_selected).serialize();
				$("#id_body").val(sentence);
			};
		});

});