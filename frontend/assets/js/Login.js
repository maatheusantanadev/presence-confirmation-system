document.addEventListener('DOMContentLoaded', () => {

  const form = document.getElementById('loginForm');
  const submitBtn = document.getElementById('submitBtn');
  const message = document.getElementById('message');

  function showMessage(text, type) {
    message.textContent = text;
    message.className = `message ${type}`;
  }

  function setLoading(isLoading) {
    submitBtn.disabled = isLoading;
    submitBtn.textContent = isLoading ? 'Entrando...' : 'Entrar';
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;

    if (!username || !password) {
      showMessage('Preencha todos os campos.', 'error');
      return;
    }

    showMessage('', '');
    setLoading(true);

    try {
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);

      const response = await fetch('http://localhost:8000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem('access_token', data.access_token);

        showMessage('Login realizado com sucesso!', 'success');

        // limpa senha
        document.getElementById('password').value = '';

        // redireciona (opcional)
        setTimeout(() => {
          window.location.href = 'dashboard.html';
        }, 1000);

      } else {
        showMessage(data.detail || 'Erro no login', 'error');
      }

    } catch (error) {
      showMessage('Erro ao conectar com o servidor.', 'error');
    } finally {
      setLoading(false);
    }
  });

});