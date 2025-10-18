document.addEventListener("DOMContentLoaded", () => {
  // Toast
  const toastEl = document.getElementById("toast");
  const toastBody = document.getElementById("toast-body");
  const bsToast = toastEl ? new bootstrap.Toast(toastEl) : null;

  function mostrarToast(msg, tipo = "success") {
    if (!bsToast) return;
    toastEl.classList.remove("bg-success", "bg-danger");
    toastEl.classList.add(tipo === "danger" ? "bg-danger" : "bg-success");
    toastBody.textContent = msg;
    bsToast.show();
  }

  function actualizarBadge(cantidad) {
    const badge = document.getElementById("contador-carrito");
    if (badge) badge.textContent = cantidad;
  }

  function getCSRFToken() {
    const csrf = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrf ? csrf.value : "";
  }

  async function enviarAccion(url, producto_id, content_type, cantidad = 1) {
    try {
      const formData = new FormData();
      formData.append("producto_id", producto_id);
      formData.append("content_type", content_type);
      formData.append("cantidad", cantidad);
      formData.append("csrfmiddlewaretoken", getCSRFToken());

      const res = await fetch(url, { method: "POST", body: formData });
      const data = await res.json();

      if (data.ok) {
        mostrarToast(data.msg, "success");
        actualizarBadge(data.cantidad_total);
      } else {
        mostrarToast(data.msg, "danger");
      }
    } catch (err) {
      mostrarToast("Error al procesar la solicitud", "danger");
      console.error(err);
    }
  }

  function obtenerCantidad(card) {
    const input = card.querySelector(".cantidad-input");
    return input ? parseInt(input.value) || 1 : 1;
  }

  // Agregar producto
  document.querySelectorAll(".btn-agregar").forEach((btn) => {
    if (!btn) return;
    btn.addEventListener("click", () => {
      const card = btn.closest(".card");
      if (!card) return;
      const producto_id = btn.dataset.id;
      const content_type = btn.dataset.ctid;
      const cantidad = obtenerCantidad(card);
      const url = btn.dataset.url || "/agregar/";
      enviarAccion(url, producto_id, content_type, cantidad);
    });
  });

  // Restar producto
  document.querySelectorAll(".btn-restar").forEach((btn) => {
    if (!btn) return;
    btn.addEventListener("click", () => {
      const card = btn.closest(".card");
      if (!card) return;
      const producto_id = btn.dataset.id;
      const content_type = btn.dataset.ctid;
      const cantidad = obtenerCantidad(card);
      const url = btn.dataset.url || "/restar/";
      enviarAccion(url, producto_id, content_type, cantidad);
    });
  });

  // Eliminar producto
  document.querySelectorAll(".btn-eliminar").forEach((btn) => {
    if (!btn) return;
    btn.addEventListener("click", () => {
      const producto_id = btn.dataset.id;
      const content_type = btn.dataset.ctid;
      const url = btn.dataset.url || "/eliminar/";
      enviarAccion(url, producto_id, content_type);
    });
  });

  // Limpiar carrito
  const btnLimpiar = document.getElementById("btn-limpiar");
  if (btnLimpiar) {
    btnLimpiar.addEventListener("click", () => {
      enviarAccion("/limpiar/");
    });
  }
});
