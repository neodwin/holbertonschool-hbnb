// Common utility functions
document.addEventListener('DOMContentLoaded', () => {
    console.log('HBnB application loaded');
    
    // Check if we're on the index page
    if (document.getElementById('places-list')) {
        console.log('Index page loaded');

        // Check authentication and control login button visibility
        checkAuthentication();
        
        // Add event listener for price filter
        document.getElementById('price-filter').addEventListener('change', (event) => {
            filterPlacesByPrice(event.target.value);
        });
    }
    
    // Check if we're on the login page
    if (document.getElementById('login-form')) {
        console.log('Login page loaded');
        
        // Login functionality implementation (Task 1)
        const loginForm = document.getElementById('login-form');
        
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            // Clear previous error messages
            clearError('login-error');
            
            // Get form data
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            // Validate form data
            if (!email || !password) {
                showError('login-error', 'Please enter both email and password');
                return;
            }
            
            try {
                // Call login function
                await loginUser(email, password);
            } catch (error) {
                console.error('Login error:', error);
                showError('login-error', 'An unexpected error occurred. Please try again.');
            }
        });
    }
    
    // Check if we're on the place details page
    if (document.getElementById('place-details')) {
        console.log('Place details page loaded');
        
        // Get place ID from URL
        const placeId = getPlaceIdFromURL();
        
        if (placeId) {
            // Check authentication and control login button visibility
            const token = checkAuthenticationForPlaceDetails();
            
            // Fetch place details
            fetchPlaceDetails(token, placeId);
        } else {
            // Handle invalid or missing place ID
            const placeDetails = document.getElementById('place-details');
            placeDetails.innerHTML = '<div class="error-message">Invalid place ID. Please return to the <a href="index.html">home page</a>.</div>';
        }
    }
    
    // Check if we're on the add review page
    if (document.getElementById('review-form')) {
        console.log('Add review page loaded');
        
        // Check authentication first - redirect to index if not authenticated
        const token = checkAuthenticationForAddReview();
        
        if (token) {
            // Get place ID from URL
            const placeId = getPlaceIdFromURL();
            
            if (!placeId) {
                // Handle missing place ID
                showMessage('review-message', 'Invalid place ID. Please return to the home page.', 'error');
                document.getElementById('review-form').style.display = 'none';
                return;
            }
            
            // Update cancel button to return to the correct place page
            const cancelButton = document.getElementById('cancel-button');
            if (cancelButton) {
                cancelButton.href = `place.html?id=${placeId}`;
            }
            
            // Setup form submission event listener
            setupReviewFormSubmission(token, placeId);
        }
    }
});

// Check authentication for add review page and redirect if not authenticated
function checkAuthenticationForAddReview() {
    const token = getCookie('token');
    if (!token) {
        // Redirect to index page if not authenticated
        window.location.href = 'index.html';
        return null;
    }
    
    // Hide login link if authenticated
    const loginLink = document.getElementById('login-link');
    if (loginLink) {
        loginLink.style.display = 'none';
    }
    
    return token;
}

// Modify the review form submission function
function setupReviewFormSubmission(token, placeId) {
    const reviewForm = document.getElementById('review-form');
    
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // Get form values
            const rating = document.querySelector('input[name="rating"]:checked')?.value;
            const reviewText = document.getElementById('review-text').value;
            
            // Validate form
            if (!rating) {
                showMessage('review-message', 'Please select a rating', 'error');
                return;
            }
            
            if (!reviewText.trim()) {
                showMessage('review-message', 'Please enter your review', 'error');
                return;
            }
            
            // Désactiver le bouton de soumission pour éviter les doubles soumissions
            const submitButton = reviewForm.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = 'Submitting...';
            }
            
            // Show loading message
            showMessage('review-message', 'Submitting your review...', 'info');
            
            try {
                // Submit the review
                const result = await submitReview(token, placeId, rating, reviewText);
                
                if (result.success) {
                    // Show success message
                    showMessage('review-message', 'Review submitted successfully!', 'success');
                    
                    // Mettre un drapeau dans la session storage pour indiquer que l'utilisateur vient de soumettre une review
                    sessionStorage.setItem('reviewJustSubmitted', 'true');
                    
                    // Rediriger vers la page de détails du lieu après un court délai
                    setTimeout(() => {
                        window.location.href = `place.html?id=${placeId}`;
                    }, 500);
                } else {
                    // Show error message
                    showMessage('review-message', result.message || 'Failed to submit review', 'error');
                    
                    // Réactiver le bouton en cas d'erreur
                    if (submitButton) {
                        submitButton.disabled = false;
                        submitButton.textContent = 'Submit Review';
                    }
                }
            } catch (error) {
                console.error('Error submitting review:', error);
                showMessage('review-message', 'An unexpected error occurred. Please try again.', 'error');
                
                // Réactiver le bouton en cas d'erreur
                if (submitButton) {
                    submitButton.disabled = false;
                    submitButton.textContent = 'Submit Review';
                }
            }
        });
    }
}

