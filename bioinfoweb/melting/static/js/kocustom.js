// Using KO to create an interactive wrapper for the Melting 5 program made in JAVA
// David Bour, 2015 08 24
// Code inspired by IDT Oligo Analyzer 
// *** Melting 5 - http://www.ebi.ac.uk/compneur-srv/melting/


// Function below restricts input to specific nucleotides only && counts character
$(document).ready(function() {
	$("#seq").on('change keyup paste', function() {
		var $th = $(this);

		$th.val($th.val().toUpperCase().replace(/[^ATCGIatcgi]/g, function(){ return '';}) );

		// Gets character count on the field
		var len = $th.val().length;
		$("#charCount").text(len);


	});

	$("#oligoConc").on('change keyup paste', function() {
		var $th = $(this);
		$th.val($th.val().replace(/[^\d+\.]/g, function(){return '';}) );
	});

	$("#sodiumConc").on('change keyup paste', function() {
		var $th = $(this);
		$th.val($th.val().replace(/[^\d+\.]/g, function(){return '';}) );
	});

	$("#magConc").on('change keyup paste', function() {
		var $th = $(this);
		$th.val($th.val().replace(/[^\d+\.]/g, function(){return '';}) );
	});		

});

$(document).ready(function() {

	// jQuery CSRF_TOKEN 


	// 5'-3' constructor
	function bases(base) {

		var self = this;
		self.originalBase = base;

	};

	// Get the complement of the original base
	bases.prototype.complementBase = function() {

		var comparison = this.originalBase;

		if (comparison === "A") {
			return "T";
		} else if (comparison ==="T") {
			return "A";
		} else if (comparison === "C") {
			return "G";
		} else if (comparison === "G") {
			return "C";
		}

	};

	// 3'-5' constructor
	function compFactory(comBase, index) {

		var self = this;
		self.compBase = ko.observable(comBase); 
		self.originalBase = comBase; // Hold for comparison
		self.index = index; // Allows for checking of neighbors in array
		self.isGap = 0; // 0 -- not gap | 1 -- is gap --- Allow for tandem gaps
		self.currentBase = comBase;
		self.isVisible = ko.observable(false); // Hides | Show base after clicking select base


	};

	// ______ View Model _______ //
	function meltViewModel() {

		var self = this;

		// Initialize observal arrays for the input sequences
		self.seqArray = ko.observableArray([]); // Holds the 5'-3' sequence.
		self.comArray = ko.observableArray([]); // Holds the 3'-5' complementary sequence.

		// Clears array when the "CLEAR" button is hit
		self.clearArray = function() {
			self.seqArray.removeAll();
			self.comArray.removeAll();

		}

		// Reads in sequence from input form and inserts into the seqArray & comArray
		self.readArray = function() {

			// Clear array if user re-submits
			self.seqArray.removeAll();
			self.comArray.removeAll();

			var sequences = $("#seq").val().split("");
			for (var i=0; i<sequences.length; i++) {

				var firstStrand = new bases(sequences[i]);
				var secondStrand = new compFactory(firstStrand.complementBase(), i);
				self.seqArray.push(firstStrand); // 5'-3' sequence
				self.comArray.push(secondStrand); // 3'-5' sequence

			}

		}

		// Available options to select from
		self.selectBase = [
			{ basePair: "A"},
			{ basePair: "T"},
			{ basePair: "C"},
			{ basePair: "G"},
			{ basePair: "-"}
		]


		// Function to show select option
		self.openList = function() {

			var startpoint = 0;
			var endpoint = self.comArray().length -1;
			var leftpos = self.comArray()[this.index-1];
			var rightpos = self.comArray()[this.index+1];
			var currentpos = self.comArray()[this.index];



			// Disable end point modifications on extreme 5' or 3'



			if (this.index === startpoint || this.index === endpoint) 
			{
				alert("No terminal mismatches allowed.");
				this.isVisible(false);
			} 


			else 
			{
				this.isVisible(true);
			}


		}



		// Function to check if selection is different from original base
		self.modCheck = function() {

			// Checks neighbors for allowed mismatches
			if (this.compBase() != this.originalBase && this.compBase() === "-" ) 
			{
		

					if (   self.comArray()[this.index+1].compBase() != self.comArray()[this.index+1].originalBase 
						&& self.comArray()[this.index+1].compBase() != "-" ||
						   self.comArray()[this.index-1].compBase() != self.comArray()[this.index-1].originalBase
						&& self.comArray()[this.index-1].compBase() != "-" 
					   ) 
					{
						
						self.comArray()[this.index].compBase(this.currentBase);
						alert("No gaps next to mismatches allowed");
						this.isVisible(false);


					}



			} else if (this.compBase() != this.originalBase && this.compBase() != "-") {

		
				
					if (   self.comArray()[this.index+1].compBase() != self.comArray()[this.index+1].originalBase  ||
						   self.comArray()[this.index-1].compBase() != self.comArray()[this.index-1].originalBase
					   ) 
					{
						
						self.comArray()[this.index].compBase(this.currentBase);
						alert("No tandem mismatch allowed or gaps next to mistmaches allowed");
						this.isVisible(false);
					}
				

			} 
			else
 			{
				this.modified = 0;
				this.currentBase = this.compBase();
			
			}
		}

		self.save = function() {

			// Checks if ion/oligo parameters are filled & displays appropriate warnings
			check();

			var cusJSON = {"attributes": [
						   {"name": $('#oligoConc').attr('name'), "value":$('#oligoConc').val()},
						   {"name": $('#hybridType').attr('name'), "value": $('#hybridType').val()},
					       {"name": $('#sodiumConc').attr('name'), "value": $('#sodiumConc').val()},
						   {"name": $('#magConc').attr('name'), "value": $('#magConc').val()}
						   ]};

			$.ajax({
				url: "/ajaxresponse/",
				type: "POST",
				dataType: 'json',
				data: {
					propertiesArray: JSON.stringify(cusJSON),
					koArray: ko.toJSON(self),
					csrfmiddlewaretoken: '{{ csrf_token }}'
				},
				success: function (response) {
					dataDict = response.finalData.results
					$("#tm").text(dataDict.TM);
					$("#enthalpy_result").text(dataDict.ENTHALPY);
					$("#entropy_result").text(dataDict.ENTROPY);
					$("#message").text(dataDict.MESSAGE);
					$("#status").text(dataDict.STATUS);
				}
			})
		}

	}

	// ___ Unit Testers ___ //

	function seeAll(giveMeObj) {
		for (var key in giveMeObj) {
			console.log(key + " " + giveMeObj[key]);
		}
	};

	// *** Test bases constructor
	var tBase = new bases("C");
	//seeAll(tBase);
	//console.log(tBase.complementBase());

	// *** Test compFactory constructor
	var cBase = new compFactory("A", 1);
	//seeAll(cBase);


	ko.applyBindings(new meltViewModel());

});




