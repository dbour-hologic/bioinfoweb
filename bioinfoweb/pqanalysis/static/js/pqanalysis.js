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
			},
			'assay-analysis': {
				required: true
			}
		},
		messages: {
			'analysis_id': 'Only letters and numbers allowed.'
		},
		errorPlacement: function(error, element) {
			if ( element.is(":radio") ) {
				error.appendTo($('.checkboxError'));
			} else {
				error.insertAfter(element);
			}

		}
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

			// Check the time of worklist being submitted
			// i.e. either 'fusion' or 'tma'
			var assaytype;
			var get_assay_option = $('#assay_option_selection').val();
			if (get_assay_option === 'tma') {
				assaytype = 'tma';
			} else {
				assaytype = 'fusion';
			}


			$.ajax({
				type: "POST",
				url: "worklist-upload/" + assaytype + "/",
				data: JSON.stringify(data_collection),
				datatype: "application/json",
				cache: false,
				success: function(json_data) {assay_option_selection
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
	});
	/**
	* Validation method for dynamically generated
	* workflow form.
	*
	**/
	$("#tmaForm").validate({
		// Initializing initial rules for static content - necessary before "adding" more rules
		rules: {
			'worklist[0].name': {
				required: true
			},
			'worklist[0].type': {
				required: true
			},
			'submitter_name': {
				required: true
			},
			'worklist_name': {
				required: false
			}
		},

		submitHandler: function(form) {


			// Needed to prevent default action
			event.preventDefault();

			var data_collection = data_collect_tma();

			// Check the time of worklist being submitted
			// i.e. either 'fusion' or 'tma'
			var assaytype;
			var get_assay_option = $('#assay_option_selection').val();
			if (get_assay_option === 'tma') {
				assaytype = 'tma';
			} else {
				assaytype = 'fusion';
			}

			$.ajax({
				type: "POST",
				url: "worklist-upload/" + assaytype + "/",
				data: JSON.stringify(data_collection),
				datatype: "application/json",
				cache: false,
				success: function(json_data) {
					clear_form($("#tmaForm"));
					$("#success-upload-tma").show();
					// Calls a django view to get the updated list
					update_tma_list();
					return true;
				},
				error: function() {
					alert("ERROR");
				}
			});
		}
	});
	/**
	* Validation method for dynamically generated
	* limits form.
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

			// Check the time of worklist being submitted
			// i.e. either 'fusion' or 'tma'
			var assaytype;
			var get_assay_option = $('#assay_option_selection').val();
			if (get_assay_option === 'tma') {
				assaytype = 'tma';
			} else {
				assaytype = 'fusion';
			}

			$.ajax({
				type: "POST",
				url: "limits-upload/" + assaytype + "/",
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

	$("#tmaLimitsForm").validate({
		// Initializing initial rules for static content - necessary before "adding" more rules
		rules: {
			'limitslist-tma[0].name': {
				required: true,
			},
			'limitslist-tma[0].minthreshold': {
				required: true,
				number: true
			},
			'limitslist-tma[0].maxthreshold': {
				required: true,
				number: true
			},
			'limitslist-tma[0].icthreshold': {
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
			'limitslist-tma[0].minthreshold': {
				number: "Only numbers."
			},
			'limitslist-tma[0].maxthreshold': {
				number: "Only number."
			},
			'limitslist-tma[0].icthreshold': {
				number: "Only number."
			}
		},

		submitHandler: function(form, event) {

			// Needed to prevent default action
			event.preventDefault();

			var data_collection = limits_data_collect_tma();

			// Check the time of worklist being submitted
			// i.e. either 'fusion' or 'tma'
			var assaytype;
			var get_assay_option = $('#assay_option_selection').val();
			if (get_assay_option === 'tma') {
				assaytype = 'tma';
			} else {
				assaytype = 'fusion';
			}

			$.ajax({
				type: "POST",
				url: "limits-upload/" + assaytype + "/",
				data: JSON.stringify(data_collection),
				datatype: "application/json",
				cache: false,
				success: function(json_data) {
					clear_form($("#tmaLimitsForm"));
					$("#limits-success-upload-tma").show();
					update_tma_limits_list();
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
	* Validation method for dynamically generated
	* recovery form
	*
	**/
	$("#tmaRecoveryForm").validate({
		// Initializing initial rules for static content - necessary before "adding" more rules
		rules: {
			'recovery[0].runid': {
				required: true,
			},
			'reocvery[0].lot': {
				required: true
			},
			'recovery[0].pol': {
				required: true
			},
			'recovery[0].ltr': {
				required: true
			},
			'submitter_name': {
				required: true
			},
			'recovery_filename': {
				required: true
			}
		},

		submitHandler: function(form, event) {

			// Needed to prevent default action
			event.preventDefault();

			var data_collection = recovery_data_collect_tma();


			$.ajax({
				type: "POST",
				url: "recovery-upload/",
				data: JSON.stringify(data_collection),
				datatype: "application/json",
				cache: false,
				success: function(json_data) {
					clear_form($("#tmaRecoveryForm"));
					$("#success-upload-recovery-tma").show();
					// update_tma_limits_list();
					return true;
				},
				error: function() {
					alert("ERROR");
				}
			});
			return false;
		}
	});
	/*************************************************************
	*
	* Below is a list of functions show/display
	*
	**************************************************************/

    /**
	 * Hide/Show assay selection options
     *
     */

	var get_assay_option = $('#assay_option_selection').val();
	$('#fusionAdvancedOptions').show();
	$('#tma_checkbox_options').hide();
	$('#tmaAdvancedOptions').hide();

	$('#assay_option_selection').change(function() {
	    get_assay_option = $('#assay_option_selection').val();
		if (get_assay_option === 'tma') {
			$('#tma_checkbox_options').show();
			$('#tmaAdvancedOptions').show();
			$('#fusionAdvancedOptions').hide();
			$('#fusion_checkbox_options').hide();
		}
		else {
			$('#tma_checkbox_options').hide();
			$('#tmaAdvancedOptions').hide();
			$('#fusion_checkbox_options').show();
			$('#fusionAdvancedOptions').show();
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
		$("#success-upload-tma").hide();
		$("#success-upload-recovery-tma").hide();
	});

	/**
	* Retrieves the selected worklist from dropdown and returns
	* the file contents to the dynamic upload box. The optional
	* primaryKey argument allows us to manually select which
	* key to select.
	**/
	function dynamicWorklistRetrieve(primaryKey) {

		var getValue;

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
				var parsed_JSON = JSON.parse(fileData);
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
		dynamicWorklistRetrieve();
	});	

	/**
	* Clears the form with 'Clear' button
	**/
	$("#clickClear").click(function() {
		clear_form($("#fusionForm"))
	});

	$("#clickClearTMA").click(function() {
		clear_form($("#tmaForm"))
	});

	$("#clickClearRecoveryTMA").click(function() {
		clear_form($("#tmaRecoveryForm"))
	});

	$("#clickClearLimitsTMA").click(function() {
		clear_form($("#tmaLimitsForm"))
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


			$("#worklist-upload input[name='worklist["+worklistIndex+"].name']").val(value.term);
			$("#worklist-upload input[name='worklist["+worklistIndex+"].type']").val(value.type);
			$("#worklist-upload input[name='worklist["+worklistIndex+"].category']").val(value.logvector);

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
    }
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
			.find('[name="worklist.type"]').attr('name', 'worklist[' + worklistIndex + '].type').end();

			$('.worklist-input').each(function() {

				// Add a different rule to the name field which allows other characters
					$(this).rules("add", {
						required: true,
					});
			});
		};

	})()).on("click", ".removeButton", function() {
		var $row = $(this).parents(".form-group").remove();
	});
    /**
	* Feature to add/remove rows of data for workflow.
	*
	**/
	$("#tmaForm").on("click", ".addButton", (function() {

		var worklistIndex = 0;

		return function() {

			worklistIndex++;

			var $template = $("#datagroup-template-tma"),
			$clone = $template
			.clone()
			.removeClass("hide")
			.removeAttr("id")
			.attr("data-worklist-index", worklistIndex)
			.insertBefore($template);

			$clone
			.find('[name="worklist-tma.name"]').attr('name', 'worklist-tma[' + worklistIndex + '].name').end()
			.find('[name="worklist-tma.type"]').attr('name', 'worklist-tma[' + worklistIndex + '].type').end()

			$('.worklist-input-tma').each(function() {

				// Add a different rule to the name field which allows other characters

				$(this).rules("add", {
					required: true,
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
	* clear_form() is a function that is used
	* for clearing the input from the form quickly.
	*/

	function clear_form($form) {
		$form.find('input:text').val('');
		// Default values when reset
		$form.find('.limitslist-input-tma-ictt').val('99');
    }
    /**
	* data_collect() is a function that is used for collecting
	* data from a dynamically generated form that creates rows
	* and returns this data as a JSON object.
	*
	**/

    function data_collect_tma() {
        // Holds the group of data per row
        var data_results = {};
        $("#tmaForm > div").each(function (index, element) {

            if ($(this).attr("data-worklist-index") != null) {
                data_results[index] = {};
                $(this).children().find("[name]").each(function () {

                    var propertyName = $(this).attr("name");
                    var propertyValue = $(this).val();

                    data_results[index][propertyName] = propertyValue
                });
            }
        });

        var submitter_name = $("#worklist-submitter-tma").val();
        var worklist_name = $("#worklist-name-input-tma").val();

        data_results["submitter_name"] = submitter_name;
        data_results["worklist_name"] = worklist_name;

        var json_data = {
        	json: data_results
		};

        return json_data
    }

	function data_collect() {
		// Holds the group of data per row
		var data_results = {};

		$("#fusionForm > div").each(function(index, element) {
			if ($(this).attr("data-worklist-index") != null) {
				data_results[index] = {};
				$(this).children().find("[name]").each(function() {
					var propertyName = $(this).attr("name");
					var propertyValue = $(this).val();

					console.log(data_results);
					console.log("Property name: ", propertyName);
                    console.log("Property value: ", propertyValue);

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
    }
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
		dynamicLimitsListRetrieve();
	});		

	/**
	* Hides the success banner when clicked anywhere.
	**/
	$(document).click(function() {
		$("#limits-success-upload").hide();
		$("#limits-success-upload-tma").hide();
	});

	/**
	* Clears the form with 'Clear' button
	**/
	$("#clickClearLimits").click(function() {
		clear_form($("#fusionLimitsForm"))
	});
	$("#clickClearTMA").click(function() {
		clear_form($("#tmaLimitsForm"))
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


		var limitsListIndex = 0;
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
			.find('[name="limitslist.threshold"]').attr('name', 'limitslist[' + limitsListIndex + '].threshold').end();


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
    }
    /**
	* Feature to add/remove rows of data for limits,
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
			.find('[name="limitslist.threshold"]').attr('value', '99').end();

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
	* Feature to add/remove rows of data for limits,
	*
	**/
	$("#tmaLimitsForm").on("click", ".addLimitsButton", (function() {

		var limitsListIndexTMA = 0;


		return function() {

			limitsListIndexTMA++;
			console.log(limitsListIndexTMA);

			var $template = $("#datagroup-template-limits-tma"),
			$clone = $template
			.clone()
			.removeClass("hide")
			.removeAttr("id")
			.attr("data-limitslist-index", limitsListIndexTMA)
			.insertBefore($template);

			$clone
			.find('[name="limitslist-tma.name"]').attr('name', 'limitslist-tma[' + limitsListIndexTMA + '].name').end()
			.find('[name="limitslist-tma.minthreshold"]').attr('name', 'limitslist-tma[' + limitsListIndexTMA + '].minthreshold').end()
			.find('[name="limitslist-tma.maxthreshold"]').attr('name', 'limitslist-tma[' + limitsListIndexTMA + '].maxthreshold').end()
			.find('[name="limitslist-tma.icthreshold"]').attr('name', 'limitslist-tma[' + limitsListIndexTMA + '].icthreshold').end();

			$('.limitslist-input-tma').each(function() {
				// Add a different rule to the name field which allows other characters
				console.log($(this));
				$(this).rules("add", {
					required: true
				});
			});
		};
	})()).on("click", ".removeButton", function() {
		var $row = $(this).parents(".form-group").remove();
	});



	/**
	* limits_data_collect() is a function that is used for collecting
	* data from a dynamically generated form that creates rows
	* and returns this data as a JSON object.
	*
	**/

	function limits_data_collect_tma() {
		var data_results = {}

		$("#tmaLimitsForm > div").each(function(index, element) {
			if ($(this).attr("data-limitslist-index") != null) {
				data_results[index] = {};
				$(this).children().find("[name]").each(function() {
					var propertyName = $(this).attr("name");
					var propertyValue = $(this).val();
					data_results[index][propertyName] = propertyValue
				});
			}
		});

		var submitter_name = $("#limitsList-submitter-tma").val();
		var limitslist_name = $("#limits-name-input-tma").val();

		data_results["submitter_name"] = submitter_name;
		data_results["limitslist_name"] = limitslist_name;

		var json_data = {
			json: data_results
		};

		return json_data
	}


	function limits_data_collect() {
		// Holds the group of data per row
		var data_results = {};

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
    }


	/*************************************************************
	*
	* Below is a list of functions for the recovery list
	*
	**************************************************************/
    /**
	* Feature to add/remove rows of data for workflow.
	*
	**/
	$("#tmaRecoveryForm").on("click", ".addButton", (function() {

		var recoveryIndex = 0;

		return function() {

			recoveryIndex++;

			var $template = $("#datagroup-template-recovery-tma"),
			$clone = $template
			.clone()
			.removeClass("hide")
			.removeAttr("id")
			.attr("data-recovery-index", recoveryIndex)
			.insertBefore($template);

			$clone
			.find('[name="recovery.runid"]').attr('name', 'recovery[' + recoveryIndex + '].runid').end()
			.find('[name="recovery.lot"]').attr('name', 'recovery[' + recoveryIndex + '].lot').end()
			.find('[name="recovery.pol"]').attr('name', 'recovery[' + recoveryIndex + '].pol').end()
			.find('[name="recovery.ltr"]').attr('name', 'recovery[' + recoveryIndex + '].ltr').end();

			$('.recovery-input-tma').each(function() {

				// Add a different rule to the name field which allows other characters
				if (this.name.indexOf("name") == -1) {
					$(this).rules("add", {
						required: true
					});
				} else {
					$(this).rules("add", {
						required: true
					});
				}
			});
		};

	})()).on("click", ".removeButton", function() {
		var $row = $(this).parents(".form-group").remove();
	});

	function recovery_data_collect_tma() {
		var data_results = {}

		$("#tmaRecoveryForm > div").each(function(index, element) {
			if ($(this).attr("data-recovery-index") != null) {
				data_results[index] = {};
				$(this).children().find("[name]").each(function() {
					var propertyName = $(this).attr("name");
					var propertyValue = $(this).val();
					data_results[index][propertyName] = propertyValue
				});
			}
		});

		var submitter_name = $("#recovery-submitter-tma").val();
		var recovery_filename = $("#recovery-name-input-tma").val();

		data_results["submitter_name"] = submitter_name;
		data_results["recovery_filename"] = recovery_filename;

		var json_data = {
			json: data_results
		};

		return json_data
	}

// <--- Document on load --->
});
