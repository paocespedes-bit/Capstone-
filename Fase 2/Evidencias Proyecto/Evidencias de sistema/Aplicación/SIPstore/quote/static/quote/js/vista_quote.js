document.addEventListener("DOMContentLoaded", function () {

  const tabs = document.querySelectorAll("#moduloTabs button");
  const currentModuloName = document.getElementById("currentModuloName");
  const currentModuloImage = document.getElementById("currentModuloImage");
  const imageMap = {
    Piso: "piso.png",
    "Muros Interiores": "muros.png",
    "Muros Exteriores": "muros.png",
    Cielo: "cielo.png",
    Aberturas: "aberturas.png",
  };
  const BASE_IMAGE_PATH = "/static/quote/img/";

  tabs.forEach((tab) => {
    tab.addEventListener("shown.bs.tab", function (event) {
      const tabText = event.target.textContent.trim();
      currentModuloName.textContent = tabText;
      const fileName = imageMap[tabText];
      if (fileName && currentModuloImage) {
        const newImagePath = BASE_IMAGE_PATH + fileName;
        currentModuloImage.src = newImagePath;
        currentModuloImage.alt = "Imagen de " + tabText;
      } else {
        console.warn("No se encontró imagen para la pestaña:", tabText);
      }
    });
  });


  const modulesConfig = [
    // MÓDULO PISO
    {
      prefix: "piso",
      title: "Piso",
      containerId: "piso-forms-container",
      templateId: "piso-form-template",
      buttonId: "add-piso-btn",
      fields: [
        { baseId: "pisoLargo", name: "largo" },
        { baseId: "pisoAncho", name: "ancho" },
        { baseId: "pisoTipoPanel", name: "tipoPanel", isSelect: true },
      ],
    },
    // MÓDULO MUROS EXTERIORES
    {
      prefix: "muros-ext", 
      title: "Muro Exterior",
      containerId: "muros-ext-forms-container",
      templateId: "muros-ext-form-template",
      buttonId: "add-muros-ext-btn",
      fields: [
        { baseId: "muroExtLargo", name: "largo" },
        { baseId: "muroExtAncho", name: "ancho" },
        { baseId: "muroExtTipoPanel", name: "tipoPanel", isSelect: true },
      ],
    },
    // MÓDULO MUROS INTERIORES
    {
      prefix: "muros-int", 
      title: "Muro Interior",
      containerId: "muros-int-forms-container",
      templateId: "muros-int-form-template",
      buttonId: "add-muros-int-btn",
      fields: [
        { baseId: "muroIntLargo", name: "largo" },
        { baseId: "muroIntAncho", name: "ancho" },
        { baseId: "muroIntTipoPanel", name: "tipoPanel", isSelect: true },
      ],
    },
    // MÓDULO CIELO
    {
      prefix: "cielo",
      title: "Cielo",
      containerId: "cielo-forms-container",
      templateId: "cielo-form-template",
      buttonId: "add-cielo-btn",
      fields: [
        { baseId: "cieloLargo", name: "largo" },
        { baseId: "cieloAncho", name: "ancho" },
        { baseId: "cieloTipoPanel", name: "tipoPanel", isSelect: true },
      ],
    },
    // MÓDULO ABERTURAS
    {
      prefix: "abertura",
      title: "Abertura",
      containerId: "abertura-forms-container",
      templateId: "abertura-form-template",
      buttonId: "add-abertura-btn",
      fields: [
        { baseId: "aberturaLargo", name: "largo" },
        { baseId: "aberturaAncho", name: "ancho" },
        { baseId: "aberturaTipoMuro", name: "tipoMuro", isSelect: true },
        { baseId: "aberturaMuro", name: "muroId", isSelect: true },
      ],
    },
  ];

  let globalCounter = 0;

  function assignUniqueIds(cardElement, fields) {
    globalCounter++;
    fields.forEach((field) => {
      const labelSelector = `label[for^="${field.baseId}"]`;
      const inputSelector = field.isSelect
        ? `select[name="${field.name}"]`
        : `input[name="${field.name}"]`;

      const label = cardElement.querySelector(labelSelector);
      const input = cardElement.querySelector(inputSelector);

      const uniqueId = `${field.baseId}-${globalCounter}`;

      if (label && input) {
        label.setAttribute("for", uniqueId);
        input.setAttribute("id", uniqueId);
      }
    });
  }

  /**
   * @param {Object} config - Objeto de configuración del módulo.
   */
  function handleModuleLogic(config) {
    const container = document.getElementById(config.containerId);
    const emptyState = document.getElementById(`${config.prefix}-empty-state`);
    const template = document.getElementById(config.templateId);
    const addButton = document.getElementById(config.buttonId);

    if (!container || !template || !addButton || !emptyState) {
      console.error(
        `ERROR CRÍTICO: Faltan elementos HTML para el módulo: ${config.title}. Verifique IDs y prefixes.`,
        config
      );
      return;
    }

    function updateOrder() {
      const items = container.querySelectorAll(".item-card");

      if (items.length === 0) {
        if (emptyState) emptyState.style.display = "block";
      } else {
        if (emptyState) emptyState.style.display = "none";

        items.forEach((item, index) => {
          const numberElement = item.querySelector(".item-number");
          const titleElement = item.querySelector("h5");

          const newNumber = index + 1;

          if (numberElement) {
            numberElement.textContent = newNumber; 
          }

          if (titleElement) {
            titleElement.textContent = `${config.title} - ${newNumber}`;
          }
        });
      }
    }

    addButton.addEventListener("click", function () {
      const clone = template.content.cloneNode(true);
      const newCard = clone.querySelector(".item-card");

      assignUniqueIds(newCard, config.fields);

      container.appendChild(newCard);
      updateOrder();
    });

    container.addEventListener("click", function (event) {
      if (event.target.closest(".delete-btn")) {
        const cardToRemove = event.target.closest(".item-card");

        if (cardToRemove) {
          cardToRemove.remove();
          updateOrder();
        }
      }
    });

    updateOrder();
  }

  modulesConfig.forEach((config) => handleModuleLogic(config));
});
