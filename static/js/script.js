// -------------------------------------------
// Function: Show Sidebar
// -------------------------------------------
function showSidebar() {
  const sidebar = document.querySelector('.sidebar');
  sidebar.style.display = 'flex';
}

// -------------------------------------------
// Function: Hide Sidebar
// -------------------------------------------
function hideSidebar() {
  const sidebar = document.querySelector('.sidebar');
  sidebar.style.display = 'none';
}

// -------------------------------------------
// FAQ Accordion Toggle
// -------------------------------------------
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

// -------------------------------------------
// Form Submission Handler with Confetti + Alert
// -------------------------------------------
document.getElementById('contactform').addEventListener('submit', function(event) {
  event.preventDefault();

  const firstName = document.getElementById('firstName').value;
  const lastName = document.getElementById('lastName').value;

  // Confetti animation
  confetti({
    particleCount: 350,
    spread: 700,
    origin: { y: 0.6 }
  });

  // Notification
  const notificationMessage = `Thank you for reaching out to the Pawfect Match, ${firstName} ${lastName}. Your message has been sent successfully.`;
  alert(notificationMessage);

  // Delay and submit after 1 second
  setTimeout(() => {
    event.target.submit();
  }, 1000);
});
