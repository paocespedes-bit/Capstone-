// === FUNCIONES BÁSICAS === //
function obtenerCarrito() {
  return JSON.parse(localStorage.getItem("carrito")) || [];
}

function guardarCarrito(carrito) {
  localStorage.setItem("carrito", JSON.stringify(carrito));
  actualizarBadge();
}

function actualizarBadge() {
  const carrito = obtenerCarrito();
  const total = carrito.reduce((acc, p) => acc + p.cantidad, 0);
  const badge = document.getElementById("cart-badge");
  if (badge) {
    if (total > 0) {
      badge.textContent = total;
      badge.style.display = "inline-block";
    } else {
      badge.style.display = "none";  
    }
  }
}

function mostrarToast(mensaje) {
  const toast = document.getElementById("toastCarrito");
  const texto = document.getElementById("toastMensaje");
  texto.textContent = mensaje;

  const toastBootstrap = new bootstrap.Toast(toast);
  toastBootstrap.show();
}

// === AGREGAR PRODUCTO AL CARRITO === //
function agregarAlCarrito(producto) {
  let carrito = obtenerCarrito();
  const existente = carrito.find(p => p.id === producto.id && p.content_type === producto.content_type);

  if (existente) {
    existente.cantidad += producto.cantidad;
  } else {
    carrito.push(producto);
  }

  guardarCarrito(carrito);
  mostrarToast(`${producto.nombre_producto} agregado al carrito`);
}

// === CUANDO EL DOM ESTÉ LISTO === //
document.addEventListener("DOMContentLoaded", () => {
  actualizarBadge();
  // --- Botón "Agregar al carrito" ---
  document.querySelectorAll(".btn-agregar-carrito").forEach(btn => {
    btn.addEventListener("click", function() {
      // Busca el contenedor .actions más cercano para obtener su cantidad
      const container = this.closest(".actions");
      const cantidadSpan = container.querySelector(".quantity span");
      const cantidad = parseInt(cantidadSpan.textContent);

      const producto = {
        content_type: this.dataset.contenttype,
        id: parseInt(this.dataset.id),
        nombre_producto: this.dataset.nombre,
        cantidad: cantidad,
        precio_unitario: parseFloat(this.dataset.precio)
      };

      agregarAlCarrito(producto);
      // Resetea el contador visual a 1 tras añadir
      cantidadSpan.textContent = 1;
    });
  });
});
