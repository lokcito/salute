$(document).on("ready", function(){
	function fillData(_da) {
		var template = "<option value='-'>-- Seleccione la Estacion -- </option>{{#Estaciones}}<option value='{{text}}'>{{text}}</option>{{/Estaciones}}";

		var tmpl = Mustache.render(template, _da);
		$("#estacion_combo").html(tmpl);

	}
	function getNCamas() {
	  var val = $("#servicio_combo").val();
	  var estacion_val = $("#estacion_combo").val();
	  var hab_val = $("#habitacion_combo").val();

	  if (!val || val === "-") {
	  	return 0;
	  }
	  if ( !estacion_val || estacion_val === "-" ) {
	  	return 0;
	  }
	  if ( !hab_val || hab_val === "-" ) {
	  	return 0;
	  }

   		for(var i = 0; _data[val]['Estaciones'].length > i; i++){
	   		if ( _data[val]['Estaciones'][i].text === estacion_val ) {
		   		var u = _data[val]['Estaciones'][i].data["umore"].split(",");
		   		var a = _data[val]['Estaciones'][i].data["amore"].split(",");
		   		var t = [];
		   		for (var j = 0; u.length > j; j++) {
		   			if ( u[j] )
		   				t.push(u[j]);
		   		}
		   		for (var k = 0; a.length > k; k++) {
		   			if ( a[k] )
		   				t.push(a[k]);
		   		}
		   		var habs = [];
				for(var l = 0; t.length > l; l++) {
					var o = _alldata[t[l]];
					habs.push(o[5]);
				}

				var options_hab = "<option value='-'>- Seleccione Habitacion -</option>";
				var counted = _.countBy(habs);
				if ( hab_val in counted ) {
					return counted[hab_val];
				}
				return 0;
	   		}
	   	}
	  }
	function searchData() {
	  var val = $("#servicio_combo").val();
	  var estacion_val = $("#estacion_combo").val();
	  if (val !== "-") {
	   	for(var i = 0; _data[val]['Estaciones'].length > i; i++){
	   		if ( _data[val]['Estaciones'][i].text === estacion_val ) {
		   		var u = _data[val]['Estaciones'][i].data["umore"].split(",");
		   		var a = _data[val]['Estaciones'][i].data["amore"].split(",");
		   		var t = [];
		   		for (var j = 0; u.length > j; j++) {
		   			if ( u[j] )
		   				t.push(u[j]);
		   		}
		   		for (var k = 0; a.length > k; k++) {
		   			if ( a[k] )
		   				t.push(a[k]);
		   		}
		   		var habs = [];
				for(var l = 0; t.length > l; l++) {
					var o = _alldata[t[l]];
					habs.push(o[5]);
				}

				var options_hab = "<option value='-'>- Seleccione Habitacion -</option>";
				var counted = _.countBy(habs);
				for(var oh in counted) {
					options_hab += "<option value='" + oh + 
						"'>" + oh + " / Camas: " + counted[oh] + "</option>";
				}

				$("#habitacion_combo").html(options_hab);
	   		}
	   	}
	  }
	}
	function cleanBelow(field) {
		if (field === "servicio") {
		  $("#estacion_combo").val("-");
		  $("#habitacion_combo").html("<option value='-'>- Seleccione Habitacion -</option>");
		  $("#habitacion_combo").val("-");
		  $("#inpt_ncama").val(0);
		} else if ( field === "estacion" ) {
			$("#inpt_ncama").val(0);
		}
	}

	$("#servicio_combo").on("change", function(){
	  var val = $("#servicio_combo").val();
	  if (val !== "-") {
	    fillData(_data[val]);
	  }
	 	cleanBelow("servicio");
	});
	$("#estacion_combo").on("change", function(){
		var val = $("#estacion_combo").val();
		searchData();
		cleanBelow("estacion");
	});
	$("#habitacion_combo").on("change", function(){
		var nn = getNCamas();
		$("#inpt_ncama").val(nn);
	});	
	$("#censo_table").DataTable();
});