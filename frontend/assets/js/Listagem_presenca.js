document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = 'login.html';
        return;
    }

    const tableBody = document.getElementById('presenceTableBody');
    const applyBtn = document.getElementById('applyFilters');
    const noData = document.getElementById('noData');

    async function fetchHistory() {
        setLoading(true);
        try {
            // Pegando valores dos filtros caso o professor queira usar
            const nameFilter = document.getElementById('nameFilter').value;
            const dateStart = document.getElementById('dateStart').value;
            const dateEnd = document.getElementById('dateEnd').value;

            const response = await fetch('http://localhost:8000/presence/history', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Accept': 'application/json'
                }
            });

            if (!response.ok) throw new Error("Falha na requisição");

            const data = await response.json();
            console.log("Dados da Listagem:", data); // Debug no console (F12)

            renderTable(data, nameFilter);

        } catch (error) {
            console.error(error);
            tableBody.innerHTML = '<tr><td colspan="5" style="text-align:center; color:red; padding:20px;">Erro ao carregar dados.</td></tr>';
        } finally {
            setLoading(false);
        }
    }

    function renderTable(data, nameFilter) {
        tableBody.innerHTML = '';
        const entries = Object.entries(data);
        let hasVisibleData = false;

        if (entries.length === 0) {
            noData.style.display = 'block';
            return;
        }

        entries.forEach(([groupName, presences]) => {
            // Filtrar presenças pelo nome se o filtro estiver preenchido
            const filteredPresences = presences.filter(p =>
                p.aluno.toLowerCase().includes(nameFilter.toLowerCase())
            );

            if (filteredPresences.length > 0) {
                hasVisibleData = true;

                // 1. Linha da Turma
                const groupRow = document.createElement('tr');
                groupRow.className = 'group-header-row';
                groupRow.innerHTML = `
                    <td colspan="5" style="background-color: #f8fafc; font-weight: bold; color: #2563eb; border-left: 4px solid #2563eb; padding: 12px 15px;">
                        <i class="fas fa-users"></i> Turma: ${groupName}
                    </td>
                `;
                tableBody.appendChild(groupRow);

                // 2. Linhas dos Alunos
                filteredPresences.forEach(reg => {
                    const row = document.createElement('tr');
                    const [dataStr, horaStr] = reg.data.split(' ');

                    row.innerHTML = `
                        <td><strong>${reg.aluno}</strong></td>
                        <td>${reg.email || '---'}</td>
                        <td>${dataStr}</td>
                        <td>${horaStr}</td>
                        <td><span class="status-badge">${reg.status.toUpperCase()}</span></td>
                    `;
                    tableBody.appendChild(row);
                });
            }
        });

        noData.style.display = hasVisibleData ? 'none' : 'block';
    }

    function setLoading(isLoading) {
        applyBtn.disabled = isLoading;
        applyBtn.innerHTML = isLoading ?
            '<i class="fas fa-spinner fa-spin"></i>' :
            '<i class="fas fa-filter"></i> Filtrar';
    }

    // Eventos
    applyBtn.addEventListener('click', fetchHistory);

    // Inicialização
    fetchHistory();
});