const form = document.getElementById("login-form");
const mensagemElemento = document.getElementById("mensagem");

function limparMensagem() {
  mensagemElemento.textContent = "";
  mensagemElemento.className = "mensagem";
}

function mostrarErro(texto) {
  mensagemElemento.textContent = texto;
  mensagemElemento.className = "mensagem erro";
}

form.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  limparMensagem();

  const dados = {
    email: form.email.value.trim(),
    senha: form.senha.value.trim(),
  };

  if (!dados.email || !dados.senha) {
    mostrarErro("Informe e-mail e senha.");
    return;
  }

  try {
    const resposta = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dados),
    });

    const corpo = await resposta.json().catch(() => ({}));
    if (!resposta.ok) {
      mostrarErro(corpo.erro || `Erro ${resposta.status}`);
      return;
    }

    window.location.href = "/";
  } catch (erro) {
    mostrarErro("Falha ao entrar, tente novamente.");
  }
});
