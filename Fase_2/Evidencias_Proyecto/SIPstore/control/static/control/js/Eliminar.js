document.addEventListener("DOMContentLoaded", function () {
    const modalEliminar = document.getElementById('modalEliminar');

    modalEliminar.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const url = button.getAttribute('data-url');
        const nombre = button.getAttribute('data-nombre');
        const tipo = button.getAttribute('data-tipo');

        // Cambiar el texto en el modal
        document.getElementById('modalTextEliminar').textContent =
            `¿Estás seguro de eliminar ${tipo} "${nombre}"?`;

        // Cambiar la acción del formulario
        document.getElementById('formEliminar').action = url;
    });
});