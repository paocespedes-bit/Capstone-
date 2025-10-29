/**
 * Inicializa un carrusel de bucle infinito para un contenedor específico.
 * @param {string} containerSelector El selector (ID o Clase) del contenedor principal del carrusel.
 * @param {number} CLONE_COUNT La cantidad de tarjetas a clonar en cada extremo.
 * @param {number} transitionMs La duración de la transición en milisegundos.
 * @param {number} autoplayMs El intervalo de auto-reproducción en milisegundos.
 */
function initInfiniteCarousel(
  containerSelector,
  CLONE_COUNT = 2,
  transitionMs = 500,
  autoplayMs = 3500
) {
  // 1. Aislamiento de Elementos: Buscar dentro del contenedor específico
  const container = document.querySelector(containerSelector);
  if (!container) {
    console.error(`Contenedor de carrusel no encontrado: ${containerSelector}`);
    return;
  }

  const track = container.querySelector(".card-track");
  const prevBtn = container.querySelector(".carousel-btn.prev");
  const nextBtn = container.querySelector(".carousel-btn.next");

  // Inicialización de variables locales
  let items = Array.from(container.querySelectorAll(".card-item"));
  let isAnimating = false;
  let autoTimer = null;
  let cardWidth = 0;
  let index = 0;

  // Guardrail: No inicializar si no hay suficientes tarjetas reales
  if (items.length < CLONE_COUNT + 1) {
    console.warn(
      `No hay suficientes ítems (${items.length}) en ${containerSelector} para CLONE_COUNT=${CLONE_COUNT}.`
    );
    // Opcional: deshabilitar botones si no hay suficiente contenido
    if (prevBtn) prevBtn.style.display = "none";
    if (nextBtn) nextBtn.style.display = "none";
    return;
  }

  // --- FUNCIONES INTERNAS (Sin cambios mayores en la lógica) ---

  function calcCardWidth() {
    const node = items[0];
    const style = getComputedStyle(node);
    const marginLeft = parseFloat(style.marginLeft) || 0;
    const marginRight = parseFloat(style.marginRight) || 0;
    return Math.round(node.offsetWidth + marginLeft + marginRight);
  }

  function setupClones() {
    // Limpiar clones anteriores si la función se llama varias veces (aunque no debería ser el caso aquí)
    items = Array.from(container.querySelectorAll(".card-item"));
    const realItemsCount = items.length;

    // 1. Clonar los ÚLTIMOS items y colocarlos al inicio
    for (let i = 1; i <= CLONE_COUNT; i++) {
      const itemToClone = items[realItemsCount - i];
      const clone = itemToClone.cloneNode(true);
      track.insertBefore(clone, track.firstChild);
    }

    // 2. Clonar los PRIMEROS items y colocarlos al final
    for (let i = 0; i < CLONE_COUNT; i++) {
      const itemToClone = items[i];
      const clone = itemToClone.cloneNode(true);
      track.appendChild(clone);
    }

    // Refrescar listado de items: (Clones iniciales) + (Reales) + (Clones finales)
    items = Array.from(container.querySelectorAll(".card-item"));
  }

  function moveToIndex(anim = true) {
    if (anim) {
      track.style.transition = `transform ${transitionMs}ms ease`;
    } else {
      track.style.transition = "none";
    }
    track.style.transform = `translateX(-${index * cardWidth}px)`;
  }

  // 2. Lógica de Bucle
  track.addEventListener("transitionend", () => {
    const lastRealIndex = items.length - CLONE_COUNT - 1;

    if (index >= lastRealIndex + 1) {
      index = CLONE_COUNT;
      moveToIndex(false);
    } else if (index < CLONE_COUNT) {
      index = lastRealIndex;
      moveToIndex(false);
    }

    isAnimating = false;
  });

  // 3. Navegación
  function next() {
    if (isAnimating) return;
    isAnimating = true;
    index++;
    moveToIndex(true);
  }

  function prev() {
    if (isAnimating) return;
    isAnimating = true;
    index--;
    moveToIndex(true);
  }

  if (nextBtn)
    nextBtn.addEventListener("click", () => {
      stopAutoplay();
      next();
      startAutoplay();
    });

  if (prevBtn)
    prevBtn.addEventListener("click", () => {
      stopAutoplay();
      prev();
      startAutoplay();
    });

  // 4. Autoplay
  function startAutoplay() {
    if (autoTimer) clearInterval(autoTimer);
    autoTimer = setInterval(() => {
      if (!isAnimating) next();
    }, autoplayMs);
  }
  function stopAutoplay() {
    if (autoTimer) clearInterval(autoTimer);
    autoTimer = null;
  }

  container.addEventListener("mouseenter", stopAutoplay);
  container.addEventListener("mouseleave", startAutoplay);

  // 5. Ajuste en Resize
  let resizeTimeout;
  window.addEventListener("resize", () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
      const newWidth = calcCardWidth();
      cardWidth = newWidth;
      index = Math.max(
        CLONE_COUNT,
        Math.min(index, items.length - CLONE_COUNT - 1)
      );
      moveToIndex(false);
    }, 120);
  });

  // --- INICIALIZACIÓN ---
  setupClones();
  cardWidth = calcCardWidth();
  index = CLONE_COUNT;
  track.style.transition = "none";
  track.style.transform = `translateX(-${index * cardWidth}px)`;
  startAutoplay();
}
