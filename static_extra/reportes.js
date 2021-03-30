function enableSearch() {
	$("#buscar-paciente").on("keyup", function(){
		var ii = [];
		var o = $("#buscar-paciente").val();
		if ( o.length <= 0 ) {

			fillDetail([]);
			return;	
		}
		for (var i = 0; _alldata.length > i; i++) {
			var nombres = _alldata[i][10] || "";
			if ( nombres.toLowerCase().includes(o.toLowerCase()) ) {
				ii.push(i);
			}
		}
		fillDetail(ii);
		//var o = _alldata[ids[i]];
	});
}


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

$(document).on("ready", function(){


	$("#btn-covid").on("click", function(){
	    TableToExcel.convert(document.getElementById("detail"), {
	        name: "Covid-reporte.xlsx",
	        sheet: {
	        name: "reporte-covid"
	        }
	      });
	});
	$("#btn-no-covid").on("click", function(){
	    TableToExcel.convert(document.getElementById("detail"), {
	        name: "Covid-No-reporte.xlsx",
	        sheet: {
	        name: "reporte-no-covid"
	        }
	      });
	});

	function fillData(_da) {
	  var data = _da;
	  var availables = 0;
	  var unables = 0;
	  var totals = 0;
	  for(var i = 0; data['Estaciones'].length > i; i++) {
	  	availables += data['Estaciones'][i].data.available;
	  	unables += data['Estaciones'][i].data.unable;
	  	totals += data['Estaciones'][i].data.total;
	  }
	  var template = "<tr>" + 
		"<td style='display:none' ></td>" +
		"<td></td>" +
		"<td><strong>" + availables + "</strong></td>" +
		"<td data-exclude='true'></td>" +
		"<td><strong>" + unables + "</strong></td>" +
		"<td data-exclude='true'></td>" +
		"<td><strong>" + totals + "</strong></td>" +
		"</tr>" + 
	  	"{{#Estaciones}}<tr>" + 
	  	"<td style='display:none'>{{ _servicio }}</td>"+ 
	  	"<td>{{text}}</td>" + 
	  	"<td>{{data.available}}</td>" + 
	  	"<td data-exclude='true'>" + 
	  	"<a data-more='{{data.amore}}' data-exclude='true' href='#' style='float: right; color: white' " + 
	  	" class='btn btn-info' >Ver</a>" + 
	  	"</td>"+
	  	"<td>{{data.unable}} </td>"+
	  	"<td  data-exclude='true'>" + 
	  	"<a data-more='{{data.umore}}' data-exclude='true' style='float: right; color: white' "+
	  	"class='btn btn-info'>Ver</a>"+
	  	"</td>" + 
	  	"<td>{{data.total}}</td></tr>{{/Estaciones}}";
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
	    if (val === "COVID") {
	    	$("#btn-covid").show();
	    	$("#btn-no-covid").hide();
	    } else if ( val === "NO COVID" ) {
	    	$("#btn-covid").hide();
	    	$("#btn-no-covid").show();
	    } else {
	    	$("#btn-covid").hide();
	    	$("#btn-no-covid").hide();
	    }
	  }

	});
	enableSearch();
});