const open = document.getElementById('open');
const modal = document.getElementById('modal-container');
const close = document.getElementById('close');
const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))


open.addEventListener('click',()=>{
  modal-container.container.classList.add('show')
});


close.addEventListener('click',()=>{
  modal-container.container.classList.remove('show')
});



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
function showPopup() {
  document.getElementById("popup").style.display = "block";
}

// Fonction pour fermer le popup
function closePopup() {
  document.getElementById("popup").style.display = "none";
}

// Appel de la fonction showPopup lorsque la page est chargée (simulé ici)
window.onload = function() {
  showPopup();
};
