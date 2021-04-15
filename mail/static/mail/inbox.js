document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

});

function compose_email() { //Load view and listening submit 
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Listening if the compose-form is submited
  document.querySelector("#compose-form").onsubmit = send_mail;
}
  
function send_mail(event){// To POST an email to the API and check if sent
  event.preventDefault();
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
        if (result.error){
          alert(result.error); 
        }
        else{
          console.log("Message sent sucessfully");
        }
    });
    load_mailbox('sent'); //TODO: After this, the mailbox is loaded too.
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  var body = document.querySelector('#emails-view'); 
  body.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //GET the emails
  console.log("Loading "+mailbox);
  fetch(`/emails/${mailbox}`)
.then(response => response.json())
.then(emails => {
    emails.forEach(data => addMail(data, mailbox))
});
}

function addMail(element, box){
  const div = document.createElement('div');
  div.className = 'div-mail';
  if (element.read === 'false'){
    div.style.backgroundColor = "green";
    div.className += 'unreaded'; //NotWorking
  }

  if (box === 'inbox')
    div.innerHTML = '<a>From: </a><b id="sender">' + element.sender + ' </b>';
  else if (box === 'sent')
    div.innerHTML = '<a>To: </a><b id="recipients">' + element.recipients + ' </b>';
  
  div.innerHTML += '<a id="subject">' + element.subject +' </a>';
  div.innerHTML += '<a id="date">' + element.timestamp +' </a>';
  document.querySelector('#emails-view').append(div);
}

function readMail(id){
  alert("Email #"+id);
}