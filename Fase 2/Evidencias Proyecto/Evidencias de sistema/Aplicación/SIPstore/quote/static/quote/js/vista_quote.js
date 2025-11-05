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
        console.error("No se encontró imagen para la pestaña:", tabText);
      }
    });
  });

});
