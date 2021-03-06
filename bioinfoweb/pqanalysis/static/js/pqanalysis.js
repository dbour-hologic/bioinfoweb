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
	* Retrieves the selected worklist from dropdown and returns
	* the file contents to the dynamic upload box. The optional
	* primaryKey argument allows us to manually select which
	* key to select.
	**/
	function dynamicWorklistRetrieve(primaryKey) {

		if (typeof primaryKey === 'undefined') {
			getValue = $("#id_file_upload_selection option:selected").val();
		} else {
			getValue = primaryKey;
		}
		
		
		$.ajax({
			type:"GET",
			url: "prepopulate-worklist/" + getValue,
			success: function(fileData)
			{
				parsed_JSON = JSON.parse(fileData);
				addWorklistRows(parsed_JSON.rows)
			}
		});
	}

	/**
	* Populates the worklist through worklist selection.
	*/
	$("#id_file_upload_selection").change(function() {
		dynamicWorklistRetrieve();
	});

	/**
	* Populates the default worklist through clicking. The
	* default value can change depending on how its
	* represented in the database.
	*/
	$("#load-worklist-default").click(function() {
		dynamicWorklistRetrieve(11);
	});	

	/**
	* Clears the form with 'Clear' button
	**/
	$("#clickClear").click(function() {
		clear_form($("#fusionForm"))
	});


	/**
	 * Helper function to dynamically populate the worklist form with 
	 * previously uploaded worklist. The way it performs addition of 
	 * rows is the same as the manual 'add rows' button.
	 **/
	function addWorklistRows(getData) {

		// 'Refreshes'/removes the old rows of data
		$("#fusionForm > div").each(function(index, element) {
			if ($(this).attr("data-worklist-index") != null) {
				$(this).remove();	
			}
		});		

		var worklistIndex = 0;

		$.each(getData, function(index, value) {


			var term = value.term;
			var type = value.type;
			var logvector = value.logvector;

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
			.find('[name="worklist.type"]').attr('name', 'worklist[' + worklistIndex + '].type').end();


			$("input[name='worklist["+worklistIndex+"].name']").val(value.term);
			$("input[name='worklist["+worklistIndex+"].type']").val(value.type);
			$("input[name='worklist["+worklistIndex+"].category']").val(value.logvector);

			// Resets the first icon to a plus since template creates removal buttons
			if (worklistIndex == 0) {
	
				$("#fusionForm > [data-worklist-index=0] > div > button").attr('class', 'btn btn-default addButton');
				$("#fusionForm > [data-worklist-index=0] > div > button > span").attr('class', 'glyphicon glyphicon-plus');
			}

			worklistIndex++;

			$('.worklist-input').each(function() {

				// Add a different rule to the name field which allows other characters
				if (this.name.indexOf("name") == -1) {
					$(this).rules("add", {
						required: true,
						alphaOnly: true,
						messages: {
							alphaOnly: "Only letters and numbers."
						}
					});
				} else {
					$(this).rules("add", {
						required: true,
					});
				}
			});

		});
	};

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

				// Add a different rule to the name field which allows other characters
				if (this.name.indexOf("name") == -1) {
					$(this).rules("add", {
						required: true,
						alphaOnly: true,
						messages: {
							alphaOnly: "Only letters and numbers."
						}
					});
				} else {
					$(this).rules("add", {
						required: true,
					});
				}
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
				alphaOnly: false,
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
				required: false,
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
					clear_form($("#fusionForm"));
					$("#success-upload").show();
					// Calls a django view to get the updated list
					update_list();
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
	* Retrieves the selected limitslist from dropdown and returns
	* the file contents to the dynamic upload box. The optional
	* primaryKey argument allows us to manually select which
	* key to select.
	**/
	function dynamicLimitsListRetrieve(primaryKey)
	{
		if (typeof primaryKey === 'undefined') {
			getValue = $("#id_file_limits_upload_selection option:selected").val();
		} else {
			getValue = primaryKey;
		}
		
		$.ajax({
			type:"GET",
			url: "prepopulate-limitslist/" + getValue,
			success: function(fileData)
			{
				console.log(fileData);
				parsed_JSON = JSON.parse(fileData);
				addLimitslistRows(parsed_JSON.rows)
			}
		});
	}


	/**
	* Populates the limitslist through worklist selection.
	*/
	$("#id_file_limits_upload_selection").change(function() {
		dynamicLimitsListRetrieve();
	});

	/**
	* Populates the default limitslist through clicking. The
	* default value can change depending on how its
	* represented in the database.
	*/
	$("#load-limitslist-default").click(function() {
		dynamicLimitsListRetrieve(6);
	});		

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
	 * Helper function to dynamically populate the limits list form with 
	 * previously uploaded limits list. The way it performs addition of 
	 * rows is the same as the manual 'add rows' button.
	 **/
	function addLimitslistRows(getData) {

		// 'Refreshes'/removes the old rows of data
		$("#fusionLimitsForm > div").each(function(index, element) {
			if ($(this).attr("data-limitslist-index") != null) {
				$(this).remove();	
			}
		});		

		var limitsListIndex = 0;;

		$.each(getData, function(index, value) {


			var sampletype = value.sampletype;
			var channel = value.channel;
			var sampthreshold = value.threshold; 
			var directionlogic = value.direction;

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


			$("input[name='limitslist["+limitsListIndex+"].name']").val(value.sampletype);
			$("select[name='limitslist["+limitsListIndex+"].channel']").val(value.channel);
			$("select[name='limitslist["+limitsListIndex+"].logic']").val(value.direction);
			$("input[name='limitslist["+limitsListIndex+"].threshold']").val(value.threshold);

			// Resets the first icon to a plus since template creates removal buttons
			if (limitsListIndex == 0) {
	
				$("#fusionLimitsForm > [data-limitslist-index=0] > div > button").attr('class', 'btn btn-default addLimitsButton');
				$("#fusionLimitsForm > [data-limitslist-index=0] > div > button > span").attr('class', 'glyphicon glyphicon-plus');
			}

			limitsListIndex++;

			$('.limitslist-input').each(function() {
				$(this).rules("add", {
					required: true,
					alphaOnly: true,
					messages: {
						alphaOnly: "Only letters and numbers."
					}
				});
			});

		});
	};


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
				number: true
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
				number: "Only numbers."
			}
		},

		submitHandler: function(form, event) {

			// Needed to prevent default action
			event.preventDefault();

			var data_collection = limits_data_collect();

			$.ajax({
				type: "POST",
				url: "limits-upload/",
				data: JSON.stringify(data_collection),
				datatype: "application/json",
				cache: false,
				success: function(json_data) {
					clear_form($("#fusionLimitsForm"));
					$("#limits-success-upload").show();
					update_limits_list();
					return true;
				},
				error: function() {
					alert("ERROR");
				}
			});
			return false;
		}	
	});

	/**
	* limits_data_collect() is a function that is used for collecting
	* data from a dynamically generated form that creates rows
	* and returns this data as a JSON object.
	*
	**/
	function limits_data_collect() {
		// Holds the group of data per row
		data_results = {};

		$("#fusionLimitsForm > div").each(function(index, element) {
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
		data_results["limitslist_name"] = limitslist_name;

		// Create JSON RESPONSE OBJECT
		var json_data = {
			json: data_results
		};

		return json_data
	};


// <--- Document on load --->
});
