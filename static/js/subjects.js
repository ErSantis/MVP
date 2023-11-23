document.addEventListener('DOMContentLoaded', function () {
    // Obtener todas las cartas y agregar el evento de clic a cada una
    var cards = document.querySelectorAll('.card');

    cards.forEach(function (card) {
        // Verificar si el ID cumple con ciertos criterios (por ejemplo, si contiene '_dynamic')

        card.addEventListener('click', function () {
            // Acción a realizar cuando se hace clic en una carta
            console.log(card);
            var cardName = card.id.split('_')[1];
            var smallContent = card.querySelector('.nrc').innerText;

            // Redirigir a la página correspondiente
            window.location.href = '/subjects/' + cardName + '/' + smallContent;
        });

    });
});
