document.addEventListener('DOMContentLoaded', function() {

});

document.querySelector('#newpost-form').addEventListener('submit', () =>{
    e.preventDefault;
    console.log("New post sent!");
    document.querySelector('textarea').innerHTML = '';
});