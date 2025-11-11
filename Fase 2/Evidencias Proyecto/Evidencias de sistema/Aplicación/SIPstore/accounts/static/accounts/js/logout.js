document.addEventListener('DOMContentLoaded', function() {
    
    const countdownElement = document.getElementById('countdown');
    
    // Obtenemos la URL de login desde el atributo data-*
    const loginUrl = countdownElement.dataset.loginUrl;
    
    let countdown = 5; // Empieza en 5 segundos
    
    // Función para actualizar la cuenta regresiva
    function updateCountdown() {
        countdownElement.textContent = countdown;
        countdown--;
        
        if (countdown < 0) {
            // Redirigir al login usando la URL que obtuvimos
            window.location.href = loginUrl;
        } else {
            // Esperar 1 segundo y llamar de nuevo a la función
            setTimeout(updateCountdown, 1000);
        }
    }
    
    // Iniciar la cuenta regresiva
    updateCountdown(); 
});