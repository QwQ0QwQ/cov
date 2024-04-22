modifyButton.onclick = async (e) => {
    e.preventDefault();  // Prevent default form submission

    // Get the modified content from the UI (replace with your content retrieval logic)
    const modifiedContent = document.getElementById('modified-content-input').value; // Assuming an input with this ID holds the content
    console.log(modifiedContent)
    // Check if content is empty (optional, replace with your validation logic)
    if (!modifiedContent.trim()) {
        msg('Please enter content to modify the file!', 'danger');
        return;
    }

    // Send the modified content to the server using fetch (assuming a POST request)
    fetch('/modify_tagconfig', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // Set content type to JSON
        },
        body: JSON.stringify({ content: modifiedContent }) // Send content as JSON data
    })
        .then((response) => response.json())
    .then((data) => {
      // Handle successful modification response
      msg(data.message, 'success'); // Assuming the response contains a message
    })
    .catch((error) => {
      // Handle errors during modification
      msg('Error modifying file!', 'danger');
      console.error(error); // Log the error for debugging
    });
};


function msg(message, messageType) {
  // Use Alert for popups (consider using a library for more advanced notifications)
  if (messageType === 'success') {
    alert(`Success! ${message}`);
  } else {
    alert(`Error: ${message}`);
  }
}