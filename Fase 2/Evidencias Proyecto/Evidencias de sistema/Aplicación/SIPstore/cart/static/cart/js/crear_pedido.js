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
            if (data.ok) {
                window.location.href = data.redirect;
            } else {
                alert(data.error || "Error al guardar el pedido");
            }
        })
        .catch(error => console.error("❌ Error en fetch:", error));
    });
});