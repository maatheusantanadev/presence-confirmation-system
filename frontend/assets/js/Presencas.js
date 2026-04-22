document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = 'login.html';
        return;
    }

    const tableBody = document.getElementById('presenceTableBody');
    const noData = document.getElementById('noData');
    const applyBtn = document.getElementById('applyFilters');

    async function fetchHistory() {
        setLoading(true);
        try {
            // Pegamos os valores dos filtros
            const nameFilter = document.getElementById('nameFilter').value.toLowerCase();
            const dateStart = document.getElementById('dateStart').value;
            const dateEnd = document.getElementById('dateEnd').value;

            // Busca no backend
            const response = await fetch('http://localhost:8000/presence/history', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Accept': 'application/json'
                }
            });

            if (!response.ok) throw new Error("Falha ao buscar dados");

            const data = await response.json();

            // Renderizamos passando o filtro de nome
            renderTable(data, nameFilter);

        } catch (error) {
            console.error("Erro na requisição:", error);
            tableBody.innerHTML = '<tr><td colspan="5" style="text-align:center; color:red; padding:20px;">Erro ao conectar com o servidor.</td></tr>';
        } finally {
            setLoading(false);
        }
    }

    function renderTable(data, filter) {
        tableBody.innerHTML = '';
        const entries = Object.entries(data);
        let hasRecords = false;

        if (entries.length === 0) {
            noData.style.display = 'block';
            return;
        }

        entries.forEach(([groupName, presences]) => {
            // Filtramos os alunos localmente pelo nome/email caso haja busca
            const filtered = presences.filter(p =>
                p.aluno.toLowerCase().includes(filter) ||
                (p.email && p.email.toLowerCase().includes(filter))
            );

            if (filtered.length > 0) {
                hasRecords = true;

                // 1. Linha de Título da Turma (Visualmente igual ao Dashboard)
                const groupHeader = document.createElement('tr');
                groupHeader.innerHTML = `
                    <td colspan="5" style="background-color: #f8fafc; font-weight: bold; color: #2563eb; border-left: 4px solid #2563eb;">
                        <i class="fas fa-users" style="margin-right: 8px;"></i> Turma: ${groupName}
                    </td>
                `;
                tableBody.appendChild(groupHeader);

                // 2. Linhas dos Alunos
                filtered.forEach(reg => {
                    const tr = document.createElement('tr');
                    // O backend envia "DD/MM/YYYY HH:MM"
                    const [dataStr, horaStr] = reg.data.split(' ');

                    tr.innerHTML = `
                        <td><strong>${reg.aluno}</strong></td>
                        <td>${reg.email || '---'}</td>
                        <td>${dataStr}</td>
                        <td>${horaStr}</td>
                        <td><span class="status-badge">${reg.status.toUpperCase()}</span></td>
                    `;
                    tableBody.appendChild(tr);
                });
            }
        });

        // Exibe mensagem de "Nenhum resultado" se os filtros esconderem tudo
        noData.style.display = hasRecords ? 'none' : 'block';
    }

    function setLoading(isLoading) {
        applyBtn.disabled = isLoading;
        applyBtn.innerHTML = isLoading ?
            '<i class="fas fa-spinner fa-spin"></i> Filtrando...' :
            '<i class="fas fa-filter"></i> Filtrar';
    }

    // Botão Filtrar
    applyBtn.addEventListener('click', fetchHistory);

    // Logout
    document.getElementById('logoutBtn').addEventListener('click', (e) => {
        e.preventDefault();
        localStorage.removeItem('access_token');
        window.location.href = 'login.html';
    });

    // Carga Inicial
    fetchHistory();
});