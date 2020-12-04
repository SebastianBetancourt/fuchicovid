let revisar_tope_medicamento = function(){
    const reservas = JSON.parse(document.getElementById('reservas_objs').textContent);
    select_medicamento = document.getElementById("laboratorio")
    laboratorio = select_medicamento[select_medicamento.selectedIndex].text
    select_medicamento = document.getElementById("medicamento")
    medicamento = select_medicamento.options[select_medicamento.selectedIndex].value
    reserva = reservas.find(e => e.laboratorio ==  laboratorio && e.medicamento_id == medicamento);
    input_cantidad = document.getElementById("cantidad")
    if(reserva !== undefined){
        if(input_cantidad.value > reserva.cantidad){
            input_cantidad.value = reserva.cantidad
        }
        document.getElementById("cantidad").max = reserva.cantidad;
    }
}

document.getElementById("laboratorio").onchange = revisar_tope_medicamento;
document.getElementById("medicamento").onchange = revisar_tope_medicamento;
revisar_tope_medicamento();