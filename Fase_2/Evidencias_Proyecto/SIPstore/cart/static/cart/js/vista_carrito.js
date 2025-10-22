const cartListCollapse = document.getElementById("cartListCollapse");
const checkoutFormCollapse = document.getElementById("checkoutFormCollapse");
const cartControls = document.getElementById("cart-controls");

const paymentOnline = document.getElementById("paymentOnline");
const paymentStore = document.getElementById("paymentStore");

const bsCartListCollapse = new bootstrap.Collapse(cartListCollapse, {
  toggle: false,
});
const bsCheckoutFormCollapse = new bootstrap.Collapse(checkoutFormCollapse, {
  toggle: false,
});

function isCartEmpty() {
  const totalSummaryElement = document.getElementById("total_sumary");
  if (!totalSummaryElement) return true;

  const totalText = totalSummaryElement.textContent
    .replace("$", "")
    .replace(/\./g, "")
    .replace(/,/g, "")
    .trim();
  const total = parseFloat(totalText);

  return isNaN(total) || total <= 0;
}

function toggleCartCollapse() {
  if (checkoutFormCollapse.classList.contains("show")) {
    bsCheckoutFormCollapse.hide();
    bsCartListCollapse.show();
  } else {
    bsCartListCollapse.hide();
    bsCheckoutFormCollapse.show();
  }
}

function updatePaymentButton() {
  const isStorePayment = paymentStore.checked;

  if (isStorePayment) {
    cartControls.innerHTML = `
            <button type="submit" form="pedidoForm" id="btn-finish-order" class="btn btn-success w-100 mb-2">
                Terminar Pedido &check;
            </button>
            <button id="btn-back" class="btn btn-outline-secondary w-100" onclick="toggleCartCollapse()">
                &larr; Volver
            </button>
        `;
    document
      .getElementById("btn-finish-order")
      .addEventListener("click", function (e) {
        e.preventDefault();
        const form = document.getElementById("pedidoForm");
        if (form) form.submit();
      });
  } else {
    cartControls.innerHTML = `
            <button id="btn-continue-payment" class="btn btn-primary w-100 mb-2">
                Continuar con el Pago &rarr;
            </button>
            <button id="btn-back" class="btn btn-outline-secondary w-100" onclick="toggleCartCollapse()">
                &larr; Volver
            </button>
        `;
  }
}

function initCartButtonState() {
  const cartIsEmpty = isCartEmpty();
  const continueButton = document.getElementById("btn-continue-cart");

  if (continueButton) {
    continueButton.disabled = cartIsEmpty;
    continueButton.textContent = cartIsEmpty
      ? "Carrito Vacío"
      : "Continuar Compra →";
    continueButton.classList.toggle("btn-success", !cartIsEmpty);
    continueButton.classList.toggle("btn-secondary", cartIsEmpty);
  }
}

function showLocalCard(localId) {
  const localCard = document.getElementById("localCard");
  const localCardName = document.getElementById("localCardName");
  const localCardAddress = document.getElementById("localCardAddress");

  const select = document.getElementById("localSelect");
  const selectedOption = select.options[select.selectedIndex];

  if (localId) {
    const nombre = selectedOption.getAttribute("data-nombre");
    const ubicacion = selectedOption.getAttribute("data-ubicacion");

    localCardName.textContent = nombre;
    localCardAddress.textContent = ubicacion;
    localCard.classList.remove("d-none");
  } else {
    localCard.classList.add("d-none");
  }
}

checkoutFormCollapse.addEventListener("shown.bs.collapse", function () {
  updatePaymentButton();

  paymentOnline.addEventListener("change", updatePaymentButton);
  paymentStore.addEventListener("change", updatePaymentButton);
});

cartListCollapse.addEventListener("shown.bs.collapse", function () {
  const cartIsEmpty = isCartEmpty();

  cartControls.innerHTML = `
        <button id="btn-continue-cart" class="btn btn-success w-100" 
            onclick="toggleCartCollapse()" ${cartIsEmpty ? "disabled" : ""}>
            ${cartIsEmpty ? "Carrito Vacío" : "Continuar Compra &rarr;"}
        </button>
    `;

  const continueButton = document.getElementById("btn-continue-cart");
  if (cartIsEmpty) {
    continueButton.classList.remove("btn-success");
    continueButton.classList.add("btn-secondary");
  }

  paymentOnline.removeEventListener("change", updatePaymentButton);
  paymentStore.removeEventListener("change", updatePaymentButton);
});

document.addEventListener("DOMContentLoaded", initCartButtonState);
