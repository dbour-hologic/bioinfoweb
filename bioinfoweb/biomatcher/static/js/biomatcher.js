$(document).ready(function() {

	$('#id_file_upload_selection').click(function(){
		var item = $('#id_file_upload_selection').val();
		$('#hidden-database-selection').val(item);
	});

	$('#run-biomatcher').submit(function(event) {

		$('#submit-form').attr('disabled', true);

		var biomatcher_data = {
				minimum_total_hits: $('#id_minimum_total_hits').val(),
				maximum_total_hits: $('#id_maximum_total_hits').val(),
				max_mismatches_allowed: $('#id_max_mismatches_allowed').val(),
				patterns: $('#id_patterns').val(),
				database_selection_hidden: $('#hidden-database-selection').val(),
				csrfmiddlewaretoken: '{{ csrf_token }}'
		};

		$.ajax({

			url: "/biomatcher/run/",
			type: "POST",
			cache: false,
			dataType: "json",
			data: JSON.stringify(biomatcher_data),
			complete: function() {
				$('#submit-form').removeAttr('disabled');
			},
			success: function (response) {
				refreshTables();
				biomatcherRun(response);
			}
		});

		event.preventDefault();
	});


	/* Refresh Tables
	
			Helps clear the table per ajax request to add only new data
			instead of keeping the old.

	*/
	function refreshTables() {

		$("#biomatcher-data-table").html("<table id='biomatcher-data-table' class='table table-striped'><tr><th>Subject ID</th><th>Oligo Name</th><th>Oligo Seq</th><th>Mismatch Tolerance</th><th>Hit Coordinates</th></tr></table>");
	}

	function biomatcherRun(big_data) {
		var dataPoints = big_data;
		for (strain_index = 0; strain_index < dataPoints.length; strain_index++) {
			// Get the specific STRAIN NAME
			var STRAIN_OBJ_NAME = dataPoints[strain_index];
			// 'Loop' once to get the first & only key
			for (STRAIN_STRING_NAME in STRAIN_OBJ_NAME) {
				// Get list of OLIGOS
				var OLIGO_LIST = STRAIN_OBJ_NAME[STRAIN_STRING_NAME];
				// Iterates the length of the LIST objects (OLIGO_LIST) | INDEX
				for (object_index = 0; object_index < OLIGO_LIST.length; object_index++) {
					// Get the specific OLIGO NAME
					var OLIGO_OBJ_NAME = OLIGO_LIST[object_index];

					// Loop to get the OLIGO names (keys)
					for (var OLIGO_NAME in OLIGO_OBJ_NAME) {
						var PATTERN_SEQUENCE = OLIGO_OBJ_NAME[OLIGO_NAME].pattern_sequence;
						var SUBJECT_SEQUENCE = OLIGO_OBJ_NAME[OLIGO_NAME].subj_sequence;
						var TOLERANCE = OLIGO_OBJ_NAME[OLIGO_NAME].tolerance;
						var SUBJECT_ID = OLIGO_OBJ_NAME[OLIGO_NAME].subject_id;
						if (OLIGO_OBJ_NAME[OLIGO_NAME].total_hits != 0) {
							var SUBJECT_MATCHED_SEQUENCE = OLIGO_OBJ_NAME[OLIGO_NAME].sub_sequences;
							var hitCoords = OLIGO_OBJ_NAME[OLIGO_NAME].hit_coordinates.join([separator='<br>']);

							addingDataToTable(SUBJECT_ID, OLIGO_NAME, TOLERANCE, hitCoords, PATTERN_SEQUENCE, SUBJECT_MATCHED_SEQUENCE, strain_index, SUBJECT_SEQUENCE);
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

	function addingDataToTable(subjectID, oligoName, mismatchTolerance, hitCoords, patternSeq, subjectSeq, iteration, fullSeq) {
		var assign_subjectID = subjectID;
		var assign_oligoName = oligoName;
		var assign_mismatch = mismatchTolerance;
		var assign_hitCoords = hitCoords;
		var assign_patternSeq = patternSeq;
		var assign_subjectSeq = subjectSeq;
		var assign_fullSubSeq = fullSeq;

		// Remove invalid characters in html ID creation
		var reg_remove_special = /[\.()\s+\+]/g;
		var new_subject_id = subjectID.replace(reg_remove_special,"");
		var new_oligo_id = oligoName.replace(reg_remove_special,"");

		var subseq_table_id = new_subject_id + "-" + new_oligo_id + "-" + iteration;
		var subseq_table_html = "<div id='" + subseq_table_id + "'></div>";

		$("#biomatcher-data-table").append('<tr><td>' + assign_subjectID + '</td>' +
											   '<td>' + assign_oligoName + '</td>' +
											   '<td>' + assign_patternSeq + '</td>' +
										       '<td>' + assign_mismatch  + '</td>' +
										       '<td>' + assign_hitCoords + '</td>' +
										       '<tr><td colspan="5">' + subseq_table_html + '</td></tr>'
		)

		// Appends all patterns to subseq_table_html using subseq_table_id
		generateSubPatterns(subjectSeq, subseq_table_id, patternSeq);

	}

	/* generateSubPatterns

	Serves to parse out all the patterns that hit per subject and create 
	a visual display of the matches.
	
	Args:
		arrayOfSubSequences - the hash of all sub sequence match (key) and the hit coordinates (values)
		oligoIdIteration - the ID of the subject table that corresponds to each oligo set
		seqPattern - pattern/oligonucleotide sequence 

	*/
	function generateSubPatterns(arrayOfSubSequences, oligoIdIteration, seqPattern) {
		
		var count = 0;

		for (key in arrayOfSubSequences) {

			var topSeq = "seq-top" + count + "-" + oligoIdIteration;
			var midSeq = "seq-mid" + count + "-" + oligoIdIteration;
			var botSeq = "seq-bot" + count + "-" + oligoIdIteration;

			var topSeqDiv = "<div id=" + "'" + topSeq + "'></div>";
			var midSeqDiv = "<div id=" + "'" + midSeq + "'></div>";
			var botSeqDiv = "<div id=" + "'" + botSeq + "'></div>";
			var hitCounts = "<div>" + "Match (Start, Stop): " + arrayOfSubSequences[key].join([separator=' | ']) + "</div>";

			var assign_allSeq = topSeqDiv + midSeqDiv + botSeqDiv + hitCounts + "<hr>";
			var createID = "#" + oligoIdIteration;
			$(createID).append(assign_allSeq);
			seqAligner(seqPattern, key, topSeq, midSeq, botSeq);
			count = count + 1;
		}
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

		for (index = 0; index < patternArray.length; index++) {
			var patternCode = "<span class='styleGuide'>" + patternArray[index] + "</span>";
			var subjectCode = "<span class='styleGuide'>" + subjectArray[index] + "</span>";

			var topSeqID = "#" + topID;
			var midSeqID = "#" + midID;
			var botSeqID = "#" + botID;

			$(topSeqID).append(patternCode);
			$(botSeqID).append(subjectCode);
			if (isSameBase(patternArray[index], subjectArray[index])) 
			{
				var midCode = "<span class='styleGuide'>" + "|" + "</span>";
			} else {
				var midCode = "<span class='styleGuide'>" + "<div class='blockYellow'>&nbsp</div>" + "</span>";
			}
			$(midSeqID).append(midCode);

		}
	}

	/* isSameBase

	Helps with matching base pairs with its degenerate pair.

	Args:
		pattern_seq - The single pattern sequence base
		subject_seq - The single subject sequence base
	Returns
		true or false depending on if the bases match or not

	*/
	function isSameBase(patternBase, subjectBase) {

		var IUPAC = {
		        "A" : ["A"], 
		        "C" : ["C"], 
		        "G" : ["G"],        
		        "T" : ["T","U"],        
		        "U" : ["U","T"],        
		        "R" : ["G", "A"], 
		        "Y" : ["T", "C"], 
		        "K" : ["G", "T"], 
		        "M" : ["A", "C"], 
		        "S" : ["G", "C"], 
		        "W" : ["A", "T"], 
		        "B" : ["C", "G", "T"], 
		        "D" : ["A", "G", "T"], 
		        "H" : ["A", "C", "T"], 
		        "V" : ["A", "C", "G"], 
		        "N" : ["A", "C", "G", "T"]
		};

		var firstBase = IUPAC[patternBase];
		var secondBase = IUPAC[subjectBase];

		for (baseOne in firstBase) {
			for (baseTwo in secondBase) {
				if (firstBase[baseOne] == secondBase[baseTwo]) {
					return true;
				}
			}
		}
		return false;
	}

})


