document.addEventListener('DOMContentLoaded', function() {
    // Make the entire label clickable
    const options = document.querySelectorAll('.option');
    options.forEach(option => {
        const label = option.querySelector('label');
        const radio = option.querySelector('input[type="radio"]');
        
        label.addEventListener('click', function() {
            // Select the corresponding radio button
            radio.checked = true;

            // Find all labels within the same question
            const questionDiv = this.closest('.question');
            questionDiv.querySelectorAll('.option label').forEach(l => {
                l.classList.remove('selected');
            });

            // Highlight the selected option
            this.classList.add('selected');
        });
    });

    // Form submission animation
    const form = document.querySelector('form');
    form.addEventListener('submit', function() {
        const button = this.querySelector('button[type="submit"]');
        button.style.opacity = '0.7';
        button.textContent = 'Submitting...';
    });
});
