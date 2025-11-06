const cartListCollapse = document.getElementById("cartListCollapse");
const checkoutFormCollapse = document.getElementById("checkoutFormCollapse");
const cartControls = document.getElementById("cart-controls");

const paymentOnline = document.getElementById("paymentOnline");
const paymentStore = document.getElementById("paymentStore");

const btnContinueCart = document.getElementById("btn-continue-cart");
const btnFinishOrder = document.getElementById("btn-finish-order");
const btnBackStore = document.getElementById("btn-back-store");
const btnCheckout = document.getElementById("walletBrick_container");
const btnBackOnline = document.getElementById("btn-back-online");
const btnValidateData = document.getElementById("btn-validate-data");

const bsCartListCollapse = new bootstrap.Collapse(cartListCollapse, { toggle: false });
const bsCheckoutFormCollapse = new bootstrap.Collapse(checkoutFormCollapse, { toggle: false });


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

function hideAllCheckoutButtons() {
  btnFinishOrder.classList.add("d-none");
  btnBackStore.classList.add("d-none");
  btnCheckout.classList.add("d-none");
  btnBackOnline.classList.add("d-none");
  btnContinueCart.classList.add("d-none");
  btnValidateData.classList.add("d-none");
}

function initCartButtonState() {
  const cartIsEmpty = isCartEmpty();

  if (btnContinueCart) {
    btnContinueCart.disabled = cartIsEmpty;
    btnContinueCart.textContent = cartIsEmpty ? "Carrito Vacío" : "Continuar Compra";
    btnContinueCart.classList.toggle("btn-success", !cartIsEmpty);
    btnContinueCart.classList.toggle("btn-secondary", cartIsEmpty);
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

function toggleCartCollapse() {
  const isCheckoutVisible = checkoutFormCollapse.classList.contains("show");
  hideAllCheckoutButtons();

  if (isCheckoutVisible) {
    bsCheckoutFormCollapse.hide();
    bsCartListCollapse.show();
    btnContinueCart.classList.remove("d-none");
  } else {
    bsCartListCollapse.hide();
    bsCheckoutFormCollapse.show();

    if (paymentOnline.checked) {
      btnValidateData.classList.remove("d-none");
      btnBackOnline.classList.remove("d-none");
    } else if (paymentStore.checked) {
      btnFinishOrder.classList.remove("d-none");
      btnBackStore.classList.remove("d-none");
    }
  }
}

function updatePaymentButton() {
  const isStorePayment = paymentStore.checked;
  const isOnlinePayment = paymentOnline.checked;

  hideAllCheckoutButtons();

  if (isStorePayment) {
    btnFinishOrder.classList.remove("d-none");
    btnBackStore.classList.remove("d-none");
    btnValidateData.classList.add("d-none");
  } else if (isOnlinePayment) {
    btnValidateData.classList.remove("d-none");
    btnBackOnline.classList.remove("d-none");
  }
}

checkoutFormCollapse.addEventListener("shown.bs.collapse", function () {
  updatePaymentButton();
  paymentOnline.addEventListener("change", updatePaymentButton);
  paymentStore.addEventListener("change", updatePaymentButton);
});

cartListCollapse.addEventListener("shown.bs.collapse", function () {
  const cartIsEmpty = isCartEmpty();

  hideAllCheckoutButtons();
  btnContinueCart.classList.remove("d-none");

  initCartButtonState();

  paymentOnline.removeEventListener("change", updatePaymentButton);
  paymentStore.removeEventListener("change", updatePaymentButton);
});

document.addEventListener("DOMContentLoaded", initCartButtonState);

document.addEventListener("DOMContentLoaded", function () {
  hideAllCheckoutButtons();
  if (cartListCollapse.classList.contains("show")) {
    btnContinueCart.classList.remove("d-none");
    initCartButtonState();
  }
});

const PUBLIC_KEY = window.MERCADOPAGO_PUBLIC_KEY;
let mp;

if (window.MercadoPago) {
  mp = new window.MercadoPago(PUBLIC_KEY, { locale: "es-CL" });
} else {
  console.error("SDK de Mercado Pago no cargado. Revisa la etiqueta script.");
}

function mostrarMensaje(mensaje, esError = true) {
  console.log(`${esError ? "ERROR" : "INFO"}: ${mensaje}`);
  if (esError) console.error(mensaje);
}

async function renderWalletBrick(preferenceId) {
  if (!mp) {
    mostrarMensaje("Mercado Pago SDK no inicializado.", true);
    return;
  }

  const bricksBuilder = mp.bricks();

  try {
    await bricksBuilder.create("wallet", "walletBrick_container", {
      initialization: { preferenceId: preferenceId },
    });
  } catch (e) {
    mostrarMensaje("Error al renderizar el Wallet Brick.", true);
    console.error("Detalle del error del Brick:", e);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const pedidoForm = document.getElementById("pedidoForm");
  const btnCheckout = document.getElementById("walletBrick_container");
  const btnContinueCart = document.getElementById("btn-continue-cart");

  const validarFormulario = () => {
    if (!pedidoForm || !btnCheckout) return;
    const esValido = pedidoForm.checkValidity() && !isCartEmpty();
    btnCheckout.classList.toggle("d-none", !esValido);
  };

  if (btnContinueCart) {
    btnContinueCart.addEventListener("click", () => {
      bsCartListCollapse.hide();
      bsCheckoutFormCollapse.show();
      validarFormulario();

      pedidoForm.querySelectorAll("input, select, textarea").forEach((input) => {
        input.addEventListener("input", validarFormulario);
        input.addEventListener("change", validarFormulario);
      });
    });
  }

  if (btnCheckout) {
    btnCheckout.addEventListener("click", async () => {
      if (!pedidoForm.checkValidity()) {
        pedidoForm.reportValidity();
        mostrarMensaje("Completa todos los campos requeridos antes de pagar.", true);
        return;
      }

      try {
        const response = await fetch("/crear_preferencia/");
        if (!response.ok) {
          mostrarMensaje("Error al generar preferencia de pago.", true);
          return;
        }
        const preference = await response.json();
        await renderWalletBrick(preference.id);
      } catch (err) {
        mostrarMensaje("Error al iniciar pago.", true);
      }
    });
  }
});

btnContinueCart.addEventListener("click", function () {
  bsCartListCollapse.hide();
  bsCheckoutFormCollapse.show();
  btnContinueCart.classList.add("d-none");

  if (paymentOnline.checked) {
    btnValidateData.classList.remove("d-none");
  } else {
    btnValidateData.classList.add("d-none");
    btnFinishOrder.classList.remove("d-none");
    btnBackStore.classList.remove("d-none");
  }
});

function validarRut(rut) {
  rut = rut.replace(/\./g, "").replace(/-/g, "").trim().toUpperCase();
  if (!/^(\d{7,8}[0-9K])$/.test(rut)) return false;

  const cuerpo = rut.slice(0, -1);
  const dv = rut.slice(-1);
  let suma = 0;
  let multiplo = 2;

  for (let i = cuerpo.length - 1; i >= 0; i--) {
    suma += parseInt(cuerpo.charAt(i)) * multiplo;
    multiplo = multiplo < 7 ? multiplo + 1 : 2;
  }

  const dvEsperado = 11 - (suma % 11);
  const dvFinal = dvEsperado === 11 ? "0" : dvEsperado === 10 ? "K" : String(dvEsperado);
  return dv === dvFinal;
}

function validarTelefono(telefono) {
  const regex = /^(?:\+?56)?(?:9\d{8}|[2-9]\d{7})$/;
  return regex.test(telefono.trim());
}

document.addEventListener("DOMContentLoaded", function () {
  const rutInput = document.getElementById("clientRut");
  const phoneInput = document.getElementById("clientPhone");
  const emailInput = document.getElementById("clientEmail");
  const pedidoForm = document.getElementById("pedidoForm");

  rutInput.addEventListener("input", () => {
    rutInput.setCustomValidity("");
    const rutVal = rutInput.value.trim();
    if (rutVal && !validarRut(rutVal)) {
      rutInput.setCustomValidity("El RUT ingresado no es válido. Ejemplo correcto: 12.345.678-5");
    }
  });

  phoneInput.addEventListener("input", () => {
    phoneInput.setCustomValidity("");
    const phoneVal = phoneInput.value.trim();
    if (phoneVal && !validarTelefono(phoneVal)) {
      phoneInput.setCustomValidity("Ingresa un número de celular válido. Ejemplo: +56912345678 o 912345678");
    }
  });

  pedidoForm.addEventListener("submit", (e) => {
    if (!pedidoForm.checkValidity()) {
      e.preventDefault();
      pedidoForm.reportValidity();
      alert("Por favor corrige los campos inválidos antes de continuar.");
    }
  });
});

btnValidateData.addEventListener("click", async function () {
  const pedidoForm = document.getElementById("pedidoForm");

  if (!pedidoForm.checkValidity()) {
    pedidoForm.reportValidity();
    mostrarMensaje("Por favor completa todos los campos requeridos antes de continuar.", true);
    return;
  }

  mostrarMensaje("Validando datos del pedido...", false);
  btnValidateData.classList.add("d-none");

  const formData = new FormData(pedidoForm);

  try {
    const responsePedido = await fetch("/crear-pedido/", {
      method: "POST",
      body: formData,
    });

    const dataPedido = await responsePedido.json();

    if (!dataPedido.ok || !dataPedido.pedido_id) {
      mostrarMensaje("Error al crear el pedido.", true);
      console.error("Respuesta del pedido:", dataPedido);
      return;
    }

    const pedidoId = dataPedido.pedido_id;
    mostrarMensaje(`Pedido #${pedidoId} creado correctamente. Generando preferencia...`, false);

    const responsePref = await fetch("/crear_preferencia/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pedido_id: pedidoId }),
    });

    const preference = await responsePref.json();

    if (!preference.id) {
      mostrarMensaje("Error al generar preferencia de Mercado Pago.", true);
      console.error("Respuesta de preferencia:", preference);
      return;
    }

    await renderWalletBrick(preference.id);
    document.getElementById("walletBrick_container").classList.remove("d-none");
    btnBackOnline.classList.remove("d-none");

    mostrarMensaje("Botón de Mercado Pago listo para pagar.", false);
  } catch (err) {
    mostrarMensaje("Error al crear pedido o preferencia de pago.", true);
    console.error(err);
  }
});
