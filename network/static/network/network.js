document.addEventListener('DOMContentLoaded', function() {
   console.log("DOM loaded"); 
   
   
});

async function isFollow(id){ //Return true o False
    const response = await fetch(`/isFollow/${id}`)
    const resp = await response.json()
    //console.log('Follow in js function is: '+ resp.response);
    return await Promise.resolve(resp.response); //Without this line, the response is Undefined
};


async function isLike(id){ //Return true o False
    const response = await fetch(`/isLike/${id}`)
    const resp = await response.json()
    //console.log('For post '+id+' is: '+resp.response);
    return await Promise.resolve(resp.response); 
    
};

function actFollow(id){
    //console.log('User hit the Follow/Unfollow button');
    fetch(`/actFollow/${id}`, {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({id : id}),
        })      
      .then(response => response.json())
      .then(response => {
        //console.log('Resultado:  '+response.message);
        location.reload();})
    .catch(error => console.error('Error:', error));
};  

function actLike(id){
    //console.log('User hit the Follow/Unfollow button');
    fetch(`/actLike/${id}`, {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({id : id}),
        })      
      .then(response => response.json())
      .then(response => {
        //console.log('Resultado:  '+response.message);
        location.reload();})
    .catch(error => console.error('Error:', error));
};  

function editPost(post){
    document.querySelector(".modal").style.display = 'block';
    
    document.querySelector(".edit_message").value = "Aca tiene que ir old_txt";
    
}

function get_post(post){
    fetch(`/edit/${post}/${text}`, {
        method: 'POST',
        body: JSON.stringify({
            post_message : text,
        })
      })
    .then(response => response.json())
    .then( data => {
        console.log("Edit function responsed -> "+data);
    })
}

function put_post(post, text){
    fetch(`/edit/${post}/${text}`, {
        method: 'POST',
        body: JSON.stringify({
            post_message : text,
        })
      })
    .then(response => response.json())
    .then( data => {
        console.log("Edit function responsed -> "+data);
    })
}