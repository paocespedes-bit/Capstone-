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
    // Verificar si mp está inicializado antes de continuar
    if (!mp) {
        mostrarMensaje("El sistema de pago no está disponible temporalmente.", true);
        return;
    }

    try {
        // 1. Solicitar la preferencia de pago a Django
        const response = await fetch("/crear_preferencia/");
        
        if (!response.ok) {
            // Manejar errores de Django o Mercado Pago API
            const errorData = await response.json();
            mostrarMensaje(
                "No se pudo generar la preferencia de pago: " +
                (errorData.message || errorData.error || "Error desconocido en el backend"),
                true
            );
            return;
        }

        const preference = await response.json();
        const preferenceId = preference.id;

        if (!preferenceId) {
            console.error("Preference ID no recibido:", preference);
            mostrarMensaje("Ocurrió un error al generar la preferencia de pago. (ID no encontrado)", true);
            return;
        }

        // 2. Renderizar el Brick
        await renderWalletBrick(preferenceId);

        // 3. Mostrar la interfaz de checkout
        // Asegúrate de que tienes un elemento con ID 'walletBrick_container' en tu HTML
        // para que el Brick pueda renderizarse.
        bsCartListCollapse.hide();
        bsCheckoutFormCollapse.show();
        
    } catch (err) {
        console.error("Error al inicializar el pago/Brick:", err);
        mostrarMensaje("Ocurrió un error al intentar iniciar el pago.", true);
    }
});
