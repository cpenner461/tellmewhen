$( ".event-type select" ).on('change', function() {
  console.log( this.value );
  if (this.value == "string_match" || this.value == "regex_match") {
  	$( ".response" ).hide();
  	$( ".string" ).css( "display" , "inline-block" );
  } else {
  	$( ".response" ).css( "display" , "inline-block" );
  	$( ".string" ).hide()
  }
});

$( ".frequency select" ).on('change', function () {
	if (this.value == "1") {
		$( ".frequency + li" ).text("second");
	} else {
		$( ".frequency + li" ).text("seconds");
	}
});

$( ".num_checks select" ).on('change', function () {
	if (this.value == "1") {
		$( ".num_checks + li" ).text("time");
	} else {
		$( ".num_checks + li" ).text("times");
	}
});
