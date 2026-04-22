document.addEventListener('DOMContentLoaded', () => {
    // Verificar se o usuário está logado
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = 'login.html';
        return;
    }

    // Carregar dados reais do backend Python
    loadStats();
    generateAttendanceQRCode();

    // Botão Sair
    document.getElementById('logoutBtn').addEventListener('click', (e) => {
        e.preventDefault();
        localStorage.removeItem('access_token');
        window.location.href = 'login.html';
    });
});

async function loadStats() {
    try {
        const token = localStorage.getItem('access_token');

        // Chamada real para o backend
        const response = await fetch('http://localhost:8000/stats', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            if(response.status === 401) window.location.href = 'login.html';
            throw new Error("Falha ao carregar estatísticas");
        }

        const data = await response.json();

        // Mapeando os dados do banco para os IDs do seu HTML
        // Supondo que no HTML os IDs sejam 'totalTurmas' e 'totalPresencas'
        animateValue("totalAlunos", 0, data.total_groups, 1000); // Aqui vira o total de turmas
        animateValue("totalPresencas", 0, data.total_presences, 1000);

    } catch (error) {
        console.error('Erro ao buscar estatísticas:', error);
        // Fallback em caso de erro para não deixar o card vazio
        document.getElementById('totalAlunos').innerText = "0";
        document.getElementById('totalPresencas').innerText = "0";
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

// Adicione isso dentro do seu DOMContentLoaded ou como uma função separada
function generateAttendanceQRCode() {
    const qrContainer = document.getElementById("qrcode");
    qrContainer.innerHTML = ""; // Limpa antes de gerar

    // Defina a URL da sua tela de registro (ex: registrar_presenca.html)
    // Se estiver em rede local, use o IP do seu Mac, ex: http://192.168.1.5:5500/presenca_aluno.html
    const registrationUrl = `${window.location.origin}/presenca_aluno.html`;

    new QRCode(qrContainer, {
        text: registrationUrl,
        width: 200,
        height: 200,
        colorDark: "#2563eb", // Azul do seu sistema
        colorLight: "#ffffff",
        correctLevel: QRCode.CorrectLevel.H
    });
}

