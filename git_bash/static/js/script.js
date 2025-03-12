document.getElementById("signup-form").addEventListener("submit", async function (e) {
    e.preventDefault(); // Prevent standard form submission

    // Get form field values
    const firstName = document.getElementById("name").value.trim();
    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const confirmPassword = document.getElementById("confirm-password").value.trim();

    // Display errors in this element
    const errorMessage = document.getElementById("error-message");

    // Clear previous errors
    errorMessage.innerText = "";
    errorMessage.style.color = "red";

    // Basic client-side validation
    let errors = [];
    if (!firstName) errors.push("Name is required.");
    if (!username) errors.push("Username is required.");
    if (!email) errors.push("Email is required.");
    if (!password) errors.push("Password is required.");
    if (password.length < 8) errors.push("Password must be at least 8 characters long.");
    if (password !== confirmPassword) errors.push("Passwords do not match.");

    // If any validation errors, show them and stop
    if (errors.length > 0) {
        errorMessage.innerText = errors.join(" ");
        return;
    }

    try {
        // Send JSON data to Flask
        const response = await fetch(signUpUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                first_name: firstName,        // Match your Flask keys
                username: username,
                email: email,
                password: password,
                confirm_password: confirmPassword,
            }),
        });

        // Parse response as JSON
        const result = await response.json();

        // Check if request was successful
        if (!response.ok) {
            // If status >= 400, display error message
            errorMessage.innerText = result.message || "An error occurred. Please try again.";
            console.error("Sign-up failed:", result);
            return;
        }

        // If there's a redirect in the JSON, navigate there
        if (result.redirect) {
            window.location.href = result.redirect;
            return;
        }

        // Otherwise, just show a success message
        alert(result.message);

    } catch (error) {
        console.error("Fetch Error:", error);
        errorMessage.innerText = "Failed to connect to the server. Please try again later.";
    }
});


document.getElementById("login-form").addEventListener("submit", async function (e) {
    e.preventDefault();  // ✅ Prevent standard form submission

    const formData = new FormData(this);
    const email = formData.get("email").trim();
    const password = formData.get("password").trim();
    const errorMessage = document.getElementById("error-message");

    errorMessage.innerText = "";
    errorMessage.style.color = "red";

    if (!email || !password) {
        errorMessage.innerText = "Please enter both email and password.";
        return;
    }

    try {
        console.log("Sending request to /sign_in...");

        const response = await fetch("/sign_in", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            // ✅ Convert form data to URL-encoded string
            body: new URLSearchParams({ email, password })
        });

        const result = await response.json();
        console.log("Server Response:", result);

        if (response.ok && result.redirect) {
            // ✅ Redirect on success
            window.location.href = result.redirect;
            return;
        }

        // If no redirect, show the error message
        errorMessage.innerText = result.message || "Invalid email or password.";
        console.error("Sign-in failed:", result);

    } catch (error) {
        console.error("Fetch Error:", error);
        errorMessage.innerText = "Failed to connect to the server. Please try again later.";
    }
});
