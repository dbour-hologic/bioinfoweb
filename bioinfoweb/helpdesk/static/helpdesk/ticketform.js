$(document).ready(function()
	{	

		var sentence;

		// Assign the IDs of the custom fields for different categories
		var sequencing_form = $("#seq_request_form");
		var training_form = $("#type_training_form");

		// Declare the targetted forms
		sequencing_form.hide();
		training_form.hide();

		// Hides forms until necessary - Used for adding extra fields for different
		// categories. The forms then get written into a text and entered into the
		// description box, so the fields are not actually saved into the database individually

		$("#id_queue").change(function() {

			var selected = $("#id_queue option:selected").text();

			if ((selected) === "Training Requests") {
				training_form.show();
				sequencing_form.hide();
			} else if ((selected === "Sequencing Requests")) {
				training_form.hide();
				sequencing_form.show();
			} else if ((selected === "In-Silico Analysis")) {
				training_form.hide();
				sequencing_form.hide();
			} else {
				training_form.hide();
				sequencing_form.hide();
			}
			
		});	

		// Appends the extra fields into description of issue before sending off
		$("#forpresubmit").click(function() {
			sentence = $("#seq_request_form").serialize();
			$("#id_body").val(sentence);
		})


	})