var ul = document.querySelector('#left-nav-menu ul')
var menuBtn = document.querySelector('.close-menu');
function menuShow() {

    if (ul.classList.contains('open')) {
        ul.classList.remove('open');
    
    } else {
        ul.classList.add('open');
    }
}