// Uses typed.js to write out a terminal message
$(function() {
	$("#typedJSContainer").typed({
		strings: ["Welcome to the Bioinformatics Homepage <br/> What would you like to do today?"],
		typeSpeed: 0,
		backDelay: 300,
		showCursor: true,
		cursorChar: "_"
		});
	});

$('#nav').affix({
      offset: {
        top: $('.full').height()
      }
});	

$("#gotointro").on("click",function(event) {
  if (this.hash !== "")
  {
    event.preventDefault();
    // Store the Hash
    var hash = this.hash;

    $('html, body').animate(
      {
        scrollTop: $(hash).offset().top
      }, 800, function() {
        // Add hash (#) to URL when done scrolling (default click behavior)
        window.location.hash = hash;
      });
  }
});
