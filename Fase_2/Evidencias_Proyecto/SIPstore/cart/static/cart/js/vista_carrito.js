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

function hideAllCheckoutButtons() {
  btnFinishOrder.classList.add("d-none");
  btnBackStore.classList.add("d-none");
  btnCheckout.classList.add("d-none");
  btnBackOnline.classList.add("d-none");
  btnContinueCart.classList.add("d-none");
}

function updatePaymentButton() {
  const isStorePayment = paymentStore.checked;

  hideAllCheckoutButtons();

  if (isStorePayment) {
    btnFinishOrder.classList.remove("d-none");
    btnBackStore.classList.remove("d-none");
  } else {
    btnCheckout.classList.remove("d-none");
    btnBackOnline.classList.remove("d-none");
  }
}

function initCartButtonState() {
  const cartIsEmpty = isCartEmpty();

  if (btnContinueCart) {
    btnContinueCart.disabled = cartIsEmpty;
    btnContinueCart.textContent = cartIsEmpty
      ? "Carrito Vacío"
      : "Continuar Compra";
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

// --- CONFIGURACIÓN GLOBAL DE MERCADO PAGO ---
// NOTA: Es crucial inicializar la instancia una sola vez en el scope global.
const PUBLIC_KEY = window.MERCADOPAGO_PUBLIC_KEY;

// Crea una referencia global al objeto de MercadoPago
let mp;
if (window.MercadoPago) {
    mp = new window.MercadoPago(PUBLIC_KEY, {
        locale: "es-CL", 
    });
} else {
    console.error("SDK de Mercado Pago no cargado. Revisa la etiqueta script.");
}



function mostrarMensaje(mensaje, esError = true) {
    console.log(`${esError ? 'ERROR' : 'INFO'}: ${mensaje}`);
    if (esError) {
        console.error(mensaje);
    }
}

// Función para renderizar el Wallet Brick
async function renderWalletBrick(preferenceId) {
    if (!mp) {
        mostrarMensaje("Mercado Pago SDK no inicializado.", true);
        return;
    }

    const bricksBuilder = mp.bricks();

    try {
        await bricksBuilder.create("wallet", "walletBrick_container", {
            initialization: {
                preferenceId: preferenceId,
            },
        });
    } catch (e) {
        mostrarMensaje("Error al renderizar el Wallet Brick.", true);
        console.error("Detalle del error del Brick:", e);
    }
}


btnContinueCart.addEventListener("click", async function () {
    const pedidoForm = document.getElementById("pedidoForm");

    if (!pedidoForm) {
        mostrarMensaje("No se encontró el formulario de pedido.", true);
        return;
    }


    if (!pedidoForm.checkValidity()) {
        pedidoForm.reportValidity(); 
        mostrarMensaje("Por favor completa todos los campos requeridos antes de continuar.", true);
        return;
    }

    try {
        const formData = new FormData(pedidoForm);
        const responsePedido = await fetch(pedidoForm.action, {
            method: "POST",
            headers: { "X-CSRFToken": csrftoken },
            body: formData,
        });

        if (!responsePedido.ok) {
            mostrarMensaje("No se pudo crear el pedido. Revisa los datos.", true);
            return;
        }

        const pedidoData = await responsePedido.json().catch(() => ({}));
        if (pedidoData.error) {
            mostrarMensaje(pedidoData.error, true);
            return;
        }

        const response = await fetch("/crear_preferencia/");
        if (!response.ok) {
            mostrarMensaje("No se pudo generar la preferencia de pago.", true);
            return;
        }

        const preference = await response.json();
        const preferenceId = preference.id;

        if (!preferenceId) {
            mostrarMensaje("Error: no se obtuvo un ID de preferencia válido.", true);
            return;
        }

        await renderWalletBrick(preferenceId);
        bsCartListCollapse.hide();
        bsCheckoutFormCollapse.show();
        mostrarMensaje("Pedido validado correctamente. Procede con el pago.", false);
    } catch (err) {
        console.error("Error durante la validación/pago:", err);
        mostrarMensaje("Ocurrió un error al procesar el pedido o iniciar el pago.", true);
    }
});

document.addEventListener("DOMContentLoaded", () => {
    const pedidoForm = document.getElementById("pedidoForm");
    const btnCheckout = document.getElementById("walletBrick_container");
    const btnContinueCart = document.getElementById("btn-continue-cart");

    const validarFormulario = () => {
        if (!pedidoForm || !btnCheckout) return;

        const esValido = pedidoForm.checkValidity() && !isCartEmpty();

        if (esValido) {
            btnCheckout.classList.remove("d-none");
        } else {
            btnCheckout.classList.add("d-none");
        }
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

btnContinueCart.addEventListener("click", async () => {
  const pedidoForm = document.getElementById("pedidoForm");
  if (!pedidoForm.checkValidity()) {
    pedidoForm.reportValidity();
    return;
  }

  try {
    const response = await fetch("/crear_preferencia/");
    if (!response.ok) throw new Error("No se pudo generar preferencia");
    const { id: preferenceId } = await response.json();

    const btnCheckout = document.getElementById("walletBrick_container");
    btnCheckout.classList.remove("d-none"); // muestra el contenedor
    await renderWalletBrick(preferenceId); // renderiza el Brick

    bsCartListCollapse.hide();
    bsCheckoutFormCollapse.show();
  } catch (err) {
    console.error(err);
    alert("Error al generar el pago. Intenta nuevamente.");
  }
});

const btnValidateData = document.getElementById("btn-validate-data");

// --- NUEVA LÓGICA DE VALIDACIÓN --- //
btnContinueCart.addEventListener("click", function () {
    bsCartListCollapse.hide();
    bsCheckoutFormCollapse.show();
    btnContinueCart.classList.add("d-none");
    btnValidateData.classList.remove("d-none");
});

btnValidateData.addEventListener("click", async function () {
    const pedidoForm = document.getElementById("pedidoForm");

    if (!pedidoForm.checkValidity()) {
        pedidoForm.reportValidity();
        mostrarMensaje("Por favor completa todos los campos requeridos antes de continuar.", true);
        return;
    }

    const rutInput = document.getElementById("clientRut");
    if (rutInput && !/^(\d{1,3}(?:\.\d{3})*)\-\d|k|K$/.test(rutInput.value.trim())) {
        mostrarMensaje("El RUT ingresado no es válido.", true);
        return;
    }

    mostrarMensaje("Datos validados correctamente.", false);

    btnValidateData.classList.add("d-none");

    const paymentOnline = document.getElementById("paymentOnline");
    const paymentStore = document.getElementById("paymentStore");

    if (paymentOnline.checked) {
        try {
            const response = await fetch("/crear_preferencia/");
            const preference = await response.json();

            if (!preference.id) {
                mostrarMensaje("No se pudo crear la preferencia de pago.", true);
                return;
            }

            await renderWalletBrick(preference.id);
            document.getElementById("walletBrick_container").classList.remove("d-none");
            btnBackOnline.classList.remove("d-none");
        } catch (err) {
            mostrarMensaje("Error al iniciar Mercado Pago.", true);
            console.error(err);
        }
    } else if (paymentStore.checked) {
        btnFinishOrder.classList.remove("d-none");
        btnBackStore.classList.remove("d-none");
    }
});
