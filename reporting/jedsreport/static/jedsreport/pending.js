document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#pending').style.display = 'none';
    document.querySelector('#pending-expand').onclick = function(){
        document.querySelector('#pending').style.display = 'block';
    }
    
})