document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

});

 // Setter and getter functions
 function setRead(id){
  fetch(`/emails/${id}`, {
  method: 'PUT',
  body: JSON.stringify({
      read: true})
  });
}

function setArchived(id){
  fetch(`/emails/${id}`, {
  method: 'PUT',
  body: JSON.stringify({
      archived: true  })
  });
}


function compose_email() { //Load view and listening submit
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#single-email-view').style.display = 'none';

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
          console.log(result.message);
          load_mailbox('sent');
        }
    });
    
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-email-view').style.display = 'none';

  // Show the mailbox name
  var body = document.querySelector('#emails-view');
  body.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //GET the emails
  console.log("Loading "+mailbox);
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    //Each element of the array will be passed to the function
    emails.forEach(data => addMail(data, mailbox))
  });
}

function addMail(element, box){
  const div = document.createElement('div');
  div.className = 'div-mail';
  let unread_class = element.read? "email-view-read" : "email-view-unread";
  div.className = `row border border-dark rounded email-view ${unread_class}`;

  if (box === 'inbox')
    div.innerHTML = '<a>From: </a><b id="sender">' + element.sender + ' </b>';
  else if (box === 'sent')
    div.innerHTML = '<a>To: </a><b id="recipients">' + element.recipients + ' </b>';

  div.innerHTML += '<a id="subject">' + element.subject +' </a>';
  div.innerHTML += '<a id="timestamp">' + element.timestamp +' </a>';
  document.querySelector('#emails-view').appendChild(div);
  div.addEventListener('click', ()=> showMail(element.id));
}

function showMail(id){
  console.log("Clicked on :"+id);
  viewMail(id);
}

function viewMail(id){
  // Clear previous data (if exist)
  document.querySelector('#single-email-view').innerHTML = '';
  
  // Show the email and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-email-view').style.display = 'block';

  const div = document.createElement('div');

  const btnReply = document.createElement('button');
    btnReply.className = "btn btn-sm btn-outline-primary";
    btnReply.innerHTML = "Archive";
    btnReply.addEventListener('click', ()=> setArchived(id));
    document.querySelector('#single-email-view').appendChild(btnReply);

  // GET to fetch the data
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
     //create the view and load the data
     div.innerHTML = '<p>From: <b id="sender">' + email.sender + ' </b></p>';
     div.innerHTML += '<p>Recipients: <b id="recipients">' + email.sender + ' </b></p>';
     div.innerHTML += '<p>Subject: ' + email.subject + '  <b id="timestamp">'+email.timestamp+'</b></p>';
     div.innerHTML += '<p>Body: ' + email.body + ' </p>';
    
     document.querySelector('#single-email-view').appendChild(div);
  });
  
  

}