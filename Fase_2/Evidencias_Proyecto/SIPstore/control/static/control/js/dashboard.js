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

  // ====== Ventas del mes ======
  const ventasMesCanvas = document.getElementById('ventasMes');
  if (ventasMesCanvas) {
    const labelsVentasMes = JSON.parse(ventasMesCanvas.dataset.labelsMes);
    const dataVentasMes = JSON.parse(ventasMesCanvas.dataset.valuesMes);

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
  }

  // ====== TOP productos ======
  const topProductosCanvas = document.getElementById('topProductos');
  if (topProductosCanvas) {
    const labelsTop = JSON.parse(topProductosCanvas.dataset.labels);
    const dataTop = JSON.parse(topProductosCanvas.dataset.values);

    new Chart(topProductosCanvas.getContext('2d'), {
      type: 'bar',
      data: {
        labels: labelsTop,
        datasets: [{
          label: 'Productos más vendidos',
          data: dataTop,
          backgroundColor: [
            'rgba(255, 99, 132, 0.7)',
            'rgba(54, 162, 235, 0.7)',
            'rgba(255, 206, 86, 0.7)',
            'rgba(75, 192, 192, 0.7)',
            'rgba(153, 102, 255, 0.7)',
          ],
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        scales: { 
          y: { beginAtZero: true, title: { display: true, text: 'Cantidad vendida' } },
          x: { title: { display: true, text: 'Productos' } }
        },
        plugins: { legend: { display: false }, tooltip: { enabled: true } }
      }
    });
  }
});