// Submit review to API
async function submitReview(token, placeId, rating, reviewText) {
    try {
        // Get user info using the token
        const userInfo = await getCurrentUser(token);
        
        if (!userInfo) {
            return { success: false, message: 'Could not get user information. Please log in again.' };
        }
        
        // Prepare review data
        const reviewData = {
            text: reviewText,
            rating: parseInt(rating),
            user_id: userInfo.id,
            place_id: placeId
        };
        
        console.log('Submitting review with data:', reviewData);
        
        // Send review to API (with trailing slash to prevent 308 redirect)
        const response = await fetch('http://localhost:3000/api/v1/reviews/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(reviewData)
        });
        
        if (response.ok) {
            return { success: true };
        } else {
            const errorData = await response.json();
            return { 
                success: false,
                message: errorData.error || `Failed to submit review: ${response.statusText}`
            };
        }
    } catch (error) {
        console.error('Error in submitReview:', error);
        return { success: false, message: 'An error occurred while submitting your review' };
    }
}

// Get current user information
async function getCurrentUser(token) {
    try {
        const response = await fetch('http://localhost:3000/api/v1/auth/me', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            return await response.json();
        } else {
            console.error('Failed to get user info:', response.statusText);
            return null;
        }
    } catch (error) {
        console.error('Error getting user info:', error);
        return null;
    }
}

// Show message in the specified element with success or error styling
function showMessage(elementId, message, type = 'success') {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = message;
        element.className = `message ${type}`;
        element.style.display = 'block';
    }
}

// Get place ID from URL query parameters
function getPlaceIdFromURL() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    return urlParams.get('id');
}

// Check authentication for place details page
function checkAuthenticationForPlaceDetails() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const addReviewSection = document.getElementById('add-review');
    
    if (!token) {
        // Non connecté : afficher le bouton Login
        if (loginLink) {
            loginLink.textContent = "Login";
            loginLink.style.display = 'block';
            loginLink.onclick = null; // Supprimer l'ancien gestionnaire d'événement s'il existe
        }
        // Hide add review button for unauthenticated users
        if (addReviewSection) addReviewSection.style.display = 'none';
    } else {
        // Connecté : transformer le lien en bouton Logout
        if (loginLink) {
            loginLink.textContent = "Logout";
            loginLink.style.display = 'block';
            // Ajouter un gestionnaire d'événement pour se déconnecter
            loginLink.onclick = function(e) {
                e.preventDefault();
                logoutUser();
                return false;
            };
        }
        // Show add review button for authenticated users
        if (addReviewSection) addReviewSection.style.display = 'block';
    }
    
    return token;
}

// Fetch place details from API
async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = {
            'Content-Type': 'application/json'
        };
        
        // Add Authorization header if token exists
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        // Fetch place details
        const response = await fetch(`http://localhost:3000/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: headers
        });
        
        if (response.ok) {
            const placeData = await response.json();
            displayPlaceDetails(placeData, placeId);
            
            // Fetch reviews for this place
            fetchPlaceReviews(token, placeId);
        } else {
            console.error('Failed to fetch place details:', response.statusText);
            const placeDetails = document.getElementById('place-details');
            placeDetails.innerHTML = '<div class="error-message">Failed to load place details. Please try again later.</div>';
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
        const placeDetails = document.getElementById('place-details');
        placeDetails.innerHTML = '<div class="error-message">An error occurred while loading place details. Please try again later.</div>';
    }
}

// Fetch reviews for a place
async function fetchPlaceReviews(token, placeId) {
    try {
        const headers = {
            'Content-Type': 'application/json'
        };
        
        // Add Authorization header if token exists
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        // Fetch place reviews - Ajouter un slash à la fin de l'URL pour éviter la redirection 308
        console.log(`Fetching reviews for place ${placeId}`);
        const response = await fetch(`http://localhost:3000/api/v1/places/${placeId}/reviews/`, {
            method: 'GET',
            headers: headers
        });
        
        if (response.ok) {
            const reviews = await response.json();
            console.log(`Received ${reviews.length} reviews from API`);
            displayPlaceReviews(reviews, placeId);
        } else {
            console.error('Failed to fetch reviews:', response.statusText);
            const reviewsSection = document.querySelector('.reviews-section');
            if (reviewsSection) {
                const reviewsList = document.getElementById('reviews-list');
                if (reviewsList) {
                    reviewsList.innerHTML = '<div class="error-message">Failed to load reviews. Please try again later.</div>';
                }
            }
        }
    } catch (error) {
        console.error('Error fetching reviews:', error);
        const reviewsSection = document.querySelector('.reviews-section');
        if (reviewsSection) {
            const reviewsList = document.getElementById('reviews-list');
            if (reviewsList) {
                reviewsList.innerHTML = '<div class="error-message">An error occurred while loading reviews. Please try again later.</div>';
            }
        }
    }
}

