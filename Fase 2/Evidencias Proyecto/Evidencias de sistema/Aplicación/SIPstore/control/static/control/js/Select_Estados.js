// Select_Estados.js
// Maneja el cambio de color dinámico en el selector de estados de los pedidos

document.addEventListener("DOMContentLoaded", () => {
    const selects = document.querySelectorAll(".estado-select");

    selects.forEach(select => {
        // Aplica el color correspondiente al estado inicial
        actualizarColor(select, select.value);

        // Cuando se cambie el valor, actualiza el color visualmente
        select.addEventListener("change", () => {
            actualizarColor(select, select.value);
            // Enviar el formulario automáticamente al cambiar
            select.form.submit();
        });
    });

    function actualizarColor(select, value) {
        // Elimina todas las clases de color
        select.classList.remove(
            "estado-pendiente",
            "estado-proceso",
            "estado-completado",
            "estado-cancelado",
            "estado-default"
        );

        // Aplica la clase según el valor actual
        if (value === "pendiente") select.classList.add("estado-pendiente");
        else if (value === "en_proceso") select.classList.add("estado-proceso");
        else if (value === "completado") select.classList.add("estado-completado");
        else if (value === "cancelado") select.classList.add("estado-cancelado");
        else select.classList.add("estado-default");
    }
});