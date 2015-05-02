$( ".event-type select" ).on('change', function() {
  console.log( this.value );
  if (this.value == "string_match") {
  	$( ".response" ).hide();
  	$( ".string" ).css( "display" , "inline-block" );
  } else {
  	$( ".response" ).css( "display" , "inline-block" );
  	$( ".string" ).hide()
  }
});