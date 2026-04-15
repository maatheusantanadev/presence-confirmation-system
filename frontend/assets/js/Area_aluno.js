document.addEventListener('DOMContentLoaded', () => {
    // Mock de dados do aluno (vindo do seu Back em Python)
    const historico = [
        { data: "14 Abr", hora: "08:15", aula: "Estrutura de Dados", status: "Presente" },
        { data: "12 Abr", hora: "10:30", aula: "Banco de Dados II", status: "Presente" },
        { data: "10 Abr", hora: "08:05", aula: "Estrutura de Dados", status: "Presente" },
        { data: "08 Abr", hora: "19:15", aula: "Engenharia de Software", status: "Presente" }
    ];

    const listContainer = document.getElementById('presenceList');
    const totalDisplay = document.getElementById('totalPresence');
    const countDisplay = document.getElementById('listCount');

    // Atualizar indicadores
    totalDisplay.textContent = historico.length;
    countDisplay.textContent = `${historico.length} registros`;

    // Renderizar lista
    historico.forEach(item => {
        const itemHtml = `
            <div class="presence-item">
                <div class="date-icon">
                    <i class="far fa-calendar"></i>
                    <span>${item.data.split(' ')[0]}</span>
                </div>
                <div class="item-info">
                    <h4>${item.aula}</h4>
                    <p><i class="far fa-clock"></i> ${item.hora}</p>
                </div>
                <span class="status-badge">${item.status}</span>
            </div>
        `;
        listContainer.innerHTML += itemHtml;
    });
});