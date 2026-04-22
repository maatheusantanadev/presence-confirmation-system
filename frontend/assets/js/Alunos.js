document.addEventListener('DOMContentLoaded', async () => {
    const tableBody = document.getElementById('studentTableBody');
    const searchInput = document.getElementById('searchStudent');

    // Variável global para armazenar os alunos vindos do banco e permitir o filtro
    let alunosLocal = [];

    // 1. Função para BUSCAR dados do Backend
    async function fetchStudents() {
        const token = localStorage.getItem('access_token');

        try {
            const response = await fetch('http://localhost:8000/students', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                alunosLocal = await response.json();
                renderTable(alunosLocal);
            } else {
                console.error("Erro ao buscar alunos:", response.status);
                if(response.status === 401) window.location.href = 'login.html';
            }
        } catch (error) {
            console.error("Erro de conexão:", error);
        }
    }

    // 2. Função para RENDERIZAR a tabela (ajustada para os nomes do seu Banco: name/email)
    function renderTable(data) {
        tableBody.innerHTML = '';

        data.forEach(aluno => {
            const row = `
                <tr>
                    <td><strong>${aluno.name}</strong></td> <td>${aluno.email}</td>
                    <td class="text-center">
                        <button class="btn-icon btn-edit" onclick="editarAluno(${aluno.id})" title="Editar">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn-icon btn-delete" onclick="excluirAluno(${aluno.id})" title="Excluir">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });
    }

    // 3. Filtro de busca (usando a variável alunosLocal)
    searchInput.addEventListener('input', (e) => {
        const term = e.target.value.toLowerCase();
        const filtered = alunosLocal.filter(a =>
            (a.name && a.name.toLowerCase().includes(term)) ||
            (a.email && a.email.toLowerCase().includes(term))
        );
        renderTable(filtered);
    });

    // Inicializar chamando o backend
    fetchStudents();
});

// Funções de Ação (Ajustadas para o seu backend)
async function excluirAluno(id) {
    if(confirm('Tem certeza que deseja remover este aluno?')) {
        const token = localStorage.getItem('access_token');
        try {
            const response = await fetch(`http://localhost:8000/students/${id}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (response.ok) {
                alert('Aluno removido!');
                location.reload(); // Recarrega a lista
            }
        } catch (error) {
            console.error("Erro ao deletar:", error);
        }
    }
}