document.addEventListener('DOMContentLoaded', function() {
   console.log("DOM loaded"); 
   
   
});

function closeModal(){
    document.querySelector('.modal').style.display = 'none';
    document.querySelector(".edit_message").value = '';
}

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
    document.querySelector("#savePost").addEventListener('click', ()=>{
        savePost(post);
        closeModal();
        location.reload();
    });
    
}

function savePost(id){
    console.log("Save con parametro "+id);
    const txt = document.querySelector(".edit_message").value;
    console.log(`./editPost/${id}`);
    fetch(`editPost/${id}`, {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({'post_message' : txt}),
        })      
      .then(response => response.json())
      .then(response => {
        console.log('Resultado:  '+response.message);
        })
    
    

}


async function get_Post(id){ //Return true o False
    const response = await fetch(`/editPost/${id}`)
    const resp = await response.json()
    return await Promise.resolve(resp.post_message); 
    console.log(resp.post);
};
