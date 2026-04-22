document.addEventListener('DOMContentLoaded', async () => {
    const studentInput = document.getElementById('studentSearch');
    const autocompleteList = document.getElementById('autocompleteList');
    const presenceForm = document.getElementById('presenceForm');

    // Variável para armazenar os alunos vindos do Python
    let alunos = [];

    // 1. Atualização Relógio (Mantido)
    function updateDateTime() {
        const now = new Date();
        const dateStr = now.toLocaleDateString('pt-BR');
        const timeStr = now.toLocaleTimeString('pt-BR');
        document.getElementById('currentDateTime').innerHTML = `
            <span class="date"><i class="far fa-calendar-alt"></i> ${dateStr}</span>
            <span class="time"><i class="far fa-clock"></i> ${timeStr}</span>
        `;
    }
    setInterval(updateDateTime, 1000);
    updateDateTime();

    // 2. Busca Real de Alunos do Backend
    async function carregarAlunos() {
        const token = localStorage.getItem('access_token');
        try {
            const response = await fetch('http://localhost:8000/students', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                // Mapeia apenas o nome (ou 'name' conforme seu banco) para o array
                alunos = data.map(aluno => aluno.name || aluno.nome);
            } else {
                console.error("Erro ao carregar alunos do banco.");
            }
        } catch (error) {
            console.error("Erro de conexão:", error);
        }
    }

    // Inicializa a busca
    await carregarAlunos();

    // 3. Autocomplete (Ajustado para usar a variável 'alunos' vinda do banco)
    studentInput.addEventListener('input', function() {
        const val = this.value;
        autocompleteList.innerHTML = '';
        if (!val) return false;

        const filtered = alunos.filter(a => a.toLowerCase().includes(val.toLowerCase()));

        filtered.forEach(aluno => {
            const div = document.createElement('div');
            div.className = 'autocomplete-item'; // Boa prática para CSS
            div.innerHTML = `<strong>${aluno.substr(0, val.length)}</strong>${aluno.substr(val.length)}`;

            div.addEventListener('click', function() {
                studentInput.value = aluno;
                autocompleteList.innerHTML = '';
            });
            autocompleteList.appendChild(div);
        });
    });

    // 4. Submissão e Redirecionamento
    presenceForm.addEventListener('submit', (e) => {
        e.preventDefault();

        if (!studentInput.value) {
            alert('Por favor, selecione um aluno.');
            return;
        }

        // Verifica se o nome digitado realmente existe na lista carregada
        if (!alunos.includes(studentInput.value)) {
            alert('Aluno não encontrado. Selecione um nome da lista.');
            return;
        }

        // Feedback visual antes de mudar de página
        document.getElementById('feedbackContainer').style.display = 'flex';

        // Redireciona para o Reconhecimento Facial após 1.5 segundos
        setTimeout(() => {
            // Passamos o nome do aluno via URL para a próxima tela saber quem é
            const nomeCodificado = encodeURIComponent(studentInput.value);
            window.location.href = `reconhecimentoFace.html?aluno=${nomeCodificado}`;
        }, 1500);
    });
});

function resetForm() {
    document.getElementById('presenceForm').reset();
    document.getElementById('feedbackContainer').style.display = 'none';
}