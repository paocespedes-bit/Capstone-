document.addEventListener("DOMContentLoaded", () => {
    // !encuentra el contenedor .quantity
    const quantityContainers = document.querySelectorAll(".quantity");
    // !busca las constantes y las selecciona
    quantityContainers.forEach((container) => {
        const botonMenos = container.querySelector("button:first-of-type");
        const botonMas = container.querySelector("button:last-of-type");
        const spanCantidad = container.querySelector("span");
        // !disminuye la cantidad del span
        botonMenos.addEventListener("click", () => {
            let cantidadActual = parseInt(spanCantidad.textContent);
            if (cantidadActual > 1) {
                spanCantidad.textContent = cantidadActual - 1;
            }
        });
        // !aumenta la cantidad del span
        botonMas.addEventListener("click", () => {
            let cantidadActual = parseInt(spanCantidad.textContent);
            spanCantidad.textContent = cantidadActual + 1;
        });
    });
});
