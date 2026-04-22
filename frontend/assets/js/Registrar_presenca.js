document.addEventListener('DOMContentLoaded', async () => {
    // Declaramos o token logo no início do escopo
    const token = localStorage.getItem('access_token');

    // Se o token não existir, nem tenta rodar o resto
    if (!token) {
        console.error("Token não encontrado!");
        window.location.href = 'login.html';
        return;
    }

    const studentInput = document.getElementById('studentSearch');
    const groupSelect = document.getElementById('groupSelect');
    const autocompleteList = document.getElementById('autocompleteList');
    const presenceForm = document.getElementById('presenceForm');

    let alunos = [];

    // 1. Carregar Turmas
    async function carregarTurmas() {
        try {
            const response = await fetch('http://localhost:8000/groups', {
                headers: { 'Authorization': `Bearer ${token}` } // Aqui ele usa o token local
            });
            if (response.ok) {
                const turmas = await response.json();
                turmas.forEach(turma => {
                    const option = document.createElement('option');
                    option.value = turma.id;
                    option.textContent = turma.name;
                    groupSelect.appendChild(option);
                });
            }
        } catch (error) { console.error("Erro ao carregar turmas:", error); }
    }

    // 2. Carregar Alunos
    async function carregarAlunos() {
        try {
            const response = await fetch('http://localhost:8000/students', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (response.ok) {
                const data = await response.json();
                alunos = data.map(aluno => aluno.name);
            }
        } catch (error) { console.error("Erro de conexão:", error); }
    }

    // Inicialização
    await carregarTurmas();
    await carregarAlunos();

    // ... Lógica de Autocomplete (Mantida) ...
    studentInput.addEventListener('input', function() {
        const val = this.value;
        autocompleteList.innerHTML = '';
        if (!val) return false;
        const filtered = alunos.filter(a => a.toLowerCase().includes(val.toLowerCase()));
        filtered.forEach(aluno => {
            const div = document.createElement('div');
            div.className = 'autocomplete-item';
            div.innerHTML = `<strong>${aluno.substr(0, val.length)}</strong>${aluno.substr(val.length)}`;
            div.addEventListener('click', function() {
                studentInput.value = aluno;
                autocompleteList.innerHTML = '';
            });
            autocompleteList.appendChild(div);
        });
    });

    // 4. Submissão
    presenceForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const groupId = groupSelect.value;
        const studentName = studentInput.value;

        if (!groupId || !studentName) {
            alert('Selecione a turma e o aluno.');
            return;
        }

        if (!alunos.includes(studentName)) {
            alert('Aluno não encontrado na lista.');
            return;
        }

        document.getElementById('feedbackContainer').style.display = 'flex';

        setTimeout(() => {
            const nomeCodificado = encodeURIComponent(studentName);
            window.location.href = `reconhecimentoFace.html?aluno=${nomeCodificado}&group_id=${groupId}`;
        }, 1500);
    });
});