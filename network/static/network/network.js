document.addEventListener('DOMContentLoaded', function() {
    
    
});

function isFollow(id){ //Return true o False
    fetch(`/isFollow/${id}`)
    .then(response => response.json())
    .then(resp => {
        //console.log(resp);
        if(resp){ 
            console.log("Le sigue!");
            return true;
        }
        else{
            console.log("NO le sigue!");
            return false;
        }
    })
};

