document.querySelectorAll(".alternar-senha").forEach((botao) => {
  botao.addEventListener("click", () => {
    const alvo = document.getElementById(botao.getAttribute("data-alvo"));
    const visivel = alvo.type === "text";
    alvo.type = visivel ? "password" : "text";
    botao.textContent = visivel ? "👁️" : "🙈";
    botao.setAttribute("aria-label", visivel ? "Mostrar senha" : "Ocultar senha");
  });
});

function mostrarMensagem(elemento, texto, tipo) {
  elemento.textContent = texto;
  elemento.classList.remove("sucesso", "erro");
  elemento.classList.add("mostrar", tipo);
}

document.getElementById("form-cadastro").addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const mensagem = document.getElementById("mensagem");

  const nome = document.getElementById("nome").value.trim();
  const email = document.getElementById("email").value.trim();
  const senha = document.getElementById("senha").value;
  const confirmarSenha = document.getElementById("confirmar-senha").value;

  if (senha !== confirmarSenha) {
    mostrarMensagem(mensagem, "As senhas não são iguais.", "erro");
    return;
  }

  try {
    const resposta = await fetch("/api/usuarios", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nome, email, senha }),
    });
    const dados = await resposta.json();
    if (!resposta.ok) throw new Error(dados.erro || "Não foi possível criar a conta.");

    localStorage.setItem("usuario", JSON.stringify(dados));
    mostrarMensagem(mensagem, "Conta criada! Te levando pro mural...", "sucesso");
    setTimeout(() => (window.location.href = "/"), 700);
  } catch (erro) {
    mostrarMensagem(mensagem, erro.message, "erro");
  }
});