// --------------------------
// vista_carrito.js (corregido)
// --------------------------

/* Helpers */
function $id(id) {
  return document.getElementById(id);
}

function safeClassListAdd(el, className) {
  if (el && el.classList) el.classList.add(className);
}
function safeClassListRemove(el, className) {
  if (el && el.classList) el.classList.remove(className);
}
function safeToggleClass(el, className, condition) {
  if (!el || !el.classList) return;
  if (condition) el.classList.add(className);
  else el.classList.remove(className);
}

/* Elementos del DOM (puede que algunos no existan en todas las vistas) */
const cartListCollapse = $id("cartListCollapse");
const checkoutFormCollapse = $id("checkoutFormCollapse");
const cartControls = $id("cart-controls");

const paymentOnline = $id("paymentOnline");
const paymentStore = $id("paymentStore");

const btnContinueCart = $id("btn-continue-cart");
const btnFinishOrder = $id("btn-finish-order");
const btnBackStore = $id("btn-back-store");
const walletContainer = $id("walletBrick_container"); // contenedor del brick
const btnBackOnline = $id("btn-back-online");
const btnValidateData = $id("btn-validate-data");

/* Bootstrap Collapses (si existen los elementos) */
let bsCartListCollapse = null;
let bsCheckoutFormCollapse = null;
try {
  if (cartListCollapse) bsCartListCollapse = new bootstrap.Collapse(cartListCollapse, { toggle: false });
  if (checkoutFormCollapse) bsCheckoutFormCollapse = new bootstrap.Collapse(checkoutFormCollapse, { toggle: false });
} catch (e) {
  console.warn("Bootstrap no disponible o elementos collapse no encontrados.", e);
}

/* Utilidades del carrito (UI) */
function isCartEmpty() {
  const totalSummaryElement = $id("total_sumary");
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
  [btnFinishOrder, btnBackStore, walletContainer, btnBackOnline, btnContinueCart, btnValidateData]
    .forEach(el => { if (el && el.classList) el.classList.add("d-none"); });
}

function initCartButtonState() {
  const cartIsEmptyFlag = isCartEmpty();

  if (btnContinueCart) {
    btnContinueCart.disabled = cartIsEmptyFlag;
    btnContinueCart.textContent = cartIsEmptyFlag ? "Carrito Vacío" : "Continuar Compra";
    btnContinueCart.classList.toggle("btn-success", !cartIsEmptyFlag);
    btnContinueCart.classList.toggle("btn-secondary", cartIsEmptyFlag);
  }
}

function showLocalCard(localId) {
  const localCard = $id("localCard");
  const localCardName = $id("localCardName");
  const localCardAddress = $id("localCardAddress");

  const select = $id("localSelect");
  if (!select) return;

  const selectedOption = select.options[select.selectedIndex];

  if (localId && selectedOption) {
    const nombre = selectedOption.getAttribute("data-nombre") || selectedOption.text;
    const ubicacion = selectedOption.getAttribute("data-ubicacion") || "";
    if (localCardName) localCardName.textContent = nombre;
    if (localCardAddress) localCardAddress.textContent = ubicacion;
    safeClassListRemove(localCard, "d-none");
  } else {
    safeClassListAdd(localCard, "d-none");
  }
}

/* Toggle collapse (si están presentes) */
function toggleCartCollapse() {
  const isCheckoutVisible = checkoutFormCollapse && checkoutFormCollapse.classList.contains("show");
  hideAllCheckoutButtons();

  if (isCheckoutVisible) {
    if (bsCheckoutFormCollapse) bsCheckoutFormCollapse.hide();
    if (bsCartListCollapse) bsCartListCollapse.show();
    safeClassListRemove(btnContinueCart, "d-none");
  } else {
    if (bsCartListCollapse) bsCartListCollapse.hide();
    if (bsCheckoutFormCollapse) bsCheckoutFormCollapse.show();

    if (paymentOnline && paymentOnline.checked) {
      safeClassListRemove(btnValidateData, "d-none");
      safeClassListRemove(btnBackOnline, "d-none");
    } else if (paymentStore && paymentStore.checked) {
      safeClassListRemove(btnFinishOrder, "d-none");
      safeClassListRemove(btnBackStore, "d-none");
    }
  }
}

/* Mostrar/ocultar botones según método de pago */
function updatePaymentButton() {
  const isStorePayment = paymentStore && paymentStore.checked;
  const isOnlinePayment = paymentOnline && paymentOnline.checked;

  hideAllCheckoutButtons();

  if (isStorePayment) {
    safeClassListRemove(btnFinishOrder, "d-none");
    safeClassListRemove(btnBackStore, "d-none");
    safeClassListAdd(btnValidateData, "d-none");
  } else if (isOnlinePayment) {
    safeClassListRemove(btnValidateData, "d-none");
    safeClassListRemove(btnBackOnline, "d-none");
  }
}

