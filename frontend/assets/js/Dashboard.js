document.addEventListener('DOMContentLoaded', () => {
    // Verificar se o usuário está logado
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = 'login.html';
        return;
    }

    // Carregar dados reais do backend Python
    loadStats();

    // Botão Sair
    document.getElementById('logoutBtn').addEventListener('click', (e) => {
        e.preventDefault();
        localStorage.removeItem('access_token');
        window.location.href = 'login.html';
    });
});

async function loadStats() {
    try {
        // Exemplo de chamada para o seu backend FastAPI/Flask
        // const response = await fetch('http://localhost:8000/stats', {
        //     headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        // });
        // const data = await response.json();

        // Mock para visualização inicial
        const mockData = {
            totalAlunos: 128,
            totalPresencas: 2540
        };

        animateValue("totalAlunos", 0, mockData.totalAlunos, 1000);
        animateValue("totalPresencas", 0, mockData.totalPresencas, 1000);

    } catch (error) {
        console.error('Erro ao buscar estatísticas:', error);
    }
}

// Função para efeito visual nos números
function animateValue(id, start, end, duration) {
    const obj = document.getElementById(id);
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        obj.innerHTML = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}