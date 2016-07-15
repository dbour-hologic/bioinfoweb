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
				refreshTables();
				biomatcherRun(response);
			}
		})

		event.preventDefault();
	})


	/* Refresh Tables
	
			Helps clear the table per ajax request to add only new data
			instead of keeping the old.

	*/
	function refreshTables() {

		$("#biomatcher-data-table").html("<table id='biomatcher-data-table'><tr><th>Subject ID</th><th>Oligo Name</th><th>Mismatch Tolerance</th><th>Hit Coordinates</th></tr></table>");
	}

	function biomatcherRun(big_data) {
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
							console.log("ALL",Object.keys(OLIGO_OBJ_NAME[OLIGO_NAME].sub_sequences));
							console.log("OLIGO NAME", OLIGO_NAME)
							console.log("PATTERN", PATTERN_SEQUENCE)
							console.log("SUBJECT FULL SEQ", SUBJECT_SEQUENCE)
							console.log("TOLERANCE", TOLERANCE)
							console.log("SUBJECT ID", SUBJECT_ID)
							console.log("SEQ MATCHED", SUBJECT_MATCHED_SEQUENCE)
							console.log(OLIGO_OBJ_NAME[OLIGO_NAME].hit_coordinates.join([separator='|']))
							var hitCoords = OLIGO_OBJ_NAME[OLIGO_NAME].hit_coordinates.join([separator='|'])

							addingDataToTable(SUBJECT_ID, OLIGO_NAME, TOLERANCE, hitCoords, PATTERN_SEQUENCE, SUBJECT_MATCHED_SEQUENCE, strain_index)
						}
					}
				}
			}
		}
	}

	/* addingDataToTable

	Serves to add the table in a systematic way.
	
	Args:
		subjectID - the subject id being queried against the pattern
		oligoName - the oligo pattern that matches to subject
		mismatchTolerance - the tolerance level set
		hitCoords - the start and end positions of hits
		iteration - the run number, used for assigning different id numbers

	*/

	function addingDataToTable(subjectID, oligoName, mismatchTolerance, hitCoords, patternSeq, subjectSeq, iteration) {
		var assign_subjectID = subjectID;
		var assign_oligoName = oligoName;
		var assign_mismatch = mismatchTolerance;
		var assign_hitCoords = hitCoords;
		var assign_patternSeq = patternSeq;
		var assign_subjectSeq = subjectSeq;

		var topSeq = "seq-top" + iteration;
		var midSeq = "seq-mid" + iteration;
		var botSeq = "seq-bot" + iteration;

		var topSeqDiv = "<div id=" + "'" + topSeq + "'></div>";
		var midSeqDiv = "<div id=" + "'" + midSeq + "'></div>";
		var botSeqDiv = "<div id=" + "'" + botSeq + "'></div>";
		var assign_allSeq = topSeqDiv + midSeqDiv + botSeqDiv;

		$("#biomatcher-data-table").append('<tr><td>' + assign_subjectID + '</td>' +
																			     '<td>' + assign_oligoName + '</td>' +
																			     '<td>' + assign_mismatch  + '</td>' +
																			     '<td>' + assign_hitCoords + '</td>' +
																			     '<td>' + assign_allSeq		 + '</td>'
		)

		// NOTE: 7/15/2016 - Feature temporarily disabled as need to figure out
		// how to deal with the case of multiple sub sequences matching and displaying this.
		// seqAligner(assign_patternSeq, assign_subjectSeq, topSeq, midSeq, botSeq);

	}


	/* seqAligner

	SeqAligner is used for display purposes of the DNA/RNA sequence.
	Sequences that match perfectly will be notated with a '|' character
	while non-perfect matches will be notated with a blank colored space.

	Args:
		pattern_seq - The pattern sequence 
		subject_seq - The subject sequence
		topID - pattern sequence ID
		midID - alignment notation ID
		botID - bottom sequence ID

	*/
	function seqAligner(pattern_seq, subject_seq, topID, midID, botID) {
		var patternArray = pattern_seq.split('');
		var subjectArray = subject_seq.split('');
		for (var index = 0; index < patternArray.length; index++) {
			var patternCode = "<span class='styleGuide'>" + patternArray[index] + "</span>";
			var subjectCode = "<span class='styleGuide'>" + subjectArray[index] + "</span>";

			var topSeqID = "#" + topID;
			var midSeqID = "#" + midID;
			var botSeqID = "#" + botID;

			$(topSeqID).append(patternCode);
			$(botSeqID).append(subjectCode);
			if (patternArray[index] == subjectArray[index]) {
				var midCode = "<span class='styleGuide'>" + "|" + "</span>";
			} else {
				var midCode = "<span class='styleGuide'>" + "<div class='blockYellow'>&nbsp</div>" + "</span>";
			}
			$(midSeqID).append(midCode);

		}
	}

})


