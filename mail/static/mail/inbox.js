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
  document.querySelector('#reading-view').style.display = 'none';
  document.querySelector('#not_sent').style.display = 'none'; // Dont show the alert! (yet)

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
          /* Bootstrap Alert
          document.querySelector('#not_sent').innerHTML = `<a>${result.error}</a>`;
          document.querySelector('#not_sent').style.display = 'block';
          setTimeout( ()=> { // This isn't accesible! 
              document.querySelector('#not_sent').style.display = 'none';
              document.querySelector('#compose-recipients').value = '';
          }, 2000);*/    
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
  document.querySelector('#reading-view').style.display = 'none';

  // Show the mailbox name
  var body = document.querySelector('#emails-view');
  body.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  //GET the emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    //Each element of the array will be passed to the function
    emails.forEach(data => addMail(data, mailbox))
  });
}

function addMail(element, box){
  // Create each element view dinamically
  const div = document.createElement('div');
  div.className = 'div-mail';
  let unread_class = element.read? "email-view-read" : "email-view-unread";
  
  const btnArchive = document.createElement('button'); 
  btnArchive.className = 'btn btn-sm btn-outline-primary btn-archive';

  switch(box){
    case 'inbox': 
      div.innerHTML += '<span id="email-sender">From: ' + element.sender +' </span>';
      btnArchive.innerHTML = 'Archive';
      btnArchive.addEventListener('click', ()=>{
        // set as Archived
        fetch(`/emails/${element.id}`, {
        method: 'PUT',
        body: JSON.stringify({
        archived: true  })
        });
        event.stopPropagation(); //if not, the mail will be opened
        load_mailbox('inbox');
      });
      break;
    case 'sent': 
      div.innerHTML += '<span id="email-recipients">To: ' + element.recipients +' </span>';
      unread_class = "email-view-unread";
      btnArchive.style.display = 'none';
      break;
    case 'archive': 
      div.innerHTML += '<span id="email-sender">From: ' + element.sender +' </span>';
      btnArchive.innerHTML = 'Unarchive';
      btnArchive.addEventListener('click', ()=>{
        // set as Unarchived
        fetch(`/emails/${element.id}`, {
        method: 'PUT',
        body: JSON.stringify({
        archived: false  })
        });
        event.stopPropagation(); //if not, the mail will be opened
        load_mailbox('inbox');
      });
      break;
  }
  
  div.className += `row border border-dark rounded email-view ${unread_class}`;
  
  div.innerHTML += '<span id="email-subject">' + element.subject +' </span>';
  div.innerHTML += '<span id="email-timestamp">' + element.timestamp +' </span>';
  div.append(btnArchive);
  div.addEventListener('click', ()=> openMail(element.id));
  document.querySelector('#emails-view').appendChild(div);
}

function openMail(id){
  // Load the view with the mail
  mail_view(id);
  
  // Set as Read
  fetch(`/emails/${id}`, {
  method: 'PUT',
  body: JSON.stringify({
      read: true})
  });
}

function mail_view(id){
  // Show the email and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#reading-view').style.display = 'block';

  // GET to fetch the data
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
     //create the view and load the data to the DOM
     document.querySelector('#rd-person').innerHTML = email.sender;
     document.querySelector('#rd-recipient').innerHTML = email.recipients;
     document.querySelector('#rd-subject').innerHTML = email.subject;
     document.querySelector('#rd-timestamp').innerHTML = email.timestamp;
     document.querySelector('#rd-body').innerHTML = email.body;
     
     const btnReply = document.querySelector('#btn-reply');
     btnReply.addEventListener('click', ()=>{
       reply(email.id);
     });
  });
}

function reply(id){
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
  document.querySelector('#compose-recipients').value = email.sender;
  document.querySelector('#compose-recipients').disabled = true;
  document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
  
  });
  
  compose_email();
}