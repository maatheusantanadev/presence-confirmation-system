document.addEventListener('DOMContentLoaded', () => {
    // Mock de dados vindos do backend Python
    const registros = [
        { nome: "Ana Silva", email: "ana.silva@email.com", data: "2026-04-14", hora: "08:15" },
        { nome: "Bruno Santos", email: "bruno.s@email.com", data: "2026-04-14", hora: "08:20" },
        { nome: "Carlos Souza", email: "cadu@email.com", data: "2026-04-13", hora: "19:05" },
        { nome: "Daniela Oliveira", email: "dani.o@email.com", data: "2026-04-12", hora: "08:02" }
    ];

    const tableBody = document.getElementById('presenceTableBody');
    const applyBtn = document.getElementById('applyFilters');
    const noData = document.getElementById('noData');

    function renderTable(data) {
        tableBody.innerHTML = '';
        if (data.length === 0) {
            noData.style.display = 'block';
            return;
        }
        
        noData.style.display = 'none';
        data.forEach(reg => {
            const row = `
                <tr>
                    <td><strong>${reg.nome}</strong></td>
                    <td>${reg.email}</td>
                    <td>${formatDate(reg.data)}</td>
                    <td>${reg.hora}</td>
                    <td><span class="status-badge">Presente</span></td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });
    }

    function formatDate(dateStr) {
        const [year, month, day] = dateStr.split('-');
        return `${day}/${month}/${year}`;
    }

    // Lógica de Filtro (Simulada)
    applyBtn.addEventListener('click', () => {
        applyBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Filtrando...';
        
        setTimeout(() => {
            const searchTerm = document.getElementById('nameFilter').value.toLowerCase();
            const filtered = registros.filter(r => 
                r.nome.toLowerCase().includes(searchTerm) || 
                r.email.toLowerCase().includes(searchTerm)
            );
            
            renderTable(filtered);
            applyBtn.innerHTML = '<i class="fas fa-filter"></i> Filtrar';
        }, 600);
    });

    // Exportar (Exemplo de log)
    document.getElementById('exportBtn').addEventListener('click', () => {
        alert('Relatório gerado! O download do PDF/Excel começará em instantes.');
    });

    // Inicialização
    renderTable(registros);
});