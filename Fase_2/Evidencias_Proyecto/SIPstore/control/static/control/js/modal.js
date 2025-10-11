document.addEventListener('DOMContentLoaded', function() {
  const modal = document.getElementById('modalVentas');
  const btnVentasAnio = document.getElementById('ventasPorAnio');
  const spanClose = modal.querySelector('.close');

  let chartAnio, chartMes, chartDia;

  btnVentasAnio.addEventListener('click', () => {
    modal.style.display = 'block';

    const labelsAnio = JSON.parse(btnVentasAnio.dataset.labels);
    const dataAnio = JSON.parse(btnVentasAnio.dataset.values);

    const labelsMes = JSON.parse(btnVentasAnio.dataset.labelsMes);
    const dataMes = JSON.parse(btnVentasAnio.dataset.valuesMes);

    const labelsDia = JSON.parse(btnVentasAnio.dataset.labelsDia);
    const dataDia = JSON.parse(btnVentasAnio.dataset.valuesDia);

    // Ventas por año
    if(!chartAnio) {
      chartAnio = new Chart(document.getElementById('chartVentasAnio').getContext('2d'), {
        type: 'bar',
        data: { labels: labelsAnio, datasets: [{ label: 'Ventas por año', data: dataAnio, backgroundColor: 'rgba(54, 162, 235, 0.7)' }] },
        options: { responsive: true, scales: { y: { beginAtZero: true } } }
      });
    }

    // Ventas por mes
    if(!chartMes) {
      chartMes = new Chart(document.getElementById('chartVentasMes').getContext('2d'), {
        type: 'bar',
        data: { labels: labelsMes, datasets: [{ label: 'Ventas por mes', data: dataMes, backgroundColor: 'rgba(0,140,158,0.7)' }] },
        options: { responsive: true, scales: { y: { beginAtZero: true } } }
      });
    }

    // Ventas por día
    if(!chartDia) {
      chartDia = new Chart(document.getElementById('chartVentasDia').getContext('2d'), {
        type: 'line',
        data: { labels: labelsDia, datasets: [{ label: 'Ventas por día', data: dataDia, borderColor: 'rgba(255, 99, 132, 1)', fill: false, tension: 0.3 }] },
        options: { responsive: true, scales: { y: { beginAtZero: true } } }
      });
    }
  });

  spanClose.onclick = () => { modal.style.display = 'none'; }
  window.onclick = (event) => { if(event.target == modal) modal.style.display = 'none'; }
});
