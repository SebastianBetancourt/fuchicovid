const edad_pacientes = JSON.parse(document.getElementById('edad_pacientes_json').textContent);
const pacientes_barrio = JSON.parse(document.getElementById('pacientes_barrio_json').textContent);



new Chart(document.getElementById('pacientes_barrio'), {
    type: 'bar',
    data: {
        labels: pacientes_barrio.barrios,
        datasets: [{
            label: 'Pacientes por barrio',
            backgroundColor: "rgb(244,46,74)",
            data: pacientes_barrio.pacientes,
        }]
    },
    options: {
        responsive: false,
        maintainAspectRatio: false,
        legend: {display: false},
        scales: {
            xAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Barrio'
                  },
                ticks: {
                    beginAtZero: true,
                }
            }],
            yAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Pacientes'
                  },
                ticks: {
                    beginAtZero: true,
                    callback: function(value) {if (value % 1 === 0) {return value;}}
                }
            }]
        }
    }
});
new Chart(document.getElementById('edad_pacientes'), {
    type: 'bar',
    data: {
        labels: edad_pacientes.edad,
        datasets: [{
            backgroundColor: "rgb(249,70,46)",
            data: edad_pacientes.pacientes,
        }]
    },
    options: {
        responsive: false,
        maintainAspectRatio: false,
        legend: {
            display: false},
        scales: {
            xAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Edad'
                  },
                ticks: {
                    beginAtZero: true,
                }
            }],
            yAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Pacientes'
                  },
                ticks: {
                    beginAtZero: true,
                    callback: function(value) {if (value % 1 === 0) {return value;}}
                }
            }]
        }
    }
});
$("#desde").datepicker({ dateFormat: 'yy-mm-dd' });
$("#hasta").datepicker({ dateFormat: 'yy-mm-dd' });
let consultar_visitas = function(url, csrf_token){
    let desde =  $.datepicker.formatDate('yy-mm-dd', $("#desde").datepicker( "getDate" ))
    let hasta = $.datepicker.formatDate('yy-mm-dd', $("#hasta").datepicker( "getDate" ))
    $.ajax({
        type: "POST",
        headers:{
            "X-CSRFToken": csrf_token
        },
        data: {"desde" : desde,
                "hasta" : hasta},
        url: url,
        dataType: "json",
        success: function(msg) {
            $('#resultado_visitas').text("Desde el día "+desde+" hasta el día "+hasta+" se han hecho "+msg.total+" visitas.")
        },
        error: function(msg) {
            console.log("Error consulta en backend");
            console.log(msg);
        }
    });
}