document.getElementById('studentForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const nomeInput = document.getElementById('nome');
    const emailInput = document.getElementById('email');
    let isValid = true;

    // Reset de validações
    [nomeInput, emailInput].forEach(input => input.classList.remove('invalid'));

    // Validação Nome
    if (nomeInput.value.trim().length < 3) {
        nomeInput.classList.add('invalid');
        isValid = false;
    }

    // Validação Email (Regex Simples)
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(emailInput.value)) {
        emailInput.classList.add('invalid');
        isValid = false;
    }

    if (isValid) {
        const studentData = {
            nome: nomeInput.value,
            email: emailInput.value
        };

        console.log('Enviando para o backend Python:', studentData);

        // Exemplo de Integração:
        /*
        try {
            const response = await fetch('http://localhost:8000/alunos', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(studentData)
            });
            if (response.ok) {
                alert('Aluno cadastrado com sucesso!');
                window.location.href = 'alunos.html';
            }
        } catch (error) {
            console.error('Erro na conexão:', error);
        }
        */

        // Simulação de sucesso
        alert('Aluno cadastrado com sucesso!');
        window.location.href = 'alunos.html';
    }
});