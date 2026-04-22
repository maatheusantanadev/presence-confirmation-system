document.addEventListener('DOMContentLoaded', () => {
    const studentForm = document.getElementById('studentForm');

    studentForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const nomeInput = document.getElementById('nome');
        const regInput = document.getElementById('registration'); // Novo
        const emailInput = document.getElementById('email');

        let isValid = true;

        // Limpar estados inválidos
        [nomeInput, regInput, emailInput].forEach(el => el.classList.remove('invalid'));

        // Validação Nome
        if (nomeInput.value.trim().length < 3) {
            nomeInput.classList.add('invalid');
            isValid = false;
        }

        // Validação Matrícula
        if (regInput.value.trim().length < 2) {
            regInput.classList.add('invalid');
            isValid = false;
        }

        // Validação E-mail
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(emailInput.value)) {
            emailInput.classList.add('invalid');
            isValid = false;
        }

        if (!isValid) return;

        const token = localStorage.getItem('access_token');

        // Objeto adequado ao seu Model/Schema Python
        const studentData = {
            name: nomeInput.value,
            registration_number: regInput.value, // CHAVE CORRETA
            email: emailInput.value
        };

        try {
            const response = await fetch('http://localhost:8000/students', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(studentData)
            });

            if (response.ok) {
                alert('Aluno cadastrado com sucesso!');
                window.location.href = 'alunos.html';
            } else {
                const errorDetail = await response.json();
                alert("Erro ao salvar: " + (errorDetail.detail || "Verifique os dados."));
            }

        } catch (error) {
            alert('Não foi possível conectar ao servidor.');
        }
    });
});