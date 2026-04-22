document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = 'login.html';
        return;
    }
    loadPresenceHistory();
});

async function loadPresenceHistory() {
    const container = document.getElementById('presenceContainer');
    const token = localStorage.getItem('access_token');

    try {
        const response = await fetch('http://localhost:8000/presence/history', {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) throw new Error("Erro ao carregar");

        const data = await response.json();
        container.innerHTML = '';

        if (Object.keys(data).length === 0) {
            container.innerHTML = `
                <div class="empty-state" style="text-align:center; padding: 3rem;">
                    <i class="fas fa-calendar-times" style="font-size: 3rem; color: #cbd5e1;"></i>
                    <p style="margin-top: 1rem; color: #64748b;">Nenhuma presença registrada para suas turmas.</p>
                </div>`;
            return;
        }

        // Criar um card para cada turma
        for (const [groupName, students] of Object.entries(data)) {
            const card = document.createElement('div');
            card.className = 'group-card';
            card.innerHTML = `
                <div class="group-header">
                    <h3><i class="fas fa-users"></i> ${groupName}</h3>
                    <span class="count-badge">${students.length} presenças</span>
                </div>
                <table class="presence-table">
                    <thead>
                        <tr>
                            <th>Aluno</th>
                            <th>Data e Hora</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${students.map(s => `
                            <tr>
                                <td><strong>${s.aluno}</strong></td>
                                <td>${s.data}</td>
                                <td><span class="status-badge">${s.status.toUpperCase()}</span></td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
            container.appendChild(card);
        }
    } catch (error) {
        container.innerHTML = '<p class="error">Erro de conexão com o servidor.</p>';
    }
}