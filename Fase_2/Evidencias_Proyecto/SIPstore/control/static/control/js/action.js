document.querySelectorAll(".btn-eliminar").forEach((button) => {
  button.addEventListener("click", () => {
    const nombre = button.getAttribute("data-nombre");
    const tipo = button.getAttribute("data-tipo");
    const url = button.getAttribute("data-url");

    // Actualizar el contenido del modal
    document.getElementById(
      "modalTextEliminar"
    ).textContent = `¿Estás seguro de eliminar "${nombre}" (${tipo})?`;

    // Actualizar el formulario con la URL correcta
    document.getElementById("formEliminar").setAttribute("action", url);
  });
});