// Display place details
function displayPlaceDetails(placeData, placeId) {
    const placeDetails = document.getElementById('place-details');
    
    // Clear existing content
    placeDetails.innerHTML = '';
    
    // Handle potential missing data
    const owner = placeData.owner || { first_name: 'Admin', last_name: 'HBnB', email: 'admin@hbnb.io' };
    
    // Create place info section
    const placeInfo = document.createElement('div');
    placeInfo.className = 'place-info';
    
    // Place header with title and price
    placeInfo.innerHTML = `
        <div class="place-header">
            <h1>${placeData.title}</h1>
            <p class="price">$${placeData.price} per night</p>
        </div>
        
        <div class="place-gallery">
            <img src="images/place1.jpg" alt="${placeData.title}" class="main-image">
        </div>
        
        <div class="place-description">
            <h2>About this place</h2>
            <p>${placeData.description || 'No description available.'}</p>
            
            <div class="host-info">
                <h3>Hosted by ${owner.first_name} ${owner.last_name}</h3>
                <p>Contact: ${owner.email}</p>
            </div>
            
            <div class="amenities">
                <h3>Amenities</h3>
                <ul id="amenities-list">
                    ${displayAmenities(placeData.amenities)}
                </ul>
            </div>
        </div>
    `;
    
    // Create reviews section
    const reviewsSection = document.createElement('div');
    reviewsSection.className = 'reviews-section';
    reviewsSection.innerHTML = `
        <h2>Reviews</h2>
        <div id="reviews-list"></div>
        <div id="add-review" class="add-review">
            <a href="add_review.html?id=${placeId}" class="btn-primary">Add a Review</a>
        </div>
    `;
    
    // Append sections to place details
    placeDetails.appendChild(placeInfo);
    placeDetails.appendChild(reviewsSection);
    
    // Check authentication to show/hide add review button
    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review');
    if (!token && addReviewSection) {
        addReviewSection.style.display = 'none';
    }
}

// Display place reviews
function displayPlaceReviews(reviews, placeId) {
    const reviewsList = document.getElementById('reviews-list');
    
    if (!reviewsList) return;
    
    // Clear existing content
    reviewsList.innerHTML = '';
    
    if (!reviews || reviews.length === 0) {
        reviewsList.innerHTML = '<p>No reviews yet. Be the first to leave a review!</p>';
        return;
    }
    
    console.log(`Displaying ${reviews.length} reviews`);
    
    // Garder une trace des IDs de reviews déjà affichées pour éviter les doublons
    const displayedReviewIds = new Set();
    
    // Create review cards for each review
    reviews.forEach(review => {
        // Vérifier si cette review a déjà été affichée
        if (review.id && displayedReviewIds.has(review.id)) {
            console.log(`Skipping duplicate review ${review.id}`);
            return;
        }
        
        // Ajouter l'ID à l'ensemble des reviews affichées
        if (review.id) {
            displayedReviewIds.add(review.id);
        }
        
        const reviewCard = document.createElement('div');
        reviewCard.className = 'review-card';
        
        // Generate star rating
        const stars = '★'.repeat(review.rating) + '☆'.repeat(5 - review.rating);
        
        // Fetch user info for this review if it's not already included
        let userName = "Anonymous";
        
        // If review has user object with name properties, use it directly
        if (review.user && review.user.first_name && review.user.last_name) {
            userName = `${review.user.first_name} ${review.user.last_name}`;
        } 
        // Otherwise, we'll just display User ID
        else if (review.user_id) {
            userName = `User ${review.user_id.substr(0, 8)}...`;
        }
        
        // Create review card HTML
        reviewCard.innerHTML = `
            <div class="review-header">
                <h3>${userName}</h3>
                <p class="rating">${stars}</p>
            </div>
            <p class="review-text">${review.text}</p>
        `;
        
        reviewsList.appendChild(reviewCard);
    });
    
    console.log(`Displayed ${displayedReviewIds.size} unique reviews`);
}

