// DataTable library for organization of results
$(document).ready(function() {

	$.validator.addMethod("alphaonly", function(value, element) {
		return this.optional(element) || /^[a-z0-9]+$/i.test(value);
	}),

	$("#pqupload").validate({
		rules: {
			'analysis_id': {
				required: true,
				alphaonly:true,
				rangelength:[1,99]
			},
			'submitter': {
				required: true,
				rangelength:[1,99]
			}
		},
		messages: {
			'analysis_id': 'Only letters and numbers allowed.'
		}
	});

	/*************************************************************
	*
	* Below is a list of functions for the dynamic workflow.
	*
	**************************************************************/

	/**
	* Hides the success banner when clicked anywhere.
	**/
	$(document).click(function() {
		$("#success-upload").hide();
	});

	/**
	* Clears the form with 'Clear' button
	**/
	$("#clickClear").click(function() {
		clear_form($("#fusionForm"))
	});

	/**
	* Feature to add/remove rows of data for workflow.
	* 
	**/
	$("#fusionForm").on("click", ".addButton", (function() {

		var worklistIndex = 0;

		return function() {

			worklistIndex++;

			var $template = $("#datagroup-template"),
			$clone = $template
			.clone()
			.removeClass("hide")
			.removeAttr("id")
			.attr("data-worklist-index", worklistIndex)
			.insertBefore($template);

			$clone
			.find('[name="worklist.name"]').attr('name', 'worklist[' + worklistIndex + '].name').end()
			.find('[name="worklist.category"]').attr('name', 'worklist[' + worklistIndex + '].category').end()
			.find('[name="worklist.type"]').attr('name', 'worklist[' + worklistIndex + '].type').end()

			$('.worklist-input').each(function() {
				$(this).rules("add", {
					required: true,
					alphaOnly: true,
					messages: {
						alphaOnly: "Only letters and numbers."
					}
				});
			});
		};
	})()).on("click", ".removeButton", function() {
		var $row = $(this).parents(".form-group").remove();
	});

	/**
	* Add validation method that only accepts
	* alphanumerics.
	*
	**/
	$.validator.addMethod("alphaOnly", function(value, element) {
		return this.optional(element) || /^[a-z0-9\s]+$/i.test(value); 
	});

	/**
	* Validation method for dynamically generated
	* workflow form.
	*
	**/
	$("#fusionForm").validate({
		// Initializing initial rules for static content - necessary before "adding" more rules
		rules: {
			'worklist[0].name': {
				required: true,
				alphaOnly: true,
			},
			'worklist[0].type': {
				required: true,
				alphaOnly: true
			},
			'worklist[0].category': {
				required: true,
				alphaOnly: true
			},
			'submitter_name': {
				required: true
			},
			'worklist_name': {
				required: true,
				alphaOnly: true
			}
		},
		messages: {
			'worklist[0].name': {
				alphaOnly: "Only letters and numbers."
			},
			'worklist[0].type': {
				alphaOnly: "Only letters and numbers."
			},
			'worklist[0].category': {
				alphaOnly: "Only letters and numbers."
			},
			'worklist_name': {
				alphaOnly: "Only letters and numbers."
			}
		},

		submitHandler: function(form) {

			var data_collection = data_collect();


			$.ajax({
				type: "POST",
				url: "worklist-upload/",
				data: JSON.stringify(data_collection),
				datatype: "application/json",
				cache: false,
				success: function(json_data) {
					console.log(json_data);
					clear_form($("#fusionForm"));
					$("#success-upload").show();
					return true;
				},
				error: function() {
					alert("ERROR");
				}
			});
		}		
	})

	/**
	* clear_form() is a function that is used
	* for clearing the input from the form quickly.
	*/

	function clear_form($form) {
		$form.find('input:text').val('');
	};

	/**
	* data_collect() is a function that is used for collecting
	* data from a dynamically generated form that creates rows
	* and returns this data as a JSON object.
	*
	**/
	function data_collect() {
		// Holds the group of data per row
		data_results = {};

		$("#fusionForm > div").each(function(index, element) {
			if ($(this).attr("data-worklist-index") != null) {
				data_results[index] = {};
				$(this).children().find("[name]").each(function() {
					var propertyName = $(this).attr("name");
					var propertyValue = $(this).val();
					data_results[index][propertyName] = propertyValue
				});
			}
		});

		var submitter_name = $("#worklist-submitter").val();
		var worklist_name = $("#worklist-name-input").val();

		data_results["submitter_name"] = submitter_name;
		data_results["worklist_name"] = worklist_name;

		// Create JSON RESPONSE OBJECT
		var json_data = {
			json: data_results
		};

		return json_data
	};


	/*************************************************************
	*
	* Below is a list of functions for the dynamic limits.
	*
	**************************************************************/

	/**
	* Hides the success banner when clicked anywhere.
	**/
	$(document).click(function() {
		$("#limits-success-upload").hide();
	});

	/**
	* Clears the form with 'Clear' button
	**/
	$("#clickClearLimits").click(function() {
		clear_form($("#fusionLimitsForm"))
	});

	/**
	* Feature to add/remove rows of data for workflow.
	* 
	**/
	$("#fusionLimitsForm").on("click", ".addLimitsButton", (function() {

		var limitsListIndex = 0;

		return function() {

			limitsListIndex++;

			var $template = $("#datagroup-template-limits"),
			$clone = $template
			.clone()
			.removeClass("hide")
			.removeAttr("id")
			.attr("data-limitslist-index", limitsListIndex)
			.insertBefore($template);

			$clone
			.find('[name="limitslist.name"]').attr('name', 'limitslist[' + limitsListIndex + '].name').end()
			.find('[name="limitslist.channel"]').attr('name', 'limitslist[' + limitsListIndex + '].channel').end()
			.find('[name="limitslist.logic"]').attr('name', 'limitslist[' + limitsListIndex + '].logic').end()
			.find('[name="limitslist.threshold"]').attr('name', 'limitslist[' + limitsListIndex + '].threshold').end()

			$('.limitslist-input').each(function() {
				$(this).rules("add", {
					required: true,
					alphaOnly: true,
					messages: {
						alphaOnly: "Only letters and numbers."
					}
				});
			});
		};
	})()).on("click", ".removeButton", function() {
		var $row = $(this).parents(".form-group").remove();
	});	

	/**
	* Validation method for dynamically generated
	* workflow form.
	*
	**/
	$("#fusionLimitsForm").validate({
		// Initializing initial rules for static content - necessary before "adding" more rules
		rules: {
			'limitslist[0].name': {
				required: true,
				alphaOnly: true,
			},
			'limitslist[0].threshold': {
				required: true,
				alphaOnly: true
			},
			'submitter_name_limits': {
				required: true
			},
			'limits_name': {
				required: true
			}
		},
		messages: {
			'limitslist[0].name': {
				alphaOnly: "Only letters and numbers."
			},
			'limitslist[0].threshold': {
				alphaOnly: "Only letters and numbers."
			}
		},

		submitHandler: function(form) {

			var data_collection = data_collect();

			$.ajax({
				type: "POST",
				url: "/echo/json/",
				data: data_collection,
				cache: false,
				success: function(json_data) {
					console.log(json_data);
					clear_form($("#fusionForm"));
					$("#success-upload").show();
					return false;
				},
				error: function() {
					alert("ERROR");
				}
			});
		}		
	})

	/**
	* limits_data_collect() is a function that is used for collecting
	* data from a dynamically generated form that creates rows
	* and returns this data as a JSON object.
	*
	**/
	function limits_data_collect() {
		// Holds the group of data per row
		data_results = {};

		$("#fusionForm > div").each(function(index, element) {
			if ($(this).attr("data-limitslist-index") != null) {
				data_results[index] = {};
				$(this).children().find("[name]").each(function() {
					var propertyName = $(this).attr("name");
					var propertyValue = $(this).val();
					data_results[index][propertyName] = propertyValue
				});
			}
		});

		var submitter_name = $("#limitsList-submitter").val();
		var limitslist_name = $("#limits-name-input").val();

		data_results["submitter_name"] = submitter_name;
		data_results["limitslist_name"] = worklist_name;

		// Create JSON RESPONSE OBJECT
		var json_data = {
			json: JSON.stringify(data_results)
		};

		return json_data
	};


// <--- Document on load --->
});
