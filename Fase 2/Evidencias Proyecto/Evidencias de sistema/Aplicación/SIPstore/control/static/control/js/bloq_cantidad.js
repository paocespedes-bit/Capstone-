document.addEventListener("DOMContentLoaded", function () {
  const radioBloquea = document.querySelectorAll(".radio-bloquea-cantidad");
  const radioDesbloquea = document.querySelectorAll(
    ".radio-desbloquea-cantidad"
  );

  function getCantidadInput(radioInput) {
    const form = radioInput.closest("form");
    if (form) {
      return form.querySelector(".input-cantidad-inventario");
    }
    return null;
  }

  function controlarInput(deshabilitar, radioInput) {
    const cantidadInput = getCantidadInput(radioInput);
    if (cantidadInput) {
      cantidadInput.disabled = deshabilitar;
    }
  }

  radioBloquea.forEach((radio) => {
    radio.addEventListener("change", function () {
      if (this.checked) {
        controlarInput(true, this);
      }
    });
  });

  radioDesbloquea.forEach((radio) => {
    radio.addEventListener("change", function () {
      if (this.checked) {
        controlarInput(false, this);
      }
    });
  });

  document.querySelectorAll(".input-cantidad-inventario").forEach((input) => {
    const form = input.closest("form");
    if (form) {
      const pedidoRadio = form.querySelector(".radio-bloquea-cantidad");
      if (pedidoRadio && pedidoRadio.checked) {
        input.disabled = true;
        input.value = 0;
      }
    }
  });
});