// Check authentication and manage the login link visibility
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        // Non connecté : afficher le bouton Login
        if (loginLink) {
            loginLink.textContent = "Login";
            loginLink.style.display = 'block';
            loginLink.onclick = null; // Supprimer l'ancien gestionnaire d'événement s'il existe
        }
        // Fetch places anyway for non-authenticated users
        fetchPlaces(null);
    } else {
        // Connecté : transformer le lien en bouton Logout
        if (loginLink) {
            loginLink.textContent = "Logout";
            loginLink.style.display = 'block';
            // Ajouter un gestionnaire d'événement pour se déconnecter
            loginLink.onclick = function(e) {
                e.preventDefault();
                logoutUser();
                return false;
            };
        }
        // Fetch places with token for authenticated users
        fetchPlaces(token);
    }
}

// Fetch places data from API
async function fetchPlaces(token) {
    try {
        const headers = {
            'Content-Type': 'application/json'
        };
        
        // Add Authorization header if token exists
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        // Ajouter un slash à la fin de l'URL pour éviter la redirection 308
        const response = await fetch('http://localhost:3000/api/v1/places/', {
            method: 'GET',
            headers: headers
        });
        
        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
            // Store places data in a global variable for filtering
            window.placesData = places;
        } else {
            console.error('Failed to fetch places:', response.statusText);
        }
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}

// Display places in the UI
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    
    // Clear existing content
    placesList.innerHTML = '';
    
    if (places.length === 0) {
        placesList.innerHTML = '<div class="no-places">No places found</div>';
        return;
    }
    
    // Assign specific images to each place type
    const getImageForPlace = (title) => {
        if (title.toLowerCase().includes('cozy') || title.toLowerCase().includes('apartment')) {
            return 'images/place1.jpg';
        } else if (title.toLowerCase().includes('luxury') || title.toLowerCase().includes('villa')) {
            return 'images/place2.jpg';
        } else if (title.toLowerCase().includes('beach') || title.toLowerCase().includes('house')) {
            return 'images/place3.jpg';
        } else {
            return 'images/place1.jpg'; // default image
        }
    };
    
    // Create place cards for each place
    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.dataset.price = place.price; // Store price for filtering
        
        // Get appropriate image based on place title
        const imageSrc = getImageForPlace(place.title);
        
        // Create place card HTML with correct place ID
        placeCard.innerHTML = `
            <img src="${imageSrc}" alt="${place.title}">
            <h2>${place.title}</h2>
            <p class="price">$${place.price} per night</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        
        placesList.appendChild(placeCard);
    });
    
    console.log(`Displayed ${places.length} places with real data`);
}

// Filter places by price
function filterPlacesByPrice(maxPrice) {
    const places = window.placesData || [];
    
    if (maxPrice === 'all') {
        // Show all places
        displayPlaces(places);
    } else {
        // Filter places by price
        const filteredPlaces = places.filter(place => place.price <= parseInt(maxPrice));
        displayPlaces(filteredPlaces);
    }
}

// Login functionality
async function loginUser(email, password) {
    try {
        // The API is running on port 3000 according to run.py
        const response = await fetch('http://localhost:3000/api/v1/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        // Handle the response
        if (response.ok) {
            const data = await response.json();
            // Store token in cookie
            document.cookie = `token=${data.access_token}; path=/; max-age=86400`; // expires in 1 day
            // Redirect to home page
            window.location.href = 'index.html';
        } else {
            // Handle error responses
            if (response.status === 401) {
                showError('login-error', 'Invalid email or password');
            } else if (response.status === 400) {
                showError('login-error', 'Please enter both email and password');
            } else {
                showError('login-error', 'Login failed: ' + response.statusText);
            }
        }
    } catch (error) {
        console.error('Error during login:', error);
        throw error;
    }
}

// Cookie helper function
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Function to display error messages
function showError(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = message;
        element.style.display = 'block';
    }
}

// Function to clear error messages
function clearError(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = '';
        element.style.display = 'none';
    }
}

// Helper function to display amenities regardless of format
function displayAmenities(amenities) {
    if (!amenities || !Array.isArray(amenities) || amenities.length === 0) {
        return '<li>No amenities listed</li>';
    }

    // Handle different possible formats of amenities
    return amenities.map(amenity => {
        if (typeof amenity === 'string') {
            return `<li>${amenity}</li>`;
        } else if (typeof amenity === 'object') {
            if (amenity.name) {
                return `<li>${amenity.name}</li>`;
            } else {
                return `<li>${JSON.stringify(amenity).replace(/[{}"]/g, '')}</li>`;
            }
        }
        return '';
    }).join('');
}

// logout function
function logoutUser() {
    document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    window.location.reload();
}
