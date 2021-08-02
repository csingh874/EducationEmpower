var exampleModal = document.getElementById('exampleModal');
exampleModal.addEventListener('show.bs.modal', function (event) {
  var button = event.relatedTarget;
  var url = button.getAttribute('data-bs-url');
  console.log(url);
  exampleModal.querySelector("#modalbody").innerHTML = url;
})