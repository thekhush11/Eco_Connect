document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('rating-stars-container');
    if (!container) return; // Exit if not on the feedback page
    
    const stars = container.querySelectorAll('.rating-star');
    let currentRating = 4; // Initial display score

    const applyRating = (rating) => {
        stars.forEach(star => {
            const value = parseInt(star.getAttribute('data-value'));
            star.textContent = value <= rating ? 'star' : 'star_border'; // Filled or empty
        });
    };

    const handleMouseOver = (event) => {
        const hoverValue = parseInt(event.target.getAttribute('data-value'));
        if (hoverValue) {
            stars.forEach(star => {
                const value = parseInt(star.getAttribute('data-value'));
                if (value <= hoverValue) {
                    star.classList.add('glow');
                } else {
                    star.classList.remove('glow');
                }
            });
        }
    };
    
    const handleMouseOut = () => {
        stars.forEach(star => star.classList.remove('glow'));
        applyRating(currentRating); // Reset to selected rating
    };
    
    const handleClick = (event) => {
        const clickValue = parseInt(event.target.getAttribute('data-value'));
        if (clickValue) {
            currentRating = clickValue;
            applyRating(currentRating);
            // Optional: You would update a hidden form field here to submit the rating
        }
    };

    container.addEventListener('mouseover', handleMouseOver);
    container.addEventListener('mouseout', handleMouseOut);
    container.addEventListener('click', handleClick);

    // Initial display logic
    applyRating(currentRating); 
    // Fix for the initial half-star look from the screenshot:
    stars.forEach(star => {
        const value = parseInt(star.getAttribute('data-value'));
        if (value === 5) {
            star.textContent = 'star_half';
        }
    });
});