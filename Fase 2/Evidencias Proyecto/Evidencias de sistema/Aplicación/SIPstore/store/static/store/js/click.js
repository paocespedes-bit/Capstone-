document.addEventListener("DOMContentLoaded", function () {
  const cards = document.querySelectorAll(".card");

  cards.forEach((card) => {
    let expanded = false;

    card.addEventListener("click", function (e) {
      if (e.target.closest("button") || e.target.closest(".add-cart")) {
        return;
      }

      const urlDestino = card.closest(".contenedor-card").dataset.url;

      if (window.innerWidth > 768) {
        window.location.href = urlDestino;
      } else {
        if (!expanded) {
          card.querySelector(".expansion").classList.toggle("show");
          expanded = true;
        } else {
          window.location.href = urlDestino;
        }
      }
    });
  });
});