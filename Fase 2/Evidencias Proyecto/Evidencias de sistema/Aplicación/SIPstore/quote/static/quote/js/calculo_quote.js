document.addEventListener("DOMContentLoaded", () => {
  const btnCalcular = document.getElementById("btn-calcular");
  const btnLimpiar = document.getElementById("btn-limpiar");
  const calculoTable = document.querySelector(".card-body table");

  // Guardar formulario temporalmente (cada vez que se presione el check)
  document.body.addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = e.target.closest("form");
    if (!form) return;

    const card = form.closest(".item-card");
    const module = card?.dataset.module;
    const formData = Object.fromEntries(new FormData(form).entries());

    const response = await fetch("/quote/save_temp_form/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken(),
      },
      body: JSON.stringify({ module, data: formData }),
    });

    const data = await response.json();
    if (data.message) console.log(data.message);
  });

  // Botón Calcular
  btnCalcular.addEventListener("click", async () => {
    const response = await fetch("/quote/calcular_materiales/", {
      method: "POST",
      headers: {
        "X-CSRFToken": getCSRFToken(),
      },
    });
    const data = await response.json();
    calculoTable.innerHTML = data.html;
  });

  // Botón Limpiar
  btnLimpiar.addEventListener("click", async () => {
    await fetch("/quote/limpiar_calculo/", {
      method: "POST",
      headers: {
        "X-CSRFToken": getCSRFToken(),
      },
    });
    calculoTable.innerHTML =
      "<tbody><tr><td colspan='5' class='text-center text-muted py-3'>Cálculo limpiado</td></tr></tbody>";
  });

  // Función para CSRF
  function getCSRFToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]")?.value;
  }
});