/* Mercado Pago SDK init */
const PUBLIC_KEY = window.MERCADOPAGO_PUBLIC_KEY;
let mp = null;

if (window.MercadoPago && PUBLIC_KEY) {
  try {
    mp = new window.MercadoPago(PUBLIC_KEY, { locale: "es-CL" });
  } catch (e) {
    console.error("Error inicializando MercadoPago SDK:", e);
  }
} else {
  console.warn("SDK de Mercado Pago no cargado o PUBLIC_KEY no definida.");
}

/* Mensajería */
function mostrarMensaje(mensaje, esError = true) {
  console.log(`${esError ? "ERROR" : "INFO"}: ${mensaje}`);
  if (esError) console.error(mensaje);
}

/* Render Wallet Brick */
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

/* Validaciones RUT / Teléfono */
function validarRut(rut) {
  if (!rut) return false;
  rut = rut.replace(/\./g, "").replace(/-/g, "").trim().toUpperCase();
  if (!/^(\d{7,8}[0-9K])$/.test(rut)) return false;

  const cuerpo = rut.slice(0, -1);
  const dv = rut.slice(-1);
  let suma = 0;
  let multiplo = 2;

  for (let i = cuerpo.length - 1; i >= 0; i--) {
    suma += parseInt(cuerpo.charAt(i), 10) * multiplo;
    multiplo = multiplo < 7 ? multiplo + 1 : 2;
  }

  const dvEsperado = 11 - (suma % 11);
  const dvFinal = dvEsperado === 11 ? "0" : dvEsperado === 10 ? "K" : String(dvEsperado);
  return dv === dvFinal;
}

function validarTelefono(telefono) {
  if (!telefono) return false;
  const regex = /^(?:\+?56)?(?:9\d{8}|[2-9]\d{7})$/;
  return regex.test(telefono.trim());
}

