$(document).ready(function() {

	$('#id_file_upload_selection').click(function(){
		item = $(this).val()
		$('#hidden-database-selection').val(item)
	})

	$('#run-biomatcher').submit(function(event) {

		var biomatcher_data = {
				minimum_total_hits: $('#id_minimum_total_hits').val(),
				maximum_total_hits: $('#id_maximum_total_hits').val(),
				max_mismatches_allowed: $('#id_max_mismatches_allowed').val(),
				patterns: $('#id_patterns').val(),
				database_selection_hidden: $('#hidden-database-selection').val(),
				csrfmiddlewaretoken: '{{ csrf_token }}'
		}

		$.ajax({
			url: "/biomatcher/run/",
			type: "POST",
			dataType: "json",
			data: JSON.stringify(biomatcher_data),
			success: function (response) {
				OKAY(response);
			}
		})

		event.preventDefault();
	})

	function OKAY(big_data) {
		var dataPoints = big_data;
		for (var strain_index = 0; strain_index < dataPoints.length; strain_index++) {
			// Get the specific STRAIN NAME
			var STRAIN_OBJ_NAME = dataPoints[strain_index]
			// 'Loop' once to get the first & only key
			for (var STRAIN_STRING_NAME in STRAIN_OBJ_NAME) {
				// Get list of OLIGOS
				var OLIGO_LIST = STRAIN_OBJ_NAME[STRAIN_STRING_NAME]
				// Iterates the length of the LIST objects (OLIGO_LIST) | INDEX
				for (var object_index = 0; object_index < OLIGO_LIST.length; object_index++) {
					// Get the specific OLIGO NAME
					var OLIGO_OBJ_NAME = OLIGO_LIST[object_index]

					// Loop to get the OLIGO names (keys)
					for (var OLIGO_NAME in OLIGO_OBJ_NAME) {
						var PATTERN_SEQUENCE = OLIGO_OBJ_NAME[OLIGO_NAME].pattern_sequence
						var SUBJECT_SEQUENCE = OLIGO_OBJ_NAME[OLIGO_NAME].subj_sequence
						var TOLERANCE = OLIGO_OBJ_NAME[OLIGO_NAME].tolerance
						var SUBJECT_ID = OLIGO_OBJ_NAME[OLIGO_NAME].subject_id
						if (OLIGO_OBJ_NAME[OLIGO_NAME].total_hits != 0) {
							var SUBJECT_MATCHED_SEQUENCE = Object.keys(OLIGO_OBJ_NAME[OLIGO_NAME].sub_sequences)[0]

							console.log("OLIGO NAME", OLIGO_NAME)
							console.log("PATTERN", PATTERN_SEQUENCE)
							console.log("SUBJECT FULL SEQ", SUBJECT_SEQUENCE)
							console.log("TOLERANCE", TOLERANCE)
							console.log("SUBJECT ID", SUBJECT_ID)
							console.log("SEQ MATCHED", SUBJECT_MATCHED_SEQUENCE)
							console.log(OLIGO_OBJ_NAME[OLIGO_NAME].hit_coordinates.join([separator='|']))
						}
					}
				}
			}
		}
	}

})


