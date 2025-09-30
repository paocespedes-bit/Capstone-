document.addEventListener("DOMContentLoaded", function () {
    const wrapper = document.getElementById("wrapper");
    const toggler = document.getElementById("sidebar-toggler");

    if (toggler && wrapper) {
        toggler.addEventListener("click", function (e) {
            e.preventDefault();
            wrapper.classList.toggle("toggled");

        // Cambiar el ícono
        const icon = toggler.querySelector("i");
        if (wrapper.classList.contains("toggled")) {
            icon.classList.remove("bi-chevron-left");
            icon.classList.add("bi-chevron-right");
        } else {
            icon.classList.remove("bi-chevron-right");
            icon.classList.add("bi-chevron-left");
        }
        });
    }
});
