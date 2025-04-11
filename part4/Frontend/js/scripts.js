// Common utility functions
document.addEventListener('DOMContentLoaded', () => {
    console.log('HBnB application loaded');
    
    // Check if we're on the index page
    if (document.getElementById('places-list')) {
        console.log('Index page loaded');
        
        // Task 2: Index page functionality
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
        
        // Task 3: Place details functionality
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
        
        // Task 4: Add review functionality
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

// Task 4: Add review functions
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

// Setup the review form submission event listener
function setupReviewFormSubmission(token, placeId) {
    const reviewForm = document.getElementById('review-form');
    
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            // Get form data
            const rating = document.getElementById('rating').value;
            const reviewText = document.getElementById('review-text').value;
            
            // Validate form data
            if (!rating || !reviewText) {
                showMessage('review-message', 'Please fill in all fields', 'error');
                return;
            }
            
            try {
                // Submit review
                const result = await submitReview(token, placeId, rating, reviewText);
                
                if (result.success) {
                    // Show success message
                    showMessage('review-message', 'Review submitted successfully!', 'success');
                    
                    // Clear form
                    reviewForm.reset();
                    
                    // Optionally redirect back to the place page after a delay
                    setTimeout(() => {
                        window.location.href = `place.html?id=${placeId}`;
                    }, 2000);
                } else {
                    // Show error message
                    showMessage('review-message', result.message || 'Failed to submit review', 'error');
                }
            } catch (error) {
                console.error('Error submitting review:', error);
                showMessage('review-message', 'An unexpected error occurred. Please try again.', 'error');
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

// Task 3: Place details functions
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
        if (loginLink) loginLink.style.display = 'block';
        // Hide add review button for unauthenticated users
        if (addReviewSection) addReviewSection.style.display = 'none';
    } else {
        if (loginLink) loginLink.style.display = 'none';
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
        
        // Fetch place reviews
        const response = await fetch(`http://localhost:3000/api/v1/places/${placeId}/reviews`, {
            method: 'GET',
            headers: headers
        });
        
        if (response.ok) {
            const reviews = await response.json();
            displayPlaceReviews(reviews, placeId);
        } else {
            console.error('Failed to fetch reviews:', response.statusText);
            const reviewsSection = document.querySelector('.reviews-section');
            if (reviewsSection) {
                reviewsSection.innerHTML += '<div class="error-message">Failed to load reviews. Please try again later.</div>';
            }
        }
    } catch (error) {
        console.error('Error fetching reviews:', error);
        const reviewsSection = document.querySelector('.reviews-section');
        if (reviewsSection) {
            reviewsSection.innerHTML += '<div class="error-message">An error occurred while loading reviews. Please try again later.</div>';
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
    
    if (reviews.length === 0) {
        reviewsList.innerHTML = '<p>No reviews yet. Be the first to leave a review!</p>';
        return;
    }
    
    // Create review cards for each review
    reviews.forEach(review => {
        const reviewCard = document.createElement('div');
        reviewCard.className = 'review-card';
        
        // Generate star rating
        const stars = '★'.repeat(review.rating) + '☆'.repeat(5 - review.rating);
        
        // Create review card HTML
        reviewCard.innerHTML = `
            <div class="review-header">
                <h3>${review.user.first_name} ${review.user.last_name}</h3>
                <p class="rating">${stars}</p>
            </div>
            <p class="review-text">${review.text}</p>
        `;
        
        reviewsList.appendChild(reviewCard);
    });
}

// Task 2: Index page functions
// Check authentication and manage the login link visibility
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        if (loginLink) loginLink.style.display = 'block';
        // Fetch places anyway for non-authenticated users
        fetchPlaces(null);
    } else {
        if (loginLink) loginLink.style.display = 'none';
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
        
        const response = await fetch('http://localhost:3000/api/v1/places', {
            method: 'GET',
            headers: headers
        });
        
        if (response.ok) {
            const places = await response.json();
            // IMPORTANT: Clear out static example places completely
            const placesList = document.getElementById('places-list');
            placesList.innerHTML = ''; // Force clearing before displaying
            
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

// Login functionality (Task 1)
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