document.addEventListener('DOMContentLoaded', () => {
    const studentInput = document.getElementById('studentSearch');
    const autocompleteList = document.getElementById('autocompleteList');
    const presenceForm = document.getElementById('presenceForm');
    
    // 1. Atualização Relógio
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

    // 2. Mock de Alunos (Simulando vindo do Python)
    const alunos = ["Ana Silva", "Bruno Santos", "Carlos Souza", "Daniela Oliveira", "Eduardo Lima"];

    studentInput.addEventListener('input', function() {
        const val = this.value;
        autocompleteList.innerHTML = '';
        if (!val) return false;

        const filtered = alunos.filter(a => a.toLowerCase().includes(val.toLowerCase()));
        filtered.forEach(aluno => {
            const div = document.createElement('div');
            div.innerHTML = aluno;
            div.addEventListener('click', function() {
                studentInput.value = aluno;
                autocompleteList.innerHTML = '';
            });
            autocompleteList.appendChild(div);
        });
    });

    // 3. Submissão
    presenceForm.addEventListener('submit', (e) => {
        e.preventDefault();
        if (!studentInput.value) {
            alert('Por favor, selecione um aluno.');
            return;
        }

        // Aqui você chamaria seu Back Python
        document.getElementById('feedbackContainer').style.display = 'flex';
    });
});

function resetForm() {
    document.getElementById('presenceForm').reset();
    document.getElementById('feedbackContainer').style.display = 'none';
}