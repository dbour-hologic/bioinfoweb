$(document).ready(function() {	

		$("#id_body").val("");

		// Keeps track of which form is showing
		var current_selected = "default";

		// Assign the IDs of the custom fields/sections for different categories
		var sequencing_form = $("#seq_request_form");
		var training_form = $("#type_training_form");
		var insilico_form = $("#insilico_form_section");

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
				insilico_form.hide();
			} else if ((selected === "Sequencing Requests")) {
				current_selected = sequencing_form;
				training_form.hide();
				sequencing_form.show();
				insilico_form.hide();
			} else if ((selected === "In-Silico Analysis")) {
				current_selected = "default";	
				training_form.hide();
				sequencing_form.hide();
				insilico_form.show();
			} else {
				current_selected = "default";
				training_form.hide();
				sequencing_form.hide();
				insilico_form.hide();
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
				insilico_form.hide();
			} else if ((selected === "Sequencing Requests")) {
				current_selected = sequencing_form;
				training_form.hide();
				sequencing_form.show();
				insilico_form.hide();
			} else if ((selected === "In-Silico Analysis")) {
				current_selected = "default";
				training_form.hide();
				sequencing_form.hide();
				insilico_form.show();
			} else {
				current_selected = "default";
				training_form.hide();
				sequencing_form.hide();
				insilico_form.hide();
			}
		// _______________________________________________________________


		// Appends the extra fields into description of issue before sending off

		$("#forpresubmit").click(function() {
			if (current_selected != "default") {
				var sentenceTxt = "";
				var sentenceObj = $(current_selected).serializeArray();
				jQuery.each(sentenceObj, function(i, sentenceObj) {
					sentenceTxt += sentenceObj.name + "\n" +
								  sentenceObj.value + "\n" +
								  "-----------" + "\n"
				});

				$("#id_body").val(sentenceTxt);
				console.log(sentenceTxt);
			};
		}); 
	});


$(document).ready(function() {


	// The following instructions are used for hiding/showing
	// the "OTHER" field in the list of project codes. The
	// "OTHER" field will only appear if there's a selection to "OTHER"
	// otherwise the "OTHER" field will be directly linked to whatever is selected

	initial_selected_project = $("#id_project_code option:selected").text();
	$("#id_project_code_alt").val(initial_selected_project)
	$("#id_project_code_alt").parent().parent().hide();

	$("#id_project_code").change(function() {

		selected_project = $("#id_project_code option:selected").text();

		if (selected_project !="Other") {
			$("#id_project_code_alt").parent().parent().hide();
			$("#id_project_code_alt").val(selected_project)
		} else {
			$("#id_project_code_alt").parent().parent().show();
			$("#id_project_code_alt").val("");
		}
	});
});