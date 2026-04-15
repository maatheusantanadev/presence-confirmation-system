document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username');
    const password = document.getElementById('password');
    const role = document.getElementById('role');
    const apiResponse = document.getElementById('apiResponse');

    // Reset de estilos
    [username, password, role].forEach(el => el.classList.remove('invalid'));
    apiResponse.style.display = 'none';

    // 1. Validações Locais (Espelhando o Backend)
    let hasError = false;

    if (username.value.trim().length < 3) {
        username.classList.add('invalid');
        hasError = true;
    }

    const passVal = password.value;
    const hasUpper = /[A-Z]/.test(passVal);
    const hasNum = /\d/.test(passVal);
    
    if (passVal.length < 6 || !hasUpper || !hasNum) {
        password.classList.add('invalid');
        hasError = true;
    }

    if (hasError) return;

    // 2. Preparação dos dados
    const userData = {
        username: username.value,
        password: password.value,
        role: role.value || "admin"
    };

    try {
        const response = await fetch('http://localhost:8000/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });

        const result = await response.json();

        if (response.ok) {
            apiResponse.className = "message success";
            apiResponse.textContent = "Usuário criado com sucesso!";
            apiResponse.style.display = 'block';
            document.getElementById('registerForm').reset();
        } else {
            // Trata erros vindos do FastAPI (400, 422, etc)
            apiResponse.className = "message error";
            apiResponse.textContent = result.detail || "Erro ao cadastrar usuário.";
            apiResponse.style.display = 'block';
        }

    } catch (error) {
        apiResponse.className = "message error";
        apiResponse.textContent = "Erro de conexão com o servidor.";
        apiResponse.style.display = 'block';
    }
});