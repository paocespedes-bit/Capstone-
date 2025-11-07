function enviarCotizacion() {
  const correo = document.getElementById("correoCliente").value.trim();
  if (!correo) {
    alert("Por favor ingresa un correo válido");
    return;
  }

  fetch("{% url 'enviar_cotizacion' %}", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({correo})
  })
  .then(r => r.json())
  .then(data => {
    if (data.message) alert(data.message);
    else if (data.error) alert(data.error);
  })
  .catch(() => alert("Error al enviar la cotización"));
}