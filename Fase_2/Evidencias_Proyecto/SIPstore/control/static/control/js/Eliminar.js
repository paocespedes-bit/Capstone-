document.addEventListener("DOMContentLoaded", function () {

    const modalEliminar = document.getElementById('modalEliminar');

    // 🚨 Importante: Verificar si el modal existe antes de intentar añadir listeners
    if (modalEliminar) {
        modalEliminar.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            // Si el botón no existe o no tiene atributos, salimos
            if (!button) return; 

            const url = button.getAttribute('data-url');
            const nombre = button.getAttribute('data-nombre');
            const tipo = button.getAttribute('data-tipo');

            // Cambiar el texto en el modal
            const modalText = document.getElementById('modalTextEliminar');
            if (modalText) {
                modalText.textContent = `¿Estás seguro de eliminar ${tipo} "${nombre}"?`;
            }

            // Cambiar la acción del formulario
            const form = document.getElementById('formEliminar');
            if (form) {
                form.action = url;
            }
        });
    }

    const btnsEditarKit = document.querySelectorAll(".btn-editar-kit");
    const formEditarKit = document.getElementById("formEditarKit");

    // Solo ejecutamos si encontramos botones y el formulario de edición
    if (btnsEditarKit.length > 0 && formEditarKit) {
        btnsEditarKit.forEach(btn => {
            btn.addEventListener("click", () => {
                const id = btn.getAttribute("data-id");
                const nombre = btn.getAttribute("data-nombre");
                const precio = btn.getAttribute("data-precio");
                const descripcion = btn.getAttribute("data-descripcion");
                const m2 = btn.getAttribute("data-m2");
                const dormitorios = btn.getAttribute("data-dormitorios");
                const banos = btn.getAttribute("data-banos");
                
                // Aseguramos que data-categorias sea una cadena antes de dividir, si no está definido, usamos una cadena vacía
                const categoriasAttr = btn.getAttribute("data-categorias") || "";
                const categorias = categoriasAttr.split(",");

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
    }
});