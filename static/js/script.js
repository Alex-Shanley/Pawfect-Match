function showSidebar(){
  const sidebar= document.querySelector('.sidebar')
  sidebar.style.display = 'flex'
}

function hideSidebar() {
  const sidebar= document.querySelector('.sidebar')
  sidebar.style.display = 'none'
}


const items = document.querySelectorAll ('.faq-title');

items.forEach (items => {
    items.addEventListener('click', () => {
        const parent = items.parentElement;
        parent.classList.toggle('active');
    });
});