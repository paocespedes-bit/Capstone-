const cartListCollapse = document.getElementById("cartListCollapse");
const checkoutFormCollapse = document.getElementById("checkoutFormCollapse");
const cartControls = document.getElementById("cart-controls");

const bsCartListCollapse = new bootstrap.Collapse(cartListCollapse, {
  toggle: false,
});
const bsCheckoutFormCollapse = new bootstrap.Collapse(checkoutFormCollapse, {
  toggle: false,
});


function toggleCartCollapse() {
  if (checkoutFormCollapse.classList.contains("show")) {
    bsCheckoutFormCollapse.hide();
    bsCartListCollapse.show();
  } else {
    bsCartListCollapse.hide();
    bsCheckoutFormCollapse.show();
  }
}

checkoutFormCollapse.addEventListener("shown.bs.collapse", function () {
  cartControls.innerHTML = `
                <button id="btn-continue-payment" class="btn btn-primary w-100 mb-2">Continuar con el Pago &rarr;</button>
                <button id="btn-back" class="btn btn-outline-secondary w-100" onclick="toggleCartCollapse()">
                    &larr; Volver o Cancelar
                </button>
            `;
});


cartListCollapse.addEventListener("shown.bs.collapse", function () {
  cartControls.innerHTML = `
                <button id="btn-continue-cart" class="btn btn-success w-100" 
                        onclick="toggleCartCollapse()">
                    Continuar Compra &rarr;
                </button>
            `;
});


function showLocalCard(localId) {
  const localCard = document.getElementById("localCard");
  const localCardName = document.getElementById("localCardName");
  const localCardAddress = document.getElementById("localCardAddress");

  const locales = {
    local1: {
      name: "Local Centro - Santiago",
      address: "Calle Principal 123, Santiago. Horario: 9:00 - 18:00.",
    },
    local2: {
      name: "Local Mall Costanera - Providencia",
      address: "Av. Andrés Bello 2420, Providencia. Horario: 10:00 - 20:00.",
    },
  };

  if (localId && locales[localId]) {
    localCardName.textContent = locales[localId].name;
    localCardAddress.textContent = locales[localId].address;
    localCard.classList.remove("d-none");
  } else {
    localCard.classList.add("d-none");
  }
}
