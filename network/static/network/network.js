document.addEventListener('DOMContentLoaded', function() {
   console.log("DOM loaded"); 
   
});

async function isFollow(id){ //Return true o False
    const response = await fetch(`/isFollow/${id}`)
    const resp = await response.json()
    //console.log(response);
    //console.log(resp);
    console.log('Inside the js function is: '+ resp.response);
    return await Promise.resolve(resp.response); //Tiene que estar, sino Undef
    
};

function edit(post, text){
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