// Functions for the Bioinformatics Workspace - Tools Page
// Below is used for display purposes of the Melting Fields
$(document).ready(function() {

	$("#clear").click(function()
	{
		var elem = document.getElementById("seq");
		elem.value = "";

		$("#charCount").empty();

		var oligoElem = document.getElementById("oligoConc");
		var sodiumConc = document.getElementById("sodiumConc");
		var magConc = document.getElementById("magConc");

		oligoElem.value = "";
		sodiumConc.value = "";
		magConc.value = "";

		// Clears Results
		var resultID = ["#status", "#message", "#enthalpy_result",
						"#entropy_result", "#tm"]

		for (var x in resultID) {
			$(resultID[x]).empty();
		}

		// Clears Errors
		var errorID = ["#oligoError", "#sodiumError", "#magError"]

		for (var err in errorID) {
			$(errorID[err]).empty();
		}

	});

});

// Function to check if all necessary inputs are there

function check() {

	if ($("#oligoConc").val() == '') {
		$("#oligoError").text("Enter a value!");
	} else {
		$("#oligoError").empty();
	}

	if ($("#sodiumConc").val() == '') {
		$("#sodiumError").text("Enter a value!");
	} else {
		$("#sodiumError").empty();
	}

	if ($("#magConc").val() == '') {
		$("#magError").text("Enter a value!");
	} else {
		$("#magError").empty();
	}
	
};



// Warning labels for some of the hybridization modes
$(document).ready(function() {
	$("#hybridType").change(function() {
		var $th = $(this);
		if ($th.val() === 'mrnarna') {
			$("#warningLabel").empty();
			$("#warningLabel").append("<b>Note:</b> this method does not allow mismatches at all.");
		} else if ($th.val() === 'rnadna' || $th.val() === 'rnarna' || $th.val() === 'dnarna') {
			$("#warningLabel").empty();
			$("#warningLabel").append("<b>Note:</b> this method may not allow certain mismatches/gaps.")
		} else {
			$("#warningLabel").empty();
		}
	});
})

// // On keyup, auto draw
// $(document).ready(function() {



// })