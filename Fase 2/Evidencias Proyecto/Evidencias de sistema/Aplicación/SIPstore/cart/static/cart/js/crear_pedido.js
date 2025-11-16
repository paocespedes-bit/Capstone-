document.addEventListener('DOMContentLoaded', function() {

    document.getElementById('btn-finish-order').addEventListener('click', function(event) {
        event.preventDefault();   // ⬅️ EVITA EL SUBMIT REAL DEL FORMULARIO

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

            // ❌ MUESTRA ERROR EN ALERT, NO REDIRIGE
            if (!data.ok) {
                alert(data.error || "Error al guardar el pedido");
                return;  // ⬅️ IMPORTANTE: DETENER LA EJECUCIÓN
            }

            // ✔️ SI TODO CORRECTO → REDIRIGIR
            window.location.href = data.redirect;
        })
        .catch(error => console.error("❌ Error en fetch:", error));
    });

});
