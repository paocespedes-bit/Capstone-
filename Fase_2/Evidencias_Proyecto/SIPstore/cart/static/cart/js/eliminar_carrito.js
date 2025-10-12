document.addEventListener("DOMContentLoaded", () => {
  const botonesEliminar = document.querySelectorAll(".remove-cart-item");
  const badgeCarrito = document.querySelector("#cart-badge"); 
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value

  botonesEliminar.forEach(boton => {
    boton.addEventListener("click", async (e) => {
      e.stopPropagation();

      const contentType = boton.dataset.contenttype;
      const productId = boton.dataset.id;
      try {
      const response = await fetch(URL_ELIMINAR_CARRITO, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken || "",
        },
        body: JSON.stringify({
          content_type: contentType,
          product_id: productId
        }),
      });

      if (!response.ok) {
        console.error("Error al eliminar el producto");
        return;
      }

      const result = await response.json();

      badgeCarrito.textContent = result.total_items;
      badgeCarrito.classList.remove("hidden");

      } catch (error) {
        console.error("Error en la solicitud:", error);
      }      
    });
  });
})

