$(document).on("ready", function(){
	$("#salida_tipo").on("change", function(){
		var val = $("#salida_tipo").val();
		if ( val === "TRAN" ) {
			$("#salida_servicio").show();
		} else {
			$("#salida_servicio").hide();
		}
	});
});