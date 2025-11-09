document.addEventListener("DOMContentLoaded", function () {
  const btnAgregarCarrito = document.getElementById("btnAgregarCarrito");

  if (!btnAgregarCarrito) return;

  btnAgregarCarrito.addEventListener("click", function () {
    btnAgregarCarrito.disabled = true;
    btnAgregarCarrito.innerHTML = '<i class="bi bi-hourglass-split"></i> Agregando...';

    fetch("/quote/agregar-al-carrito/", {
      method: "POST",
      headers: {
        "X-CSRFToken": getCSRFToken(),
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          showToast("🛒 " + data.message, "success");
          setTimeout(() => {
            window.location.href = "/carrito/";
          }, 1000);
        } else {
          showToast("⚠️ " + data.message, "warning");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        showToast("❌ Error al agregar al carrito.", "danger");
      })
      .finally(() => {
        btnAgregarCarrito.disabled = false;
        btnAgregarCarrito.innerHTML =
          '<i class="bi bi-cart-plus"></i> Agregar al Carrito';
      });
  });


  function getCSRFToken() {
    const csrfInput = document.querySelector("[name=csrfmiddlewaretoken]");
    return csrfInput ? csrfInput.value : "";
  }


  function showToast(message, type = "info") {
    const toast = document.createElement("div");
    toast.className = `toast align-items-center text-white bg-${type} border-0 position-fixed bottom-0 end-0 m-3`;
    toast.style.zIndex = 1055;
    toast.innerHTML = `
      <div class="d-flex">
        <div class="toast-body">${message}</div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
      </div>`;
    document.body.appendChild(toast);

    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();

    toast.addEventListener("hidden.bs.toast", () => {
      toast.remove();
    });
  }
});
