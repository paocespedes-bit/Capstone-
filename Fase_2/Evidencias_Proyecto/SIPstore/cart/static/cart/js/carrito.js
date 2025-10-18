// cart/js/carrito_ajax.js

// Funciones de utilidad AJAX
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie("csrftoken");

// * Mostrar Toast *
function mostrarToast(mensaje) {
  const toastEl = document.getElementById("toast");
  const toastBody = document.getElementById("toast-body");
  if (toastBody && toastEl) {
    toastBody.textContent = mensaje;
    const toast = new bootstrap.Toast(toastEl);
    toast.show();
  }
}

// * Actualizar el badge del carrito *
function actualizarBadge(cantidadTotal) {
  const badge = document.getElementById("contar_carrito");
  if (badge) {
    badge.textContent = cantidadTotal;
  }
}

// * Manejar solicitud AJAX *
function manejarPeticionCarrito(url, method, data, successCallback) {
  fetch(url, {
    method: method,
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Error en la petición: ${response.statusText}`);
      }
      return response.json();
    })
    .then((data) => {
      if (data.mensaje) {
        mostrarToast(data.mensaje);
      }
      actualizarBadge(data.cantidad_total);
      if (successCallback) {
        successCallback(data);
      }
    })
    .catch((error) => {
      mostrarToast(`Error: ${error.message}`);
      console.error("Error AJAX:", error);
    });
}

// * Funcionalidad de las tarjetas (tienda) *
document.addEventListener("DOMContentLoaded", function () {
  // Escucha el evento click para los botones de añadir al carrito en las cards
  document.querySelectorAll(".add-btn-ajax").forEach((button) => {
    button.addEventListener("click", function (e) {
      e.preventDefault();

      const productoId = this.dataset.id;
      const contentTypeId = this.dataset.ctid;
      const url = this.dataset.url; // Obtener la cantidad del span adyacente

      const cantidadSpan =
        this.closest(".actions").querySelector(".cantidad-input");
      const cantidad = parseInt(cantidadSpan ? cantidadSpan.textContent : 1);

      const data = {
        id: productoId,
        ctid: contentTypeId,
        cantidad: cantidad,
      };

      manejarPeticionCarrito(url, "POST", data, (data) => {
        // El badge ya se actualiza.
      });
    });
  });
});

// * Funcionalidad de la vista del carrito (carrito.html) *
if (document.querySelector(".cart")) {
  // ⚠️ Importante: La variable 'urlModificar' debe ser definida globalmente en el HTML
  // Ejemplo en carrito.html: <script>const urlModificar = '{% url "modificar_ajax" "ACCION_PLACEHOLDER" %}';</script>

  // Función auxiliar para obtener la URL correcta
  function obtenerUrlAccion(accion) {
    // Asegúrate de que 'ACCION_PLACEHOLDER' coincida con tu placeholder de Django
    if (typeof urlModificar === "undefined") {
      console.error(
        "Error: 'urlModificar' no está definida en el template HTML."
      );
      return "";
    }
    return urlModificar.replace("ACCION_PLACEHOLDER", accion);
  } // Función para formatear a moneda

  function formatearMoneda(valor) {
    return new Intl.NumberFormat("es-CL", {
      style: "currency",
      currency: "CLP",
      minimumFractionDigits: 0,
    })
      .format(valor)
      .replace("CLP", "$");
  } // Actualiza la lista de productos y el resumen después de una acción

  function actualizarVistaCarrito(data) {
    // * 1. Actualizar Resumen (Summary) *
    const totalFormateado = formatearMoneda(data.total_carrito);
    document.getElementById("subtotal_sumary").textContent = totalFormateado;
    document.getElementById("total_sumary").textContent = totalFormateado; // * 2. Actualizar Listas de Productos *

    const carritoData = data.carrito_data;
    const keysEnCarrito = Object.keys(carritoData);
    const productosContainer = document.querySelector(
      ".productos-carrito-list"
    ); // Asume que tienes un contenedor padre // Iterar sobre los items visibles para ver cuáles eliminar o actualizar

    document.querySelectorAll('[class^="product-item-"]').forEach((itemEl) => {
      const match = itemEl.className.match(/product-item-(\d+)/);
      if (!match) return; // Si no hay match, salta este elemento

      const itemId = match[1];

      if (keysEnCarrito.includes(itemId)) {
        // Producto existe: actualizar sus valores
        const item = carritoData[itemId];
        const acumuladoFormateado = formatearMoneda(item.acumulado);

        itemEl.querySelector(".cantidad-carrito-input").value = item.cantidad;
        itemEl.querySelector(
          `.total-item-${itemId}`
        ).textContent = `Total: ${acumuladoFormateado}`; // Actualizar resumen

        const summaryItem = document.querySelector(`.summary-item-${itemId}`);
        if (summaryItem) {
          summaryItem.querySelector(`.cantidad-summary-${itemId}`).textContent =
            item.cantidad;
          summaryItem.querySelector(
            `.acumulado-summary-${itemId}`
          ).textContent = acumuladoFormateado;
        }
      } else {
        // Producto eliminado: remover de la vista
        itemEl.remove();
        const summaryItem = document.querySelector(`.summary-item-${itemId}`);
        if (summaryItem) summaryItem.remove();
      }
    }); // Lógica para mostrar mensaje de carrito vacío si es necesario

    if (keysEnCarrito.length === 0) {
      // Asegúrate de que el contenedor de productos se vacíe
      if (productosContainer) {
        productosContainer.innerHTML = "";
      }

      const cartBody = document.querySelector(".card-body"); // Si el carrito está vacío y no hay un mensaje, lo agregamos
      if (cartBody && !cartBody.querySelector(".text-center.text-muted")) {
        cartBody.innerHTML =
          '<p class="text-center text-muted">Tu carrito está vacío.</p>';
      }
      // Desactivar el botón de pagar/checkout si existe
      const checkoutBtn = document.querySelector(".btn-checkout");
      if (checkoutBtn) checkoutBtn.disabled = true;
    } else {
      // Activar el botón de pagar/checkout si existe y hay productos
      const checkoutBtn = document.querySelector(".btn-checkout");
      if (checkoutBtn) checkoutBtn.disabled = false;
    }
  } // ---------------------------------------------------- // * Botones de Restar/Eliminar (product-item) * // ----------------------------------------------------

  document.addEventListener("click", function (e) {
    const target = e.target.closest(
      ".btn-restar-carrito, .btn-eliminar-carrito"
    );
    if (target) {
      e.preventDefault();
      const productoId = target.dataset.id;
      const accion = target.dataset.accion;

      const url = obtenerUrlAccion(accion);
      const data = { producto_id: productoId };

      manejarPeticionCarrito(url, "POST", data, actualizarVistaCarrito);
    }
  }); // ---------------------------------------------------- // * Botón de Limpiar Carrito * // ----------------------------------------------------

  document.addEventListener("click", function (e) {
    const target = e.target.closest(".btn-limpiar-carrito");
    if (target) {
      e.preventDefault();
      const url = obtenerUrlAccion("limpiar");

      manejarPeticionCarrito(url, "POST", {}, () => {
        // Cuando se limpia, el total es 0 y no hay datos de carrito.
        actualizarVistaCarrito({ total_carrito: 0, carrito_data: {} });
      });
    }
  }); // ---------------------------------------------------- // * Input de Cantidad (product-item) * // ----------------------------------------------------

  document.addEventListener("change", function (e) {
    const target = e.target.closest(".cantidad-carrito-input");
    if (target) {
      const productoId = target.dataset.id;
      let nuevaCantidad = parseInt(target.value); // Asegurarse de que la cantidad no sea negativa o NaN

      if (isNaN(nuevaCantidad) || nuevaCantidad < 1) {
        nuevaCantidad = 1;
        target.value = 1;
      }

      const url = obtenerUrlAccion("actualizar");
      const data = {
        producto_id: productoId,
        cantidad: nuevaCantidad,
      };

      manejarPeticionCarrito(url, "POST", data, actualizarVistaCarrito);
    }
  }); // ---------------------------------------------------- // * Botón Sumar (product-item) * // ----------------------------------------------------

  document.addEventListener("click", function (e) {
    const target = e.target.closest(".btn-sumar-carrito");
    if (target) {
      e.preventDefault();
      const input = target
        .closest(".input-group")
        .querySelector(".cantidad-carrito-input");
      let nuevaCantidad = parseInt(input.value) + 1;

      const productoId = target.dataset.id;

      const url = obtenerUrlAccion("actualizar");
      const data = {
        producto_id: productoId,
        cantidad: nuevaCantidad,
      };

      manejarPeticionCarrito(url, "POST", data, actualizarVistaCarrito);
    }
  });
}
