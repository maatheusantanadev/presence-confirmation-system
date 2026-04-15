document.addEventListener('DOMContentLoaded', () => {
    // Mock de dados para simular o retorno do Python
    let alunos = [
        { id: 1, nome: "Ana Silva", email: "ana.silva@email.com" },
        { id: 2, nome: "Bruno Oliveira", email: "bruno.o@email.com" },
        { id: 3, nome: "Carlos Eduardo", email: "cadu@email.com" },
        { id: 4, nome: "Daniela Costa", email: "dani.costa@email.com" }
    ];

    const tableBody = document.getElementById('studentTableBody');
    const searchInput = document.getElementById('searchStudent');

    // Função para renderizar a tabela
    function renderTable(data) {
        tableBody.innerHTML = '';
        
        data.forEach(aluno => {
            const row = `
                <tr>
                    <td><strong>${aluno.nome}</strong></td>
                    <td>${aluno.email}</td>
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

    // Filtro de busca
    searchInput.addEventListener('input', (e) => {
        const term = e.target.value.toLowerCase();
        const filtered = alunos.filter(a => 
            a.nome.toLowerCase().includes(term) || 
            a.email.toLowerCase().includes(term)
        );
        renderTable(filtered);
    });

    // Inicializar
    renderTable(alunos);
});

// Funções de Ação (Para integrar com o Back em Python futuramente)
function editarAluno(id) {
    console.log(`Editando aluno ID: ${id}`);
    window.location.href = `edicao_aluno.html?id=${id}`;
}

function excluirAluno(id) {
    if(confirm('Tem certeza que deseja remover este aluno?')) {
        console.log(`Excluindo aluno ID: ${id}`);
        // Aqui você faria o fetch(DELETE) para o seu backend
    }
}