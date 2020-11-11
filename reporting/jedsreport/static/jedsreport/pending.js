document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#pending').style.display = 'none';
    document.querySelector('#pending-expand').onclick = function(){
        document.querySelector('#pending').style.display = 'block';
        document.querySelector('#resolved-expand').style.display = 'none';

    }
    document.querySelector('#resolved').style.display = 'none';
    document.querySelector('#resolved-expand').onclick = function(){
        document.querySelector('#resolved').style.display = 'block';
        document.querySelector('#pending-expand').style.display = 'none';
    }
    
    
})