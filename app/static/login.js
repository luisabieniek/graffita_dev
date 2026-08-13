function ligarAlternarSenha() {
  document.querySelectorAll(".alternar-senha").forEach((botao) => {
    botao.addEventListener("click", () => {
      const alvo = document.getElementById(botao.getAttribute("data-alvo"));
      const visivel = alvo.type === "text";
      alvo.type = visivel ? "password" : "text";
      botao.textContent = visivel ? "👁️" : "🙈";
      botao.setAttribute("aria-label", visivel ? "Mostrar senha" : "Ocultar senha");
    });
  });
}

function mostrarMensagem(elemento, texto, tipo) {
  elemento.textContent = texto;
  elemento.classList.remove("sucesso", "erro");
  elemento.classList.add("mostrar", tipo);
}

// ------------------------------------------------------------------ login --

document.getElementById("form-login").addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const mensagem = document.getElementById("mensagem");
  const email = document.getElementById("email").value.trim();
  const senha = document.getElementById("senha").value;

  try {
    const resposta = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, senha }),
    });
    const dados = await resposta.json();
    if (!resposta.ok) throw new Error(dados.erro || "Não foi possível entrar.");

    localStorage.setItem("usuario", JSON.stringify(dados));
    mostrarMensagem(mensagem, "Login feito! Te levando pro mural...", "sucesso");
    setTimeout(() => (window.location.href = "/"), 700);
  } catch (erro) {
    mostrarMensagem(mensagem, erro.message, "erro");
  }
});

// ------------------------------------------------------- modal recuperar --

const sobreposicao = document.getElementById("sobreposicao");

document.getElementById("abrir-recuperar").addEventListener("click", () => {
  sobreposicao.classList.add("aberta");
});

document.getElementById("fechar-recuperar").addEventListener("click", () => {
  sobreposicao.classList.remove("aberta");
});

sobreposicao.addEventListener("click", (evento) => {
  if (evento.target === sobreposicao) sobreposicao.classList.remove("aberta");
});

document.getElementById("form-recuperar").addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const mensagem = document.getElementById("mensagem-recuperar");
  const email = document.getElementById("email-recuperar").value.trim();
  const novaSenha = document.getElementById("nova-senha").value;

  try {
    const resposta = await fetch("/api/recuperar-senha", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, nova_senha: novaSenha }),
    });
    const dados = await resposta.json();
    if (!resposta.ok) throw new Error(dados.erro || "Não foi possível redefinir a senha.");

    mostrarMensagem(mensagem, "Senha redefinida! Já pode entrar com ela.", "sucesso");
    setTimeout(() => sobreposicao.classList.remove("aberta"), 1200);
  } catch (erro) {
    mostrarMensagem(mensagem, erro.message, "erro");
  }
});

ligarAlternarSenha();