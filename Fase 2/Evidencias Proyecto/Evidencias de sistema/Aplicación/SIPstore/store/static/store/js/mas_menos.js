document.addEventListener("DOMContentLoaded", function () {
  const cards = document.querySelectorAll(".contenedor-card");

  cards.forEach((card) => {
    const minusBtn = card.querySelector(".bi-dash-lg").closest("button");
    const plusBtn = card.querySelector(".bi-plus-lg").closest("button");
    const quantitySpan = card.querySelector(".quantity span");

    let quantity = parseInt(quantitySpan.textContent, 10);

    minusBtn.addEventListener("click", function (e) {
      e.stopPropagation(); // evita que el click afecte a la tarjeta
      if (quantity > 1) {
        quantity--;
        quantitySpan.textContent = quantity;
      }
    });

    plusBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      quantity++;
      quantitySpan.textContent = quantity;
    });
  });
});