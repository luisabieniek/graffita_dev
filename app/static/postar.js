function mostrarMensagem(elemento, texto, tipo) {
  elemento.textContent = texto;
  elemento.classList.remove("sucesso", "erro");
  elemento.classList.add("mostrar", tipo);
}

document.getElementById("form-postar").addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const mensagem = document.getElementById("mensagem");

  const nomeProduto = document.getElementById("nomeProduto").value.trim();
  const preco = document.getElementById("preco").value;
  const imagem = document.getElementById("imagem").value.trim();
  const descricao = document.getElementById("descricao").value.trim();

  try {
    const resposta = await fetch("/api/produtos", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nomeProduto, preco, imagem, descricao, disponivel: true }),
    });
    const dados = await resposta.json();
    if (!resposta.ok) throw new Error(dados.erro || "Não foi possível postar.");

    mostrarMensagem(mensagem, "Postado! Te levando pro mural...", "sucesso");
    setTimeout(() => (window.location.href = "/"), 700);
  } catch (erro) {
    mostrarMensagem(mensagem, erro.message, "erro");
  }
});