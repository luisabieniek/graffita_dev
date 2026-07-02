const form = document.getElementById("cadastro-form");
const mensagemElemento = document.getElementById("mensagem");

function limparMensagem() {
  mensagemElemento.textContent = "";
  mensagemElemento.className = "mensagem";
}

function mostrarErro(texto) {
  mensagemElemento.textContent = texto;
  mensagemElemento.className = "mensagem erro";
}

function mostrarSucesso(texto) {
  mensagemElemento.textContent = texto;
  mensagemElemento.className = "mensagem sucesso";
}

form.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  limparMensagem();

  const dados = {
    nome: form.nome.value.trim(),
    email: form.email.value.trim(),
    senha: form.senha.value.trim(),
    cpf: form.cpf.value.trim(),
  };

  if (!dados.nome || !dados.senha || !dados.cpf) {
    mostrarErro("Preencha todos os campos obrigatórios.");
    return;
  }

  try {
    const resposta = await fetch("/api/usuarios", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dados),
    });

    const corpo = await resposta.json().catch(() => ({}));
    if (!resposta.ok) {
      mostrarErro(corpo.erro || `Erro ${resposta.status}`);
      return;
    }

    mostrarSucesso("Usuário cadastrado com sucesso!");
    form.reset();
  } catch (erro) {
    mostrarErro("Falha ao enviar cadastro, tente novamente.");
  }
});
