document.addEventListener("DOMContentLoaded", function () {
    // Inicializar todos los modales existentes
    document.querySelectorAll(".modal").forEach(modalEl => {
        if (modalEl) {
            bootstrap.Modal.getOrCreateInstance(modalEl);
        }
    });

    // Modal de eliminación dinámico
    document.querySelectorAll(".modal").forEach(modalEl => {
        modalEl.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            if (!button) return;

            const url = button.getAttribute('data-url') || '';
            const nombre = button.getAttribute('data-nombre') || '';
            const tipo = button.getAttribute('data-tipo') || '';

            const modalText = modalEl.querySelector('.modal-text-eliminar');
            if (modalText) {
                modalText.textContent = `¿Estás seguro de eliminar ${tipo} "${nombre}"?`;
            }

            const form = modalEl.querySelector('form');
            if (form && url) {
                form.action = url;
            }
        });
    });

    // Edición de Kits dinámica
    const btnsEditarKit = document.querySelectorAll(".btn-editar-kit");
    const formEditarKit = document.getElementById("formEditarKit");

    if (btnsEditarKit.length && formEditarKit) {
        btnsEditarKit.forEach(btn => {
            btn.addEventListener("click", () => {
                const id = btn.getAttribute("data-id") || '';
                const nombre = btn.getAttribute("data-nombre") || '';
                const precio = btn.getAttribute("data-precio") || '';
                const descripcion = btn.getAttribute("data-descripcion") || '';
                const m2 = btn.getAttribute("data-m2") || '';
                const dormitorios = btn.getAttribute("data-dormitorios") || '';
                const banos = btn.getAttribute("data-banos") || '';

                const categoriasAttr = btn.getAttribute("data-categorias") || "";
                const categorias = categoriasAttr.split(",");

                formEditarKit.action = `/editar-kit/${id}/`;

                const fields = ["nombre", "precio", "descripcion", "m2", "dormitorios", "banos"];
                const values = [nombre, precio, descripcion, m2, dormitorios, banos];

                fields.forEach((field, index) => {
                    const input = document.getElementById(`id_${field}`);
                    if (input) input.value = values[index];
                });

                formEditarKit.querySelectorAll("input[name='categorias']").forEach(cb => {
                    cb.checked = categorias.includes(cb.value);
                });
            });
        });
    }
});
