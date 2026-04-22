document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const fullName = document.getElementById('full_name');
    const cpf = document.getElementById('cpf');
    const username = document.getElementById('username');
    const password = document.getElementById('password');
    const apiResponse = document.getElementById('apiResponse');

    // Reset visual
    [fullName, cpf, username, password].forEach(el => el.classList.remove('invalid'));
    apiResponse.style.display = 'none';

    let hasError = false;

    // Validação CPF (apenas números)
    const cpfClean = cpf.value.replace(/\D/g, '');
    if (cpfClean.length !== 11) {
        cpf.classList.add('invalid');
        hasError = true;
    }

    if (fullName.value.trim().length < 3) {
        fullName.classList.add('invalid');
        hasError = true;
    }

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

    // Preparação dos dados para o seu Schema Pydantic
    const userData = {
        full_name: fullName.value,
        cpf: cpfClean, // Envia apenas números para o backend
        username: username.value,
        password: password.value
    };

    try {
        const response = await fetch('http://localhost:8000/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData)
        });

        const result = await response.json();

        if (response.ok) {
            apiResponse.className = "message success";
            apiResponse.textContent = "Professor registrado! Redirecionando...";
            apiResponse.style.display = 'block';

            // Salva o CPF no localStorage para uso futuro nas turmas
            localStorage.setItem('user_cpf', cpfClean);

            setTimeout(() => {
                window.location.href = 'login.html';
            }, 2000);
        } else {
            apiResponse.className = "message error";
            apiResponse.textContent = result.detail || "Erro ao cadastrar professor.";
            apiResponse.style.display = 'block';
        }

    } catch (error) {
        apiResponse.className = "message error";
        apiResponse.textContent = "Erro de conexão com o servidor.";
        apiResponse.style.display = 'block';
    }
});