document.addEventListener("DOMContentLoaded", () => {
  const botonesAgregar = document.querySelectorAll(".add-cart");
  const badgeCarrito = document.querySelector("#cart-badge"); 
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

  botonesAgregar.forEach(boton => {
    boton.addEventListener("click", async (e) => {
      e.stopPropagation();

      const card = e.target.closest(".card");
      const cantidad = parseInt(card.querySelector(".quantity span").textContent) || 1;

      // Datos del producto desde data-attributes
      const contentType = boton.dataset.contenttype;  
      const productId = boton.dataset.id; 

      try {
        const response = await fetch(URL_AGREGAR_CARRITO, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken || "",
          },
          body: JSON.stringify({ 
            content_type: contentType,
            product_id: productId,
            quantity: cantidad
          }),
        });

        if (!response.ok) {
          console.error("Error al agregar al carrito");
          return;
        }

        const result = await response.json();

        // Actualizar badge del carrito
        badgeCarrito.textContent = result.total_items;
        badgeCarrito.classList.remove("hidden");

        // Mostrar toast
        mostrarToast(result.message);

      } catch (error) {
        console.error("Error en la solicitud:", error);
      }
    });
  });

  // Función para mostrar toast usando Bootstrap
  function mostrarToast(mensaje) {
    const toastEl = document.getElementById("toast");
    if (!toastEl) return;
    toastEl.querySelector(".toast-message").textContent = mensaje;
    const toast = new bootstrap.Toast(toastEl);
    toast.show();
  }
});
