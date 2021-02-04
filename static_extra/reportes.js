$(document).on("ready", function(){
	function fillDetail(ids){
		//console.log(">", ids);
		var u = {'rows': []};
		for(var i = 0; ids.length > i; i++) {

			var o = _alldata[ids[i]];
			u['rows'].push({
				'CENTRO': o[0],
				'AREA': o[1],
				'CODSERVICIO': o[2],
				'SERVICIO': o[3],
				'ESTACION_ENFERMERIA': o[4],
				'HABITACION': o[5],
				'CAMA': o[6],
				'ESTADO_CAMA': o[7],
				'TIPOCAMA': o[8],
				'DNI': o[9],
				'PACIENTE': o[10],
				'FECHAACTUAL': o[11],
				'CODESTACION': o[12],				
			});
		}
		var template = "{{#rows}}<tr>"+
			"<td>{{AREA}}</td>" +
			"<td>{{SERVICIO}}</td>" +
			"<td>{{ESTACION_ENFERMERIA}}</td>" +
			"<td>{{HABITACION}}</td>" +
			"<td>{{CAMA}}</td>" +
			"<td>{{ESTADO_CAMA}}</td>" +
			"<td>{{TIPOCAMA}}</td>" +
			"<td>{{DNI}}</td>" +
			"<td>{{PACIENTE}}</td>" +
			"<td>{{FECHAACTUAL}}</td>" +
			"</tr>{{/rows}}";
		var text = Mustache.render(template, u);
		$("#full-detail tbody").html(text);
	}
	function fillData(_da) {
	  var data = _da;
	  var template = "{{#Estaciones}}<tr><td>{{text}}</td>" + 
	  	"<td>{{data.available}} <a data-more='{{data.amore}}' " +
	  	"href='#' style='float: right; color: white' " + 
	  	" class='btn btn-info'>Ver</a></td><td>{{data.unable}} "+
	  	"<a data-more='{{data.umore}}' style='float: right; color: white' "+
	  	"class='btn btn-info'>Ver</a>"+
	  	"</td><td>{{data.total}}</td></tr>{{/Estaciones}}";
	  var text = Mustache.render(template, data);
	  //console.log(_da);
	  $("#detail tbody").html(text).promise().done(function() {
		$(".btn-info").on("click", function(){
			var $this = $(this);
			var ids = "" + $this.data("more");
			var _ids = ids.split(",");
			fillDetail(_ids);
		});
	  });

	}

	$("#td_input_qty").on("change", function(){
	  var val = $("#td_input_qty").val(); 
	  if (val !== "-") {
	    fillData(_data[val]);
	  }
	});

});