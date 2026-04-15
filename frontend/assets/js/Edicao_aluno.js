document.addEventListener('DOMContentLoaded', async () => {
    const nomeInput = document.getElementById('nome');
    const emailInput = document.getElementById('email');
    const formCard = document.getElementById('editCard');
    const form = document.getElementById('editStudentForm');

    // 1. Pega o ID do aluno pela URL (ex: edicao_aluno.html?id=123)
    const urlParams = new URLSearchParams(window.location.search);
    const alunoId = urlParams.get('id');

    // 2. Simulação de busca no Backend Python
    async function loadAlunoData() {
        // Simulando delay de rede para mostrar a transição
        await new Promise(res => setTimeout(res, 500));

        // Aqui você faria: const resp = await fetch(`http://localhost:8000/alunos/${alunoId}`)
        const mockAluno = {
            nome: "Matheus Exemplo",
            email: "matheus@universidade.com"
        };

        nomeInput.value = mockAluno.nome;
        emailInput.value = mockAluno.email;
        
        // Exibe o card com a animação CSS
        formCard.style.display = 'block';
    }

    loadAlunoData();

    // 3. Lógica de Salvar
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        let isValid = true;
        const saveBtn = document.getElementById('saveBtn');
        const successBox = document.getElementById('successFeedback');

        // Validação básica
        if (nomeInput.value.trim().length < 3) {
            nomeInput.classList.add('invalid');
            isValid = false;
        } else {
            nomeInput.classList.remove('invalid');
        }

        if (!emailInput.value.includes('@')) {
            emailInput.classList.add('invalid');
            isValid = false;
        } else {
            emailInput.classList.remove('invalid');
        }

        if (isValid) {
            saveBtn.disabled = true;
            saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Salvando...';

            // Simulação de PUT no Python
            setTimeout(() => {
                saveBtn.style.display = 'none';
                successBox.style.display = 'block';

                // Redireciona após 1.5s
                setTimeout(() => {
                    window.location.href = 'alunos.html';
                }, 1500);
            }, 1000);
        }
    });
});