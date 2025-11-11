// === Calculo Quote Principal ===
document.addEventListener("DOMContentLoaded", () => {
  const btnCalcular = document.getElementById("btn-calcular");
  const btnLimpiar = document.getElementById("btn-limpiar");
  const calculoTable = document.querySelector(".card-body table");

  // Registro de muros locales (solo para llenar selects)
  const muros = {
    interior: [],
    exterior: [],
  };

  // === Guardar formulario temporalmente ===
  document.body.addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = e.target.closest("form");
    if (!form) return;

    const inputs = form.querySelectorAll("input, select");
    let isValid = true;

    // Validación visual Bootstrap
    inputs.forEach((input) => {
      const value = input.value?.trim();
      if (!value || value === "" || input.selectedIndex === 0) {
        input.classList.remove("is-valid");
        input.classList.add("is-invalid");
        isValid = false;
      } else {
        input.classList.remove("is-invalid");
        input.classList.add("is-valid");
      }
    });

    if (!isValid) {
      form.classList.add("was-validated");
      return;
    }

    const card = form.closest(".item-card");
    const module = card?.dataset.module;
    const formData = Object.fromEntries(new FormData(form).entries());
    const formKey = `${module}-${Object.values(formData).join("-")}`;
    if (card.dataset.savedKey === formKey) return;

    // Registrar muros locales para usarlos en el formulario de abertura
    if (module === "muros-int" || module === "muros-ext") {
      const tipo = module === "muros-int" ? "interior" : "exterior";
      const largo = parseFloat(formData.largo) || 0;
      const alto = parseFloat(formData.alto) || 0;
      const area = largo * alto;
      const muroId = `${tipo}-${muros[tipo].length + 1}`;

      const muroExistente = muros[tipo].find(
        (m) => m.largo === largo && m.alto === alto
      );
      if (!muroExistente) {
        muros[tipo].push({
          id: muroId,
          nombre: `Muro ${muros[tipo].length + 1}`,
          area,
          largo,
          alto,
        });
      }
    }

    // Enviar datos al backend
    const response = await fetch("/quote/save_temp_form/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken(),
      },
      body: JSON.stringify({ module, data: formData }),
    });

    const data = await response.json();
    if (response.ok) {
      card.dataset.savedKey = formKey;
      showAlert("Formulario guardado correctamente ✅", "success", card);
    } else {
      showAlert("Ocurrió un error al guardar ❌", "danger", card);
    }
  });

  // === Cargar dinámicamente muros en Abertura según tipo ===
  document.body.addEventListener("change", (e) => {
    if (e.target.name === "tipoMuro") {
      const tipoSeleccionado =
        e.target.value === "Muro Interior" ? "interior" : "exterior";
      const muroSelect = e.target
        .closest("form")
        .querySelector('select[name="muroId"]');

      muroSelect.innerHTML =
        '<option value="" selected disabled>Elige el Muro</option>';

      muros[tipoSeleccionado].forEach((muro) => {
        const option = document.createElement("option");
        option.value = muro.id;
        option.textContent = `${muro.nombre} (Área: ${muro.area.toFixed(
          2
        )} m²)`;
        muroSelect.appendChild(option);
      });
    }
  });

  // === Botón Calcular ===
  btnCalcular.addEventListener("click", async () => {
    const response = await fetch("/quote/calcular_materiales/", {
      method: "POST",
      headers: { "X-CSRFToken": getCSRFToken() },
    });
    const data = await response.json();
    calculoTable.innerHTML = data.html;
  });

  // === Botón Limpiar ===
  btnLimpiar.addEventListener("click", async () => {
    await fetch("/quote/limpiar_calculo/", {
      method: "POST",
      headers: { "X-CSRFToken": getCSRFToken() },
    });
    calculoTable.innerHTML =
      "<tbody><tr><td colspan='5' class='text-center text-muted py-3'>Cálculo limpiado</td></tr></tbody>";
  });

  // === CSRF Token ===
  function getCSRFToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]")?.value;
  }
});

// === Alerta Temporal ===
function showAlert(message, type = "info", parent) {
  const existing = parent.querySelector(".temp-alert");
  if (existing) existing.remove();
  const alert = document.createElement("div");
  alert.className = `alert alert-${type} temp-alert mt-3`;
  alert.role = "alert";
  alert.textContent = message;
  parent.appendChild(alert);
  setTimeout(() => alert.remove(), 3000);
}
