task_00_design.md

0. Design
mandatory
Objectives

    Complete the provided HTML and CSS files to match the given design specifications.
    Create the following pages:
        Login Form
        List of Places
        Place Details
        Add Review Form

Requirements

    Use the provided HTML and CSS files as a starting point.
    Follow the design specifications closely to achieve the intended look and feel.

Instructions

    Download the Provided Files:
        Obtain the HTML and CSS files provided as the starting point for this task. -> https://github.com/Holberton-Uy/hbnb-doc/tree/main/part4/base_files

    Complete the HTML Structure:
        Use semantic HTML5 elements to structure the content of each page.
        Ensure the structure matches the design specifications provided below.

    Apply CSS Styles:
        Use the provided CSS file and add necessary styles to achieve the desired design.

    Pages to Complete:
        Login Form: Create a login form with fields for email and password.
        List of Places: Design a page to display a list of places with basic information.
        Place Details: Create a detailed view for a specific place including detailed information.
        Add Review Form: Design a form for adding a review to a place, accessible only to authenticated users.

Instructions for Styles and Structure

    Required Structure:
        Header:
            Must include the application logo (https://github.com/Holberton-Uy/hbnb-doc/blob/main/part4/base_files/images/logo.png) with the class logo.
            Must include the login button or link with the class login-button.
        Footer:
            Must include text indicating all rights reserved.
        Navigation Bar:
            Must include relevant navigation links (e.g., index.html and login.html).

    Data to Display:
        Index (index.html):
            Display a list of places as “cards” using the class place-card.
            Each card must include the name, the price per night and a “View Details” button with the class details-button.
        Place Details (place.html):
            Display extended information about the place, including the host, price, description, and amenities using the classes place-details, and place-info.
            List reviews if they exist, each displayed as a card with the comment, user name, and rating using the class review-card.
            Include a button to navigate to the add_review.html page if the user is logged in.
            Optional: Substitute the previous button with a form to add a new review if the user is logged in, using the classes add-review and form.

    Fixed Parameters:
        Margin: Use a margin of 20px for place and review cards.
        Padding: Use a padding of 10px within place and review cards.
        Border: Use a border of 1px solid #ddd for place and review cards.
        Border Radius: Use a border radius of 10px for place and review cards.

    Flexible Parameters:
        Color Palette: Students can choose their color palette.
        Font: Students can choose their font.
        Images: Students can choose the images to use. Some sample images already provided with the base code.
        FavIcon: Students can add a custom favicon or use the already provided icon.png.

    All pages MUST be valid on W3C Validator page : https://validator.w3.org/

Sample Design 

Check this link to see sample images : https://github.com/Holberton-Uy/hbnb-doc/tree/main/part4/doc_images

This is to be used as a reference, they were made by someone with no design skills. :)
Resources

    HTML5 Documentation : https://developer.mozilla.org/en-US/docs/Glossary/HTML5
    CSS3 Documentation
    HTML Semantic Elements : https://developer.mozilla.org/en-US/docs/Glossary/Semantics#semantics_in_html

Repo:

    GitHub repository: holbertonschool-hbnb
    Directory: part4



1. Login
mandatory
Objectives

    Implement login functionality using the back-end API.
    Store the JWT token returned by the API in a cookie for session management.

Requirements

    Use the existing login form provided in login.html : https://github.com/Holberton-Uy/hbnb-doc/blob/main/part4/base_files/login.html
    Make an AJAX request to the login endpoint of your API when the user submits the login form.
    If the login is successful, store the JWT token in a cookie.
    Redirect the user to the main page (index.html) after a successful login.
    Display an error message if the login fails.

Instructions

    Setup Event Listener for Login Form:
        Add an event listener to the login form to handle the form submission.
        Use preventDefault to prevent the default form submission behavior.

    Make AJAX Request to API:
        Use the Fetch API to send a POST request to the login endpoint with the email and password entered by the user.
        Set the Content-Type header to application/json.
        Send the email and password in the request body as a JSON object.

    Handle API Response:
        If the login is successful, store the returned JWT token in a cookie.
        Redirect the user to the main page (index.html).
        If the login fails, display an error message to the user.

    Example Guidance:

scripts.js

    Add an event listener for the form submission:

  document.addEventListener('DOMContentLoaded', () => {
      const loginForm = document.getElementById('login-form');

      if (loginForm) {
          loginForm.addEventListener('submit', async (event) => {
              event.preventDefault();
              // Your code to handle form submission
          });
      }
  });

    Make the AJAX request to the API:

  async function loginUser(email, password) {
      const response = await fetch('https://your-api-url/login', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email, password })
      });
      // Handle the response
  }

    Handle the API response and store the token in a cookie:

  if (response.ok) {
      const data = await response.json();
      document.cookie = `token=${data.access_token}; path=/`;
      window.location.href = 'index.html';
  } else {
      alert('Login failed: ' + response.statusText);
  }

    Testing:
        Test the login functionality with valid and invalid credentials to ensure it works as expected.
        Verify that the JWT token is stored in the cookie after a successful login.
        Ensure that the user is redirected to the main page after login.

