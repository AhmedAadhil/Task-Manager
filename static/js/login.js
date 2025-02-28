document.getElementById("loginForm").addEventListener("submit", async function(event) {
    event.preventDefault(); // Prevent default form submission

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }) 
    });

    const result = await response.json();

    if (response.ok) {
        alert(result.message);
        
        // Store the JWT token
        localStorage.setItem("access_token", result.tokens.access);

        window.location.href = "/dashboard"; // Redirect to dashboard
    } else {
        alert(result.error || "Login failed");
    }
});