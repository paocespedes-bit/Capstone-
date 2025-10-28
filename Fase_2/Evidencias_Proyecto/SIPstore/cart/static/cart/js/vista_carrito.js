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
const PUBLIC_KEY = "APP_USR-72031fd5-9b5f-48d6-9f43-0b881194724c";

// Crea una referencia global al objeto de MercadoPago
let mp;
if (window.MercadoPago) {
    mp = new window.MercadoPago(PUBLIC_KEY, {
        locale: "es-CL", 
    });
} else {
    console.error("SDK de Mercado Pago no cargado. Revisa la etiqueta script.");
}
// ----------------------------------------------


// Función simple para mostrar mensajes de error/éxito (reemplazando alert())
function mostrarMensaje(mensaje, esError = true) {
    console.log(`${esError ? 'ERROR' : 'INFO'}: ${mensaje}`);
    // Aquí puedes implementar una lógica para mostrar un modal o un toast en la UI
    // Por ahora, usaremos console.error para los errores.
    if (esError) {
        console.error(mensaje);
    }
}

// Función para renderizar el Wallet Brick
// Usamos la instancia 'mp' creada globalmente.
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
            // Aquí puedes añadir personalizaciones si las necesitas
        });
        // Ocultar cualquier loading indicator si existía
    } catch (e) {
        mostrarMensaje("Error al renderizar el Wallet Brick.", true);
        console.error("Detalle del error del Brick:", e);
    }
}

// --- Event Listener para Continuar el Carrito ---
btnContinueCart.addEventListener("click", async function () {
    const pedidoForm = document.getElementById("pedidoForm");

    // --- 1️⃣ VALIDAR CAMPOS DEL FORMULARIO ---
    if (!pedidoForm) {
        mostrarMensaje("No se encontró el formulario de pedido.", true);
        return;
    }

    // Usamos la API nativa de validación de formularios HTML5
    if (!pedidoForm.checkValidity()) {
        pedidoForm.reportValidity(); // Muestra errores visuales en el navegador
        mostrarMensaje("Por favor completa todos los campos requeridos antes de continuar.", true);
        return;
    }

    // --- 2️⃣ ENVIAR DATOS AL SERVIDOR PARA CREAR PEDIDO ---
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

        // --- 3️⃣ GENERAR LA PREFERENCIA DE MERCADO PAGO ---
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

        // --- 4️⃣ MOSTRAR INTERFAZ DE PAGO ---
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

    // Función que habilita/deshabilita el botón Mercado Pago
    const validarFormulario = () => {
        if (!pedidoForm || !btnCheckout) return;

        // checkValidity valida todos los campos requeridos
        const esValido = pedidoForm.checkValidity() && !isCartEmpty();

        if (esValido) {
            btnCheckout.classList.remove("d-none");
        } else {
            btnCheckout.classList.add("d-none");
        }
    };

    // --- Paso 1: Cuando se presiona Continuar Compra ---
    if (btnContinueCart) {
        btnContinueCart.addEventListener("click", () => {
            bsCartListCollapse.hide(); // ocultar Summary
            bsCheckoutFormCollapse.show(); // mostrar form_pedido

            // Validar inmediatamente
            validarFormulario();

            // --- Paso 2: Escuchar cambios en los inputs del formulario ---
            pedidoForm.querySelectorAll("input, select, textarea").forEach((input) => {
                input.addEventListener("input", validarFormulario);
                input.addEventListener("change", validarFormulario); // para selects
            });
        });
    }

    // --- Paso 3: Clic en botón Mercado Pago ---
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
