document.addEventListener('DOMContentLoaded', () => {
    const presenceForm = document.getElementById('presenceForm');
    const presenceCodeInput = document.getElementById('presenceCode');
    const errorMsg = document.getElementById('error-code');
    const openScannerBtn = document.getElementById('openScannerBtn');
    const closeScannerBtn = document.getElementById('closeScannerBtn');
    const scannerSection = document.getElementById('scannerSection');
    
    // Feedback
    const feedbackContainer = document.getElementById('feedbackContainer');
    const successToast = document.getElementById('successToast');
    const errorToast = document.getElementById('errorToast');

    // 1. Simulação do Validador no Backend Python
    const codigosValidos = ["ALFA10", "BETA20", "GAMA30"];

    // 2. Lógica de Envio (Submissão do Formulário)
    presenceForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Reset de erros
        presenceCodeInput.classList.remove('invalid');
        hideFeedback();

        const inputVal = presenceCodeInput.value.trim().toUpperCase();

        // Validação básica (vazio)
        if (!inputVal) {
            presenceCodeInput.classList.add('invalid');
            errorMsg.style.display = 'block';
            return;
        }

        // Validação Simulada com Backend
        simulatePythonCheck(inputVal);
    });

    function simulatePythonCheck(code) {
        // Mostra spinner no botão
        const confirmBtn = document.getElementById('confirmBtn');
        const originalText = confirmBtn.innerText;
        confirmBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Verificando...';
        confirmBtn.disabled = true;

        // Simulando delay de rede (conexão com o Python)
        setTimeout(() => {
            confirmBtn.innerText = originalText;
            confirmBtn.disabled = false;

            if (codigosValidos.includes(code)) {
                showFeedback('success');
                // Redireciona para a Área do Aluno após 2s
                setTimeout(() => { window.location.href = 'area_aluno.html'; }, 2000);
            } else {
                showFeedback('error');
            }
        }, 1200);
    }

    // 3. Lógica do Scanner de QR Code
    openScannerBtn.addEventListener('click', () => {
        scannerSection.style.display = 'flex';
        // Aqui você inicializaria a biblioteca de câmera
        console.log("Inicializando a câmera...");
        // Ex: const html5QrcodeScanner = new Html5QrcodeScanner("reader", { fps: 10, qrbox: 250 });
        // html5QrcodeScanner.render(onScanSuccess);
    });

    closeScannerBtn.addEventListener('click', () => {
        scannerSection.style.display = 'none';
        console.log("Desligando a câmera.");
    });

    // 4. Funções de Feedback Visível
    function showFeedback(type) {
        feedbackContainer.style.display = 'block';
        if (type === 'success') {
            successToast.style.display = 'flex';
            errorToast.style.display = 'none';
        } else {
            successToast.style.display = 'none';
            errorToast.style.display = 'flex';
            // Oculta o erro automaticamente após 3s
            setTimeout(hideFeedback, 3000);
        }
    }

    function hideFeedback() {
        feedbackContainer.style.display = 'none';
    }

    // Exemplo de sucesso no escaneamento (para integração futura)
    function onScanSuccess(decodedText, decodedResult) {
        console.log(`Código escaneado: ${decodedText}`);
        scannerSection.style.display = 'none';
        presenceCodeInput.value = decodedText;
        simulatePythonCheck(decodedText); // Envia automaticamente
    }
});