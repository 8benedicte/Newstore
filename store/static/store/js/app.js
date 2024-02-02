const open = document.getElementById('open');
const modal = document.getElementById('modal-container');
const close = document.getElementById('close');



open.addEventListener('click',()=>{
  modal-container.container.classList.add('show')
});


close.addEventListener('click',()=>{
  modal-container.container.classList.remove('show')
});

const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))

const myModal = document.getElementById('myModal')
const myInput = document.getElementById('myInput')

myModal.addEventListener('shown.bs.modal', () => {
  myInput.focus()
})


const alertPlaceholder = document.getElementById('liveAlertPlaceholder')
const appendAlert = (message, type) => {
  const wrapper = document.createElement('div')
  wrapper.innerHTML = [
    `<div class="alert alert-${type} alert-dismissible" role="alert">`,
    `   <div>${message}</div>`,
    '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
    '</div>'
  ].join('')

  alertPlaceholder.append(wrapper)
}

const alertTrigger = document.getElementById('liveAlertBtn')
if (alertTrigger) {
  alertTrigger.addEventListener('click', () => {
    appendAlert('Nice, you triggered this alert message!', 'success')
  })
}
// Fonction pour afficher le popup
// JavaScript
function showPopup() {
    document.getElementById("popup").style.display = "block";
    document.body.classList.add('popup-open'); // Ajoute la classe 'popup-open' au body
}

function closePopup() {
    document.getElementById("popup").style.display = "none";
    document.body.classList.remove('popup-open'); // Supprime la classe 'popup-open' du body
    window.removeEventListener('click', preventClick); // Supprime l'écouteur d'événement sur le clic une fois le popup fermé

    // Enregistre l'état du popup comme fermé dans un cookie expirant à la fin de la session
    document.cookie = "popupClosed=true; expires=session";
}

function preventClick(event) {
    if (!document.getElementById('popup').contains(event.target)) {
        event.stopPropagation(); // Empêche la propagation du clic en dehors du popup
    }
}

window.addEventListener('click', preventClick); // Ajoute un écouteur d'événement sur le clic pour empêcher la propagation du clic en dehors du popup

// Vérifie si le popup a été fermé précédemment
window.onload = function() {
    if (document.cookie.indexOf("popupClosed=true") !== -1) {
        closePopup(); // Ferme le popup si son état précédent était fermé
    } else {
        showPopup(); // Affiche le popup s'il n'a pas été fermé précédemment
    }
};



