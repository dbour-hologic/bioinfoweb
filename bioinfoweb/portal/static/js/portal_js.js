// Uses typed.js to write out a terminal message
$(function() {
	$("#typedJSContainer").typed({
		strings: ["<b style='font-size: xx-large'>Welcome</b>", 
		"<b style='font-size: xx-large'>Bioinformatics</b> \
		<br/> <em style='font-size: large;'>Core Technolgies Group</em> \
		<br/> \
		<br/> \
		What would you like to do today...?  "],
		typeSpeed: 0,
		backDelay: 300,
		showCursor: true,
		cursorChar: "|"
		});
	});