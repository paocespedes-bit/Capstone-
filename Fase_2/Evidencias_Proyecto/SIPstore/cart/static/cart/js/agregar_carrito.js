document.addEventListener("DOMContentLoaded", () => {
  const botonesAgregar = document.querySelectorAll(".add-cart");
  const badgeCarrito = document.querySelector("#cart-badge"); 
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

  botonesAgregar.forEach((boton, index) => {
    boton.addEventListener("click", async (e) => {
      e.stopPropagation();
      const card = e.target.closest(".card");
      const cantidad = parseInt(card.querySelector(".quantity span").textContent);

      // Obtener datos del producto desde data-attributes del botón
      const contentType = boton.dataset.contenttype;  
      const productId = boton.dataset.id; 
      
      const data = {
        content_type: contentType,
        product_id: productId,
        quantity: cantidad
      };

      const response = await fetch(URL_AGREGAR_CARRITO, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken || "",
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();
      if (response.ok) {
        mostrarToast(result.message);         // ✅ Usamos tu toast existente
        badgeCarrito.textContent = result.total_items;
        badgeCarrito.classList.remove("hidden"); // muestra el badge si estaba oculto
      }
    });
  });

  // Función para mostrar el toast usando tu HTML existente
 function mostrarToast(mensaje) {
    const toastEl = document.getElementById("toast");
    toastEl.querySelector(".toast-message").textContent = mensaje;
    const toast = new bootstrap.Toast(toastEl);
    toast.show();
  }
});
