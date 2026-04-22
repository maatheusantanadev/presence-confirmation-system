document.addEventListener('DOMContentLoaded', async () => {
    const studentsList = document.getElementById('studentsList');
    const studentSearch = document.getElementById('studentSearch');
    const groupForm = document.getElementById('groupForm');
    const selectedCountText = document.getElementById('selectedCount');

    let allStudents = [];
    let selectedStudents = new Set();

    async function loadStudents() {
        const token = localStorage.getItem('access_token');
        try {
            const response = await fetch('http://localhost:8000/students', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (response.ok) {
                allStudents = await response.json();
                renderStudentList(allStudents);
            }
        } catch (error) {
            console.error("Erro ao carregar alunos:", error);
        }
    }

    function renderStudentList(students) {
        studentsList.innerHTML = '';
        if (students.length === 0) {
            studentsList.innerHTML = '<p class="empty-text">Nenhum aluno encontrado.</p>';
            return;
        }

        students.forEach(student => {
            const item = document.createElement('div');
            item.className = 'student-item';

            // Usamos registration_number que é o que o seu Service Python exige
            const matricula = student.registration_number;
            const isChecked = selectedStudents.has(matricula) ? 'checked' : '';

            item.innerHTML = `
                <label>
                    <input type="checkbox" value="${matricula}" ${isChecked}>
                    <div class="student-details">
                        <span class="name">${student.name}</span>
                        <span class="registration">Matrícula: ${matricula}</span>
                    </div>
                </label>
            `;

            const checkbox = item.querySelector('input');
            checkbox.addEventListener('change', (e) => {
                if (e.target.checked) selectedStudents.add(e.target.value);
                else selectedStudents.delete(e.target.value);
                updateCount();
            });

            studentsList.appendChild(item);
        });
    }

    function updateCount() {
        selectedCountText.textContent = `${selectedStudents.size} alunos selecionados`;
    }

    studentSearch.addEventListener('input', (e) => {
        const term = e.target.value.toLowerCase();
        const filtered = allStudents.filter(s =>
            s.name.toLowerCase().includes(term) ||
            s.registration_number.toLowerCase().includes(term)
        );
        renderStudentList(filtered);
    });

    groupForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (selectedStudents.size === 0) {
            alert("Selecione pelo menos um aluno.");
            return;
        }

        // Recupera o CPF do professor logado (deve ser salvo no localStorage no Login)
        const profCpf = localStorage.getItem('user_cpf');

        const groupData = {
            name: document.getElementById('groupName').value,
            professor_cpf: profCpf || "12345678901", // Fallback para teste se necessário
            student_registration_numbers: Array.from(selectedStudents)
        };

        const token = localStorage.getItem('access_token');
        try {
            const response = await fetch('http://localhost:8000/groups', { // Removi a barra final aqui
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(groupData)
            });

            if (response.ok) {
                alert("Turma criada com sucesso!");
                window.location.href = 'turmas.html';
            } else {
                const err = await response.json();
                alert("Erro: " + (err.detail || "Falha ao criar turma."));
            }
        } catch (error) {
            console.error(error);
        }
    });

    loadStudents();
});