function toggleDropdown(element) {
    let dropdowns = document.getElementsByClassName("dropdown-content");

    // Close all open dropdowns
    for (const element of dropdowns) {
        let openDropdown = element;
        if (openDropdown.classList.contains('show')) {
            openDropdown.classList.remove('show');
        }
    }

    // Toggle the current dropdown
    element.nextElementSibling.classList.toggle("show");
}

// Add an event listener to each button with the class "dropbtn"
let buttons = document.querySelectorAll(".dropbtn");
buttons.forEach(function(button) {
    button.addEventListener("click", function() {
        toggleDropdown(this); // Pass the button element as a reference
    });
});

// Close the dropdown when the user clicks outside of it
window.addEventListener("click", function(event) {
    if (!event.target.matches('.dropbtn')) {
        let dropdowns = document.getElementsByClassName("dropdown-content");
        for (const element of dropdowns) {
            let openDropdown = element;
            if (openDropdown.classList.contains("show")) {
                openDropdown.classList.remove("show");
            }
        }
    }
});