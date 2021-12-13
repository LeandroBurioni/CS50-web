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
    (async function(){
        const txt =  await get_Post(post);
        document.querySelector(".edit_message").value = txt;    
    })();
    
    document.querySelector(".modal").style.display = 'block';
    
    
}

async function get_Post(id){ //Return true o False
    const response = await fetch(`/getPost/${id}`)
    const resp = await response.json()
    return await Promise.resolve(resp.post_message); 
    console.log(resp.post);
};

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