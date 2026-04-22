// ===== CONSTANTES GLOBAIS =====
const API_BASE_URL = "http://localhost:8000";

const video = document.getElementById("video");
const message = document.getElementById("message");
const popup1 = document.getElementById("popup1");
const popup2 = document.getElementById("popup2");
const backButton = document.getElementById("backButton");
const btnVerificarRosto = document.getElementById("btnVerificarRosto");

// Variáveis de Estado
let modo = null;
let nomeAluno = null;
let streamAtivo = null;

// ===== FUNÇÕES DE SUPORTE =====

function mostrarAlerta(mensagem, tipo = 'info') {
    let containerAlertas = document.getElementById('container-alertas') || (() => {
        const div = document.createElement('div');
        div.id = 'container-alertas';
        document.body.appendChild(div);
        return div;
    })();

    const cores = { sucesso: 'alerta-sucesso', erro: 'alerta-erro', aviso: 'alerta-aviso', info: 'alerta-info' };
    const alerta = document.createElement('div');
    alerta.className = `alerta ${cores[tipo] || cores.info}`;
    alerta.innerHTML = mensagem;
    containerAlertas.appendChild(alerta);

    setTimeout(() => {
        alerta.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => alerta.remove(), 300);
    }, 4000);
}

function pararCamera() {
    if (streamAtivo) {
        streamAtivo.getTracks().forEach(track => track.stop());
        streamAtivo = null;
    }
}

async function startCamera() {
    try {
        const facingMode = (modo === 'cadastro') ? 'user' : 'environment';
        message.textContent = "Abrindo câmera...";

        streamAtivo = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: { ideal: facingMode }, width: 1280, height: 720 },
            audio: false
        });

        video.srcObject = streamAtivo;
        video.onloadedmetadata = () => {
            video.classList.add("loaded");
            btnVerificarRosto.style.display = "block";
            video.style.transform = (facingMode === 'user') ? "scaleX(-1)" : "none";
            message.textContent = `Posicione o rosto para ${modo}`;
        };
    } catch (error) {
        console.error("Erro na câmera:", error);
        message.textContent = "Erro ao iniciar a câmera.";
    }
}

// ===== LÓGICA DE CAPTURA E API =====

btnVerificarRosto.addEventListener("click", () => {
    if (!streamAtivo) return;

    message.textContent = "Analisando...";
    btnVerificarRosto.disabled = true;

    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');

    if (video.style.transform === "scaleX(-1)") {
        ctx.translate(canvas.width, 0);
        ctx.scale(-1, 1);
    }
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(async (blob) => {
        await confirmarPresencaAPI(blob);
    }, 'image/jpeg', 0.8);
});

async function confirmarPresencaAPI(blob) {
    try {
        const urlParams = new URLSearchParams(window.location.search);
        const formData = new FormData();
        const groupId = urlParams.get('group_id');
        formData.append('image', blob, 'face.jpg');
        formData.append('group_id', groupId);

        const token = localStorage.getItem('access_token');

        // Note: Aqui usamos a rota /presence que você definiu no Python
        const response = await fetch(`${API_BASE_URL}/presence`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` },
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            mostrarAlerta(`✅ ${data.msg}`, "sucesso");
            pararCamera();
            //setTimeout(() => { window.location.href = "Dashboard.html"; }, 2500);
        } else {
            throw new Error(data.detail || data.msg || "Erro no reconhecimento.");
        }
    } catch (error) {
        mostrarAlerta(error.message, "erro");
        btnVerificarRosto.disabled = false;
        message.textContent = "Tente novamente.";
    }
}

// ===== INICIALIZAÇÃO E EVENTOS =====

window.showPopup2 = () => {
    popup1.classList.add("hidden");
    popup2.classList.remove("hidden");
};

window.startVerification = () => {
    popup2.classList.add("hidden");
    startCamera();
};

backButton.addEventListener("click", () => {
    pararCamera();
    window.history.back();
});

document.addEventListener("DOMContentLoaded", () => {
    const urlParams = new URLSearchParams(window.location.search);
    nomeAluno = urlParams.get('aluno'); // Nome vindo da tela anterior

    if (urlParams.get('modo') === 'cadastro') {
        modo = 'cadastro';
        popup1.classList.add("hidden");
        popup2.classList.remove("hidden");
    } else {
        modo = 'verificar';
        popup1.classList.remove("hidden");
    }
});