function toggleSidebar() {
    document.querySelector('#sidebar').toggleAttribute('opened');
}

const buttonToggle = document.querySelector('button.sidebar-button');
buttonToggle.addEventListener('click', event => {
    toggleSidebar();
});
buttonToggle.addEventListener('keydown', event => {
    if(event.keyCode === 13 || event.keyCode === 32 ) {
        toggleSidebar();
    }
});
