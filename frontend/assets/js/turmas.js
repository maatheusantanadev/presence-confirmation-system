document.addEventListener('DOMContentLoaded', async () => {
    const groupsGrid = document.getElementById('groupsGrid');
    const modal = document.getElementById('groupModal');
    const closeModal = document.querySelector('.close-modal');
    let allGroups = [];

    // 1. Busca as turmas do seu Backend Python
    async function fetchGroups() {
        const token = localStorage.getItem('access_token');
        try {
            const response = await fetch('http://localhost:8000/groups/', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (response.ok) {
                allGroups = await response.json();
                renderGroups(allGroups);
            }
        } catch (error) {
            console.error("Erro ao buscar turmas:", error);
        }
    }

    // 2. Renderiza os cards na tela
    function renderGroups(groups) {
        groupsGrid.innerHTML = '';
        groups.forEach(group => {
            const card = document.createElement('div');
            card.className = 'group-card';
            card.innerHTML = `
                <h3>${group.name}</h3>
                <p><i class="fas fa-user-tie"></i> Prof. CPF: ${group.professor_cpf}</p>
                <span><i class="fas fa-graduation-cap"></i> Ver alunos</span>
            `;
            card.onclick = () => showGroupDetails(group);
            groupsGrid.appendChild(card);
        });
    }

    // 3. Mostra o modal com Professor e Alunos
    function showGroupDetails(group) {
        document.getElementById('modalGroupName').textContent = group.name;
        document.getElementById('modalProfessorName').textContent = `Professor (CPF): ${group.professor_cpf}`;

        const list = document.getElementById('modalStudentList');
        list.innerHTML = '';

        // Se o seu backend já retornar a lista de alunos dentro do objeto group:
        if (group.students && group.students.length > 0) {
            group.students.forEach(student => {
                const li = document.createElement('li');
                li.innerHTML = `<span>${student.name}</span> <small>${student.registration_number}</small>`;
                list.appendChild(li);
            });
        } else {
            list.innerHTML = '<li>Nenhum aluno vinculado a esta turma.</li>';
        }

        modal.style.display = 'block';
    }

    // Fechar Modal
    closeModal.onclick = () => modal.style.display = 'none';
    window.onclick = (event) => { if (event.target == modal) modal.style.display = 'none'; }

    fetchGroups();
});