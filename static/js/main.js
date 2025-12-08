document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');

    if (mobileMenuBtn && navLinks) {
        mobileMenuBtn.addEventListener('click', function() {
            navLinks.classList.toggle('active');
        });
    }

    const flashCloseButtons = document.querySelectorAll('.flash-close');
    flashCloseButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const flashMessage = this.closest('.flash-message');
            flashMessage.style.animation = 'slideUp 0.3s ease forwards';
            setTimeout(function() {
                flashMessage.remove();
            }, 300);
        });
    });

    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideUp {
            from {
                opacity: 1;
                transform: translateY(0);
            }
            to {
                opacity: 0;
                transform: translateY(-10px);
            }
        }
    `;
    document.head.appendChild(style);

    setTimeout(function() {
        const flashMessages = document.querySelectorAll('.flash-message');
        flashMessages.forEach(function(message) {
            message.style.animation = 'slideUp 0.3s ease forwards';
            setTimeout(function() {
                message.remove();
            }, 300);
        });
    }, 5000);

    const contentCards = document.querySelectorAll('.content-card');
    contentCards.forEach(function(card) {
        const link = card.querySelector('a.btn');
        if (link) {
            card.addEventListener('click', function(e) {
                if (e.target.tagName !== 'A' && e.target.tagName !== 'BUTTON') {
                    link.click();
                }
            });
        }
    });
});
