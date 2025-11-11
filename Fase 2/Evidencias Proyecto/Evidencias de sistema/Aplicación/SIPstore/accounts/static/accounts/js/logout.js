document.addEventListener('DOMContentLoaded', function() {
    
    const countdownElement = document.getElementById('countdown');
    
    const loginUrl = countdownElement.dataset.loginUrl;
    
    let countdown = 5; 

    function updateCountdown() {
        countdownElement.textContent = countdown;
        countdown--;
        
        if (countdown < 0) {
            window.location.href = loginUrl;
        } else {

            setTimeout(updateCountdown, 1000);
        }
    }
    updateCountdown(); 
});