Resources

    Fetch API : https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
    Handling Cookies in JavaScript : https://developer.mozilla.org/en-US/docs/Web/API/Document/cookie
    HTML5 Form Validation : https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/Form_validation

Repo:

    GitHub repository: holbertonschool-hbnb
    Directory: part4



2. Index
mandatory
Objectives

    Implement the main page to display a list of all places.
    Fetch places data from the API and implement client-side filtering based on price.
    Show the login link only if the user is not authenticated.

Requirements

    Use the provided HTML structure in index.html (https://github.com/Holberton-Uy/hbnb-doc/blob/main/part4/base_files/index.html) to display the list of places.
    Make an AJAX request to the API to fetch the list of places.
    Populate the places list dynamically using JavaScript.
    Implement a client-side filter to allow users to filter places by price without reloading the page.
    Show or hide the login link based on user authentication.

Instructions

    Check User Authentication:
        On page load, check if the user is authenticated by verifying the presence of the JWT token in cookies.
        If the token is not found, show the login link.
        If the token is found, hide the login link.
        Tip: Use a function to get the value of a cookie by its name.

    Fetch Places Data:
        Use the Fetch API to send a GET request to the endpoint that returns the list of places.
        Ensure the request includes the JWT token for authentication if available.
        Tip: Include the token in the Authorization header of your request.

    Populate Places List:
        Dynamically create HTML elements to display each place’s information (e.g., name, description, location).
        Append these elements to the #places-list section.
        Tip: Use document.createElement and element.innerHTML to build the place elements.

    Implement Client-Side Filtering:
        Add an event listener to the price filter dropdown.
        Filter the displayed places based on the selected price.
        Ensure the filtering works without reloading the page.
        Tip: Use element.style.display to show or hide places based on the filter.

Example Guidance

scripts.js

    Check user authentication:
        Create a function to check for the JWT token in cookies and control the visibility of the login link.

  function checkAuthentication() {
      const token = getCookie('token');
      const loginLink = document.getElementById('login-link');

      if (!token) {
          loginLink.style.display = 'block';
      } else {
          loginLink.style.display = 'none';
          // Fetch places data if the user is authenticated
          fetchPlaces(token);
      }
  }
  function getCookie(name) {
      // Function to get a cookie value by its name
      // Your code here
  }

    Fetch places data:
        Use the Fetch API to get the list of places and handle the response.

  async function fetchPlaces(token) {
      // Make a GET request to fetch places data
      // Include the token in the Authorization header
      // Handle the response and pass the data to displayPlaces function
  }

    Populate places list:
        Create HTML elements for each place and append them to the #places-list.

  function displayPlaces(places) {
      // Clear the current content of the places list
      // Iterate over the places data
      // For each place, create a div element and set its content
      // Append the created element to the places list
  }

    Implement client-side filtering:
        Add an event listener to the price filter dropdown to filter places based on the selected price.
        The filter will set the top price for the places to be shown.
        The dropdown must be loaded with the following options:
        10
        50
        100
        All

  document.getElementById('price-filter').addEventListener('change', (event) => {
      // Get the selected price value
      // Iterate over the places and show/hide them based on the selected price
  });

    Testing:
        Test the functionality by logging in and viewing the list of places.
        Verify that the client-side filter works as expected.
        Ensure the login link appears only when the user is not authenticated.

Resources

    Fetch API https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
    Handling Cookies in JavaScript : https://developer.mozilla.org/en-US/docs/Web/API/Document/cookie
    DOM Manipulation : https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction

Repo:

    GitHub repository: holbertonschool-hbnb
    Directory: part4



3. Place details
mandatory
Objectives

    Implement the detailed view of a place.
    Fetch place details from the API using the place ID.
    Display detailed information about the place, including name, description, price, amenities and reviews.
    If the user is authenticated, provide access to the form for adding a review.

Requirements

    Use the provided HTML structure in place.html (https://github.com/Holberton-Uy/hbnb-doc/blob/main/part4/base_files/place.html) to display the detailed information of a place.
    Make an AJAX request to the API to fetch the details of the selected place.
    Populate the place details dynamically using JavaScript.
    Show the add review form only if the user is authenticated.

Instructions

    Get Place ID from URL:
        Extract the place ID from the URL query parameters.
        Tip: Use window.location.search to get the query string.

    Check User Authentication:
        On page load, check if the user is authenticated by verifying the presence of the JWT token in cookies.
        Store the token in a variable for later use in API requests.

    Fetch Place Details:
        Use the Fetch API to send a GET request to the endpoint that returns the details of the place.
        Ensure the request includes the JWT token for authentication if available.
        Tip: Include the token in the Authorization header of your request.

    Populate Place Details:
        Dynamically create HTML elements to display the place’s detailed information (e.g., name, description, price, amenities and reviews).
        Append these elements to the #place-details section.

    Show Add Review Form:
        If the user is authenticated, display the add review form.
        Hide the form if the user is not authenticated.

Example Guidance

scripts.js

    Get place ID from URL:
        Create a function to extract the place ID from the query parameters.

  function getPlaceIdFromURL() {
      // Extract the place ID from window.location.search
      // Your code here
  }

    Check user authentication:
        Create a function to check for the JWT token in cookies and store it in a variable.

  function checkAuthentication() {
      const token = getCookie('token');
      const addReviewSection = document.getElementById('add-review');

      if (!token) {
          addReviewSection.style.display = 'none';
      } else {
          addReviewSection.style.display = 'block';
          // Store the token for later use
          fetchPlaceDetails(token, placeId);
      }
  }

  function getCookie(name) {
      // Function to get a cookie value by its name
      // Your code here
  }

    Fetch place details:
        Use the Fetch API to get the details of the place and handle the response.

  async function fetchPlaceDetails(token, placeId) {
      // Make a GET request to fetch place details
      // Include the token in the Authorization header
      // Handle the response and pass the data to displayPlaceDetails function
  }

    Populate place details:
        Create HTML elements for the place details and append them to the #place-details section.

  function displayPlaceDetails(place) {
      // Clear the current content of the place details section
      // Create elements to display the place details (name, description, price, amenities and reviews)
      // Append the created elements to the place details section
  }

    Testing:
        Test the functionality by navigating to the place details page and verifying the displayed information.
        Ensure that the add review form appears only when the user is authenticated.

Resources

    Fetch API : https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
    Handling Cookies in JavaScript : https://developer.mozilla.org/en-US/docs/Web/API/Document/cookie
    DOM Manipulation : https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction

Repo:

    GitHub repository: holbertonschool-hbnb
    Directory: part4



4. Add Review form
mandatory
Objectives

    Implement the form to add a review for a place.
    Ensure only authenticated users can submit reviews.
    Redirect unauthenticated users to the index page.
    Send the review data to the API endpoint and handle the response.

Requirements

    Use the provided HTML structure in add_review.html (https://github.com/Holberton-Uy/hbnb-doc/blob/main/part4/base_files/add_review.html) to create the review form.
    Make an AJAX request to the API to submit the review data.
    If the user is not authenticated, redirect them to the index page.
    Display a success message upon successful submission and handle errors appropriately.

Instructions

    Check User Authentication:
        On page load, check if the user is authenticated by verifying the presence of the JWT token in cookies.
        If the token is not found, redirect the user to the index page.
        Store the token in a variable for later use in API requests.

    Get Place ID from URL:
        Extract the place ID from the URL query parameters.
        Tip: Use window.location.search to get the query string.

    Setup Event Listener for Review Form:
        Add an event listener to the review form to handle the form submission.
        Use preventDefault to prevent the default form submission behavior.

    Make AJAX Request to Submit Review:
        Use the Fetch API to send a POST request to the endpoint that submits the review data.
        Include the JWT token in the Authorization header.
        Send the review text and place ID in the request body as a JSON object.

    Handle API Response:
        If the submission is successful, display a success message and clear the form.
        If the submission fails, display an error message to the user.

Example Guidance

scripts.js

    Check user authentication:
        Create a function to check for the JWT token in cookies and redirect unauthenticated users.

  function checkAuthentication() {
      const token = getCookie('token');
      if (!token) {
          window.location.href = 'index.html';
      }
      return token;
  }

  function getCookie(name) {
      // Function to get a cookie value by its name
      // Your code here
  }

    Get place ID from URL:
        Create a function to extract the place ID from the query parameters.

  function getPlaceIdFromURL() {
      // Extract the place ID from window.location.search
      // Your code here
  }

    Setup event listener for review form:
        Add an event listener for the form submission to handle the review data.

  document.addEventListener('DOMContentLoaded', () => {
      const reviewForm = document.getElementById('review-form');
      const token = checkAuthentication();
      const placeId = getPlaceIdFromURL();

      if (reviewForm) {
          reviewForm.addEventListener('submit', async (event) => {
              event.preventDefault();
              // Get review text from form
              // Make AJAX request to submit review
              // Handle the response
          });
      }
  });

    Make AJAX request to submit review:
        Use the Fetch API to send a POST request with the review data.

  async function submitReview(token, placeId, reviewText) {
      // Make a POST request to submit review data
      // Include the token in the Authorization header
      // Send placeId and reviewText in the request body
      // Handle the response
  }

    Handle API response:
        Display a success message if the submission is successful and clear the form.
        Display an error message if the submission fails.

  function handleResponse(response) {
      if (response.ok) {
          alert('Review submitted successfully!');
          // Clear the form
      } else {
          alert('Failed to submit review');
      }
  }

    Testing:
        Test the functionality by submitting reviews for a place as an authenticated user.
        Verify that unauthenticated users are redirected to the index page.
        Ensure that success and error messages are displayed appropriately.

Resources

    Fetch API : https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
    Handling Cookies in JavaScript : https://developer.mozilla.org/en-US/docs/Web/API/Document/cookie
    DOM Manipulation : https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction
    FormData API : https://developer.mozilla.org/en-US/docs/Web/API/FormData

Repo:

    GitHub repository: holbertonschool-hbnb
    Directory: part4

