document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('btn-finish-order').addEventListener('click', function() {
        const form = document.getElementById('pedidoForm');
        const formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if(data.success){
                window.location.href = `/pago_pendiente/${data.pedido_id}/`;
            } else {
                alert("Error al guardar el pedido");
            }
        })
        .catch(error => console.error(error));
    });
});
