

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
          // Bootstrap Alert
          document.querySelector('#not_sent').innerHTML = `<a>${result.error}</a>`;
          document.querySelector('#not_sent').style.display = 'block';
          setTimeout(
            function() {
                document.querySelector('#not_sent').style.display = 'none';}, 2000); //Improve it to not close alone
                document.querySelector('#compose-recipients').value = '';
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
  // Create each element dinamically
  const div = document.createElement('div');
  div.className = 'div-mail';
  let unread_class = element.read? "email-view-read" : "email-view-unread";
  div.className = `row border border-dark rounded email-view ${unread_class}`;
  
  switch(box){
    case 'inbox': 
      div.innerHTML += '<a id="sender">' + element.sender +' </a>';
      break;
    case 'sent': 
      div.innerHTML += '<a id="recipients">' + element.recipients +' </a>';
      break;
    case 'archive': 
      div.innerHTML += '<a id="sender">' + element.sender +' </a>';
      break;
  }
  
  div.innerHTML += '<a id="subject">' + element.subject +' </a>';
  div.innerHTML += '<a id="timestamp">' + element.timestamp +' </a>';
  
  document.querySelector('#emails-view').appendChild(div);
  div.addEventListener('click', ()=> openMail(element.id));
}

function openMail(id){
  console.log("Clicked on :"+id);
  // Load the view with the mail
  mail_view(id);
  
  // Set as Read
  console.log('Read: '+id);
  fetch(`/emails/${id}`, {
  method: 'PUT',
  body: JSON.stringify({
      read: true})
  });
}

function mail_view(id){
  // Clear previous data (if exist)
  document.querySelector('#reading-view').innerHTML = '';
  
  // Show the email and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#reading-view').style.display = 'block';

  const div = document.createElement('div');
  div.className = 'mail';

  // This button shouldn't be static in HTML? to only change the display as block or none
  
  const btnArchive = document.createElement('button');
    btnArchive.className = "btn btn-sm btn-outline-primary";
    btnArchive.innerHTML = "Archive";
    btnArchive.className = "btn btn-sm btn-outline-primary";
    btnArchive.addEventListener('click', ()=> {
      fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: true  })
      });
    }
    );
    
    document.querySelector('#reading-view').appendChild(btnArchive);
  // GET to fetch the data
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
     if (email.archived){
       btnArchive.className = "btn btn-sm btn-primary";
        }
     //create the view and load the data
     div.innerHTML = '<p>From: <b id="sender">' + email.sender + ' </b></p>';
     
     div.innerHTML += '<p>Recipients: <b id="recipients">' + email.sender + ' </b></p>';
     div.innerHTML += '<p>Subject: ' + email.subject + '  <b id="timestamp">'+email.timestamp+'</b></p>';
     
     
     div.innerHTML += '<p>Body: ' + email.body + ' </p>';
    
     div.innerHTML += '<br><hr>';
     document.querySelector('#reading-view').appendChild(div);
     
  });
  

}
