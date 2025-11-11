// Datos
  const labelsAnio = JSON.parse(document.getElementById('labels_ventas_anio_json').textContent);
  const dataAnio = JSON.parse(document.getElementById('data_ventas_anio_json').textContent);
  const labelsMes = JSON.parse(document.getElementById('labels_ventas_mes_json').textContent);
  const dataMes = JSON.parse(document.getElementById('data_ventas_mes_json').textContent);
  const labelsDia = JSON.parse(document.getElementById('labels_ventas_dia_json').textContent);
  const dataDia = JSON.parse(document.getElementById('data_ventas_dia_json').textContent);
  const labelsIngresos = JSON.parse(document.getElementById('labels_ingresos_json').textContent);
  const dataIngresos = JSON.parse(document.getElementById('data_ingresos_json').textContent);
  const labelsProductosMes = JSON.parse(document.getElementById('labels_productos_mes_json').textContent);
const datasetsProductosMes = JSON.parse(document.getElementById('datasets_productos_mes_json').textContent);

  new Chart(document.getElementById('ventasPorAnio'), {
      type: 'bar',
      data: { labels: labelsAnio, datasets: [{ label: 'Ventas Anuales', data: dataAnio, backgroundColor: 'rgba(54, 162, 235, 0.6)' }] }
  });
  new Chart(document.getElementById('ventasMes'), {
      type: 'bar',
      data: { labels: labelsMes, datasets: [{ label: 'Ventas Mensuales', data: dataMes, backgroundColor: 'rgba(255, 99, 132, 0.6)' }] }
  });
  new Chart(document.getElementById('ingresosPorTipo'), {
      type: 'pie',
      data: { labels: labelsIngresos, datasets: [{ label: 'Ingresos', data: dataIngresos, backgroundColor: ['rgba(54, 162, 235, 0.6)','rgba(255, 99, 132, 0.6)','rgba(75, 192, 192, 0.6)'] }] }
  });

  new Chart(document.getElementById('chartVentasAnio'), {
      type: 'bar',
      data: { labels: labelsAnio, datasets: [{ label: 'Ventas Anuales', data: dataAnio, backgroundColor: 'rgba(54, 162, 235, 0.6)' }] }
  });
  new Chart(document.getElementById('chartVentasMes'), {
      type: 'bar',
      data: { labels: labelsMes, datasets: [{ label: 'Ventas Mensuales', data: dataMes, backgroundColor: 'rgba(255, 99, 132, 0.6)' }] }
  });
  new Chart(document.getElementById('chartVentasDia'), {
      type: 'bar',
      data: { labels: labelsDia, datasets: [{ label: 'Ventas Diarias', data: dataDia, backgroundColor: 'rgba(75, 192, 192, 0.6)' }] }
  });

  new Chart(document.getElementById('productosPorMesLineas'), {
      type: 'line',
      data: {
          labels: labelsProductosMes,
          datasets: datasetsProductosMes.map(ds => ({
              label: ds.label,
              data: ds.data,
              borderColor: ds.backgroundColor,
              backgroundColor: ds.backgroundColor,
              fill: false,
              tension: 0.3,
              pointRadius: 5
          }))
      },
      options: {
          responsive: true,
          plugins: {
              tooltip: { mode: 'index', intersect: false },
              title: { display: true, text: 'Ventas por tipo de producto / mes' }
          },
          interaction: { mode: 'nearest', axis: 'x', intersect: false },
          scales: {
              x: { stacked: false },
              y: { beginAtZero: true }
          }
      }
  });