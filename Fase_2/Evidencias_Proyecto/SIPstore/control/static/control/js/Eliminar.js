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

document.addEventListener("DOMContentLoaded", function () {
    const btnsEditarKit = document.querySelectorAll(".btn-editar-kit");
    const formEditarKit = document.getElementById("formEditarKit");

    btnsEditarKit.forEach(btn => {
        btn.addEventListener("click", () => {
            const id = btn.getAttribute("data-id");
            const nombre = btn.getAttribute("data-nombre");
            const precio = btn.getAttribute("data-precio");
            const descripcion = btn.getAttribute("data-descripcion");
            const m2 = btn.getAttribute("data-m2");
            const dormitorios = btn.getAttribute("data-dormitorios");
            const banos = btn.getAttribute("data-banos");
            const categorias = btn.getAttribute("data-categorias").split(",");

            // Actualizar action del formulario
            formEditarKit.action = "/editar-kit/" + id + "/";

            // Llenar campos del form
            document.getElementById("id_nombre").value = nombre;
            document.getElementById("id_precio").value = precio;
            document.getElementById("id_descripcion").value = descripcion;
            document.getElementById("id_m2").value = m2;
            document.getElementById("id_dormitorios").value = dormitorios;
            document.getElementById("id_banos").value = banos;

            // Resetear checkboxes y marcar los correctos
            const checkboxes = formEditarKit.querySelectorAll("input[name='categorias']");
            checkboxes.forEach(cb => {
                cb.checked = categorias.includes(cb.value);
            });
        });
    });
});