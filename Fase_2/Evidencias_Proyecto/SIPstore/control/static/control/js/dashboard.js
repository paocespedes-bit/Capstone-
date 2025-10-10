document.addEventListener('DOMContentLoaded', function() {

 // ====== Total ventas por año ======
const ventasPorAnioCanvas = document.getElementById('ventasPorAnio');
if (ventasPorAnioCanvas) {
  const labelsVentasAnio = JSON.parse(ventasPorAnioCanvas.dataset.labels);
  const dataVentasAnio = JSON.parse(ventasPorAnioCanvas.dataset.values);

  new Chart(ventasPorAnioCanvas.getContext('2d'), {
    type: 'bar',
    data: {
      labels: labelsVentasAnio,
      datasets: [{
        label: 'Ventas por año',
        data: dataVentasAnio,
        backgroundColor: 'rgba(54, 162, 235, 0.7)'
      }]
    },
    options: {
      responsive: true,
      scales: { y: { beginAtZero: true } }
    }
  });
}

  // ====== TOP 3 productos ======
  const topProductosCanvas = document.getElementById('topProductos');
  const labelsTopProductos = JSON.parse(topProductosCanvas.dataset.labels);
  const dataTopProductos = JSON.parse(topProductosCanvas.dataset.values);

  new Chart(topProductosCanvas.getContext('2d'), {
    type: 'bar',
    data: {
      labels: labelsTopProductos,
      datasets: [{
        label: 'Cantidad vendida',
        data: dataTopProductos,
        backgroundColor: 'rgba(255, 206, 86, 0.7)'
      }]
    },
    options: {
      responsive: true,
      scales: { y: { beginAtZero: true } }
    }
  });

  // ====== 3. Ventas del mes ======
  const ventasMesCanvas = document.getElementById('ventasMes');
  const labelsVentasMes = JSON.parse(ventasMesCanvas.dataset.labels);
  const dataVentasMes = JSON.parse(ventasMesCanvas.dataset.values);

  new Chart(ventasMesCanvas.getContext('2d'), {
    type: 'line',
    data: {
      labels: labelsVentasMes,
      datasets: [{
        label: 'Ventas del mes',
        data: dataVentasMes,
        borderColor: 'rgba(255, 99, 132, 1)',
        fill: false,
        tension: 0.3
      }]
    },
    options: {
      responsive: true,
      scales: { y: { beginAtZero: true } }
    }
  });
});
