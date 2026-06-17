const API_URL = "http://127.0.0.1:5000/api/auth";

// Guardar token
function storeToken(token) {
  if (token) {
    localStorage.setItem('nexo_token', token);
    console.log('Token guardado:', token);
  }
}

// Intercambio entre Login y Sign Up
function toggleAuth() {
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');
    const title = document.getElementById('form-title');
    const toggleText = document.getElementById('toggle-text');

    if (loginForm.classList.contains('hidden')) {
        loginForm.classList.remove('hidden');
        signupForm.classList.add('hidden');
        title.innerText = "SpicyTech Hub";
        toggleText.innerHTML = '¿No tienes cuenta? <span onclick="toggleAuth()">Regístrate</span>';
    } else {
        loginForm.classList.add('hidden');
        signupForm.classList.remove('hidden');
        title.innerText = "Únete a SpicyTech";
        toggleText.innerHTML = '¿Ya tienes cuenta? <span onclick="toggleAuth()">Inicia Sesión</span>';
    }
}

function showMessage(text, isError = true) {
    const msgDiv = document.getElementById('api-message');
    msgDiv.innerText = text;
    msgDiv.className = `message ${isError ? 'error' : 'success'}`;
    msgDiv.style.display = 'block';
}

// Login
document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        const result = await response.json();
        
        if (result.success) {
            if (result.data && result.data.token) storeToken(result.data.token);
            showMessage(`¡Bienvenido de nuevo, ${result.data.username}!`, false);
            // Aquí podrías redirigir al dashboard
        } else {
            showMessage(result.message);
        }
    } catch (err) {
        showMessage("Error de conexión con el servidor.");
    }
});

// Sign Up
document.getElementById('signup-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        username: document.getElementById('signup-username').value,
        email: document.getElementById('signup-email').value,
        password: document.getElementById('signup-password').value,
        confirm_password: document.getElementById('signup-confirm').value,
        role: "member"
    };

    try {
        const response = await fetch(`${API_URL}/signup`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();

        if (result.success) {
            showMessage("Cuenta creada. ¡Ya puedes iniciar sesión!", false);
            setTimeout(toggleAuth, 2000);
        } else {
            const errorText = result.errors.length > 0 ? result.errors.join(" ") : result.message;
            showMessage(errorText);
        }
    } catch (err) {
        showMessage("Error al intentar registrar el usuario.");
    }
});
