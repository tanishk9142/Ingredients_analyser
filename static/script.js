document.getElementById('ingredient-form').addEventListener('submit', function (e) {
    e.preventDefault(); // Prevent default form submission behavior

    // Show the loading spinner and hide the results
    const loadingSpinner = document.getElementById('loading-spinner');
    loadingSpinner.style.display = 'block';
    document.getElementById('results').innerHTML = '';  // Clear previous results

    // Get the form data
    var formData = new FormData(this);

    // Make the request to the backend
    fetch('/process', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        // Hide the loading spinner
        loadingSpinner.style.display = 'none';

        // Display the result
        document.getElementById('results').innerHTML = data;
    })
    .catch(error => {
        console.error('Error:', error);
        // Hide the spinner if there's an error
        loadingSpinner.style.display = 'none';
        document.getElementById('results').innerHTML = '<p class="text-danger">An error occurred. Please try again.</p>';
    });
});

// Function to toggle the display of ingredient details
function toggleDetails(element) {
    const details = element.nextElementSibling;
    details.style.display = details.style.display === 'none' ? 'block' : 'none';
    element.setAttribute("aria-expanded", details.style.display === 'block' ? "true" : "false");
}
