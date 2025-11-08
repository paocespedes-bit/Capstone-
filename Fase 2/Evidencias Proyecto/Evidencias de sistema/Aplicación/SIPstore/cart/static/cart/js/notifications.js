// Mostrar Toast de notificación

const mostrarToast = (mensaje) => {
    const toastEl = document.getElementById("toast");
    const toastBody = document.getElementById("toast-body");
    if (!toastEl || !toastBody) return;

    toastBody.textContent = mensaje;
    new bootstrap.Toast(toastEl).show();
};

// Actualizar contador del carrito (badge)
const actualizarBadge = (cantidad) => {
    const badge = document.getElementById("contar_carrito");
    if (badge) badge.textContent = cantidad;
};
