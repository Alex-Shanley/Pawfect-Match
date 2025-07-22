function showSidebar(){
  const sidebar= document.querySelector('.sidebar')
  sidebar.style.display = 'flex'
}

function hideSidebar() {
  const sidebar= document.querySelector('.sidebar')
  sidebar.style.display = 'none'
}





const items = document.querySelectorAll('.faq-title');

items.forEach(item => {
  item.addEventListener('click', () => {
    const parent = item.parentElement;

    
    document.querySelectorAll('.faq-item').forEach(faq => {
      if (faq !== parent) {
        faq.classList.remove('active');
      }
    });

    parent.classList.toggle('active');
  });
});




  document.getElementById('contactform').addEventListener('submit', function(event) {
  event.preventDefault();  

  confetti ({
    particleCount: 150,
    spread:70,
    origin: {y:0.6}

  });

  setTimeout(() => {
    event.target.submit();
  }, 1000);

 });
