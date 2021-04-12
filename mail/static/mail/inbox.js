document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector("#compose-form").onsubmit = send_mail;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}
  
// To POST an email to the API
function send_mail(){
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });
    
}


function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  var body = document.querySelector('#emails-view'); 
  body.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //GET the emails
  fetch(`/emails/${mailbox}`)
.then(response => response.json())
.then(emails => {
    // Print emails in console
    console.log(emails);
    for (var each in emails){
      let mail = emails[each];
      addMail(mail);
    }
  
});
}

function addMail(element){
  const div = document.createElement('div');
  div.className = 'div-mail';
  div.innerHTML = '<a id="sender">' + element.sender + ' </a>';
  div.innerHTML += '<a id="subject">' + element.subject +' </a>';
  div.innerHTML += '<a id="date">' + element.timestamp +' </a>';
  document.querySelector('#emails-view').append(div);
}