/* --- Consolidamos DOMContentLoaded en un único bloque --- */
document.addEventListener("DOMContentLoaded", function () {
  // Inicializaciones UI
  hideAllCheckoutButtons();
  initCartButtonState();

  // Si el collapse del listado está visible al inicio, mostrar botón continuar
  if (cartListCollapse && cartListCollapse.classList.contains("show")) {
    safeClassListRemove(btnContinueCart, "d-none");
    initCartButtonState();
  }

  // Listeners para mostrar datos del local (si existe select)
  const selectLocal = $id("localSelect");
  if (selectLocal) {
    selectLocal.addEventListener("change", () => showLocalCard(selectLocal.value));
    // Llamada inicial si hay valor
    if (selectLocal.value) showLocalCard(selectLocal.value);
  }

  // Manejo de colapsables (si existen)
  if (checkoutFormCollapse) {
    checkoutFormCollapse.addEventListener("shown.bs.collapse", function () {
      updatePaymentButton();
      if (paymentOnline) paymentOnline.addEventListener("change", updatePaymentButton);
      if (paymentStore) paymentStore.addEventListener("change", updatePaymentButton);
    });
  }

  if (cartListCollapse) {
    cartListCollapse.addEventListener("shown.bs.collapse", function () {
      hideAllCheckoutButtons();
      safeClassListRemove(btnContinueCart, "d-none");
      initCartButtonState();

      if (paymentOnline) paymentOnline.removeEventListener("change", updatePaymentButton);
      if (paymentStore) paymentStore.removeEventListener("change", updatePaymentButton);
    });
  }

  // Formulario y validaciones
  const pedidoForm = $id("pedidoForm");
  const continueBtn = btnContinueCart; // ya declarado arriba
  const checkoutBtn = walletContainer;

  if (pedidoForm) {
    // Validación RUT / Teléfono en inputs (si existen)
    const rutInput = $id("clientRut");
    const phoneInput = $id("clientPhone");
    if (rutInput) {
      rutInput.addEventListener("input", () => {
        rutInput.setCustomValidity("");
        const rutVal = rutInput.value.trim();
        if (rutVal && !validarRut(rutVal)) {
          rutInput.setCustomValidity("El RUT ingresado no es válido. Ejemplo correcto: 12.345.678-5");
        }
      });
    }
    if (phoneInput) {
      phoneInput.addEventListener("input", () => {
        phoneInput.setCustomValidity("");
        const phoneVal = phoneInput.value.trim();
        if (phoneVal && !validarTelefono(phoneVal)) {
          phoneInput.setCustomValidity("Ingresa un número de celular válido. Ejemplo: +56912345678 o 912345678");
        }
      });
    }

    pedidoForm.addEventListener("submit", (e) => {
      if (!pedidoForm.checkValidity()) {
        e.preventDefault();
        pedidoForm.reportValidity();
        alert("Por favor corrige los campos inválidos antes de continuar.");
      }
    });
  }

  // Botón continuar -> abre checkout
  if (continueBtn) {
    continueBtn.addEventListener("click", () => {
      if (bsCartListCollapse) bsCartListCollapse.hide();
      if (bsCheckoutFormCollapse) bsCheckoutFormCollapse.show();
      safeClassListAdd(continueBtn, "d-none");

      // mostrar botones según método seleccionado
      if (paymentOnline && paymentOnline.checked) {
        safeClassListRemove(btnValidateData, "d-none");
      } else {
        safeClassListAdd(btnValidateData, "d-none");
        safeClassListRemove(btnFinishOrder, "d-none");
        safeClassListRemove(btnBackStore, "d-none");
      }

      // Agregar validadores
      if (pedidoForm) {
        pedidoForm.querySelectorAll("input, select, textarea").forEach((input) => {
          input.addEventListener("input", () => {
            if (checkoutBtn) {
              const esValido = pedidoForm.checkValidity() && !isCartEmpty();
              safeToggleClass(checkoutBtn, "d-none", !esValido);
            }
          });
          input.addEventListener("change", () => {
            if (checkoutBtn) {
              const esValido = pedidoForm.checkValidity() && !isCartEmpty();
              safeToggleClass(checkoutBtn, "d-none", !esValido);
            }
          });
        });
      }
    });
  }

  // Si existe el contenedor del brick, no le pongas el listener de "click" (el brick lo maneja)
  // Antes en tu código había un listener que hacía fetch("/crear_preferencia/") sin temp_id -> lo removemos

  // Botón validar datos -> crea pedido temporal y preferencia
  if (btnValidateData) {
    btnValidateData.addEventListener("click", async function () {
      const pedidoFormLocal = $id("pedidoForm");
      if (!pedidoFormLocal) return;

      if (!pedidoFormLocal.checkValidity()) {
        pedidoFormLocal.reportValidity();
        mostrarMensaje("Por favor completa todos los campos requeridos antes de continuar.", true);
        return;
      }

      mostrarMensaje("Validando datos del pedido...", false);
      safeClassListAdd(btnValidateData, "d-none");

      const formData = new FormData(pedidoFormLocal);

      try {
        // 1️⃣ Crear pedido temporal (solo guarda datos) -> BACKEND devuelve { ok: true, temp_id }
        const responsePedido = await fetch("/crear-pedido/", {
          method: "POST",
          body: formData,
        });

        if (!responsePedido.ok) {
          const txt = await responsePedido.text().catch(() => null);
          mostrarMensaje("Error al procesar el pedido temporal. " + (txt || ""), true);
          safeClassListRemove(btnValidateData, "d-none");
          return;
        }

        const dataPedido = await responsePedido.json().catch(() => null);

        if (!dataPedido || !dataPedido.ok || !dataPedido.temp_id) {
          mostrarMensaje("No se pudo crear el pedido temporal.", true);
          console.error("Respuesta del pedido temporal:", dataPedido);
          safeClassListRemove(btnValidateData, "d-none");
          return;
        }

        // ✅ tempId ya definido aquí (evita ReferenceError)
        const tempId = dataPedido.temp_id;
        console.log("Enviando a /crear_preferencia/:", { temp_id: tempId });

        mostrarMensaje(`Pedido temporal creado. Generando preferencia de pago...`, false);

        // 2️⃣ Crear preferencia de Mercado Pago con temp_id
        const responsePref = await fetch("/crear_preferencia/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ temp_id: tempId }),
        });

        if (!responsePref.ok) {
          const txt = await responsePref.text().catch(() => null);
          mostrarMensaje("Error al generar preferencia de Mercado Pago. " + (txt || ""), true);
          safeClassListRemove(btnValidateData, "d-none");
          return;
        }

        const preference = await responsePref.json().catch(() => null);

        if (!preference || !preference.id) {
          mostrarMensaje("No se recibió ID de preferencia desde el servidor.", true);
          console.error("Respuesta de preferencia:", preference);
          safeClassListRemove(btnValidateData, "d-none");
          return;
        }

        // 3️⃣ Renderizar Wallet Brick con el id de preferencia
        await renderWalletBrick(preference.id);
        safeClassListRemove(walletContainer, "d-none");
        safeClassListRemove(btnBackOnline, "d-none");

        mostrarMensaje("Botón de Mercado Pago listo. Puedes proceder al pago.", false);
      } catch (err) {
        mostrarMensaje("Error al crear pedido temporal o preferencia de pago.", true);
        console.error(err);
        safeClassListRemove(btnValidateData, "d-none");
      }
    });
  }
});
