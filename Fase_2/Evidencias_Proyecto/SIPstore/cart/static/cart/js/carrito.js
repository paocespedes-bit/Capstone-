// !Obtener token CSRF (Django)
const getCookie = (name) => {
    const cookie = document.cookie.split(';').find(c => c.trim().startsWith(`${name}=`));
    return cookie ? decodeURIComponent(cookie.split('=')[1]) : null;
};
const csrftoken = getCookie('csrftoken');

// !Formatear valor a moneda chilena
const formatearMoneda = (valor) =>
    new Intl.NumberFormat("es-CL", { style: "currency", currency: "CLP", minimumFractionDigits: 0 })
        .format(valor)
        .replace("CLP", "$");

function truncarNombre(nombre, max = 13) {
  return nombre.length > max ? nombre.substring(0, max - 3) + "..." : nombre;
}

// !Manejar todas las peticiones AJAX del carrito
const manejarPeticionCarrito = async (url, method, data = {}, successCallback) => {
    try {
        const response = await fetch(url, {
            method,
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken,
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) throw new Error(`Error ${response.status}: ${response.statusText}`);

        const result = await response.json();
        if (result.mensaje) mostrarToast(result.mensaje);
        if (result.cantidad_total !== undefined) actualizarBadge(result.cantidad_total);

        successCallback?.(result);
    } catch (error) {
        console.error("Error AJAX:", error);
        mostrarToast(`Error: ${error.message}`);
    }
};

// !Actualizar vistas 
const actualizarVistaCarrito = (data) => {
    const carritoData = data.carrito_data || {};
    const totalEl = document.getElementById("total_sumary");
    const summaryList = document.getElementById("summary-list");
    const checkoutBtn = document.querySelector(".btn-checkout");

    // Actualizar total general
    if (totalEl) totalEl.textContent = formatearMoneda(data.total_carrito || 0);

    // Si el carrito está vacío
    if (Object.keys(carritoData).length === 0) {
        const productosContainer = document.querySelector(".card-body");
        if (productosContainer) {
            productosContainer.innerHTML = '<p class="text-center text-muted">Tu carrito está vacío.</p>';
        }
        if (summaryList) {
            summaryList.innerHTML = `
                <li class="list-group-item d-flex justify-content-between align-items-center bg-light fw-bold border-top border-dark">
                    TOTAL
                    <span class="fs-5" id="total_sumary">$0</span>
                </li>`;
        }
        if (checkoutBtn) checkoutBtn.disabled = true;
        return;
    } else {
        if (checkoutBtn) checkoutBtn.disabled = false;
    }

    //  Actualizar productos en la vista principal 
    Object.entries(carritoData).forEach(([id, item]) => {
        const itemEl = document.querySelector(`.product-item-${id}`);
        if (itemEl) {
            const input = itemEl.querySelector(".cantidad-carrito-input");
            const totalItemEl = itemEl.querySelector(`.total-item-${id}`);
            if (input) input.value = item.cantidad;
            if (totalItemEl) totalItemEl.textContent = `Total: ${formatearMoneda(item.acumulado)}`;
        }
    });

    //  Regenerar el resumen 
    if (summaryList) {
        let html = "";
        const idsOrdenados = Array.from(
            document.querySelectorAll(".productos-en-carrito .product-item") 
        ).map(el => el.querySelector(".cantidad-carrito-input").dataset.id);
        const idsBase = idsOrdenados.length > 0 ? idsOrdenados : Object.keys(carritoData);
        idsBase.forEach(id => {
            const item = carritoData[id];

        if (!item) return; 
            
            html += `
                <li class="list-group-item d-flex justify-content-between bg-light summary-item-${id}">
                    <div style="width: 10vw;" title="${item.nombre}.">${truncarNombre(item.nombre)}</div>
                    <div class="px-3 text-center" style="max-width: 15vw;">
                        <span class="cantidad-summary-${id}">X ${item.cantidad}</span>
                    </div>
                    <div class="ms-3 text-end" style="width: 10vw;">
                        <span class="acumulado-summary-${id}">${formatearMoneda(item.acumulado)}</span>
                    </div>
                </li>`;
        });

        // Línea final de total
        html += `
            <li class="list-group-item d-flex justify-content-between align-items-center bg-light fw-bold border-top border-dark">
                TOTAL
                <span class="fs-5" id="total_sumary">${formatearMoneda(data.total_carrito || 0)}</span>
            </li>`;

        summaryList.innerHTML = html;
    }
};

// !EVENTOS GLOBALES 
document.addEventListener("DOMContentLoaded", () => {

    const obtenerUrlAccion = (accion) => {
        if (typeof urlModificar === "undefined") {
            console.error("Error: urlModificar no está definida en el template HTML.");
            return "";
        }
        return urlModificar.replace("ACCION_PLACEHOLDER", accion);
    };

    // Agregar producto desde la tienda
    document.body.addEventListener("click", (e) => {
        const btn = e.target.closest(".add-btn-ajax");
        if (!btn) return;

        e.preventDefault();
        const { id, ctid, url } = btn.dataset;
        const cantidad = parseInt(btn.closest(".actions")?.querySelector(".cantidad-input")?.textContent || 1);

        manejarPeticionCarrito(url, "POST", { id, ctid, cantidad }, actualizarVistaCarrito);
    });

    // Sumar producto
    document.body.addEventListener("click", (e) => {
        const btn = e.target.closest(".btn-sumar-carrito");
        if (!btn) return;

        e.preventDefault();
        const input = btn.closest(".input-group")?.querySelector(".cantidad-carrito-input");
        if (!input) return;

        const productoId = btn.dataset.id;
        const nuevaCantidad = parseInt(input.value) + 1;
        input.value = nuevaCantidad;

        manejarPeticionCarrito(obtenerUrlAccion("actualizar"), "POST", { producto_id: productoId, cantidad: nuevaCantidad }, actualizarVistaCarrito);
    });

    // Restar producto
    document.body.addEventListener("click", (e) => {
        const btn = e.target.closest(".btn-restar-carrito");
        if (!btn) return;

        e.preventDefault();
        const input = btn.closest(".input-group")?.querySelector(".cantidad-carrito-input");
        if (!input) return;

        const productoId = btn.dataset.id;
        const nuevaCantidad = parseInt(input.value) - 1;

        if (nuevaCantidad > 0) {
            input.value = nuevaCantidad;
            manejarPeticionCarrito(obtenerUrlAccion("actualizar"), "POST", { producto_id: productoId, cantidad: nuevaCantidad }, actualizarVistaCarrito);
        } else {
            manejarPeticionCarrito(obtenerUrlAccion("eliminar"), "POST", { producto_id: productoId }, actualizarVistaCarrito);
            location.reload();
        }
    });

    // Eliminar producto
    document.body.addEventListener("click", (e) => {
        const btn = e.target.closest(".btn-eliminar-carrito");
        if (!btn) return;

        e.preventDefault();
        manejarPeticionCarrito(obtenerUrlAccion("eliminar"), "POST", { producto_id: btn.dataset.id }, actualizarVistaCarrito);
        location.reload();
    });

    // Vaciar carrito
    document.body.addEventListener("click", (e) => {
        const btn = e.target.closest(".btn-limpiar-carrito");
        if (!btn) return;

        e.preventDefault();
        manejarPeticionCarrito(obtenerUrlAccion("limpiar"), "POST", {}, () => {
            actualizarVistaCarrito({ total_carrito: 0, carrito_data: {} });
        });
    });

    // Cambiar cantidad manualmente
    document.body.addEventListener("change", (e) => {
        const input = e.target.closest(".cantidad-carrito-input");
        if (!input) return;

        const productoId = input.dataset.id;
        let nuevaCantidad = parseInt(input.value);
        if (isNaN(nuevaCantidad) || nuevaCantidad < 1) nuevaCantidad = 1;
        input.value = nuevaCantidad;

        manejarPeticionCarrito(obtenerUrlAccion("actualizar"), "POST", { producto_id: productoId, cantidad: nuevaCantidad }, actualizarVistaCarrito);
    });
});