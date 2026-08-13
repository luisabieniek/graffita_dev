const mosaico = document.getElementById("mosaico");
const vazio = document.getElementById("vazio");
const campoBusca = document.getElementById("campo-busca");
const toast = document.getElementById("toast");
const bolhaCarrinho = document.getElementById("bolha-carrinho");
const linkConta = document.getElementById("link-conta");

let produtos = [];

function usuarioLogado() {
  try {
    return JSON.parse(localStorage.getItem("usuario"));
  } catch {
    return null;
  }
}

function carrinho() {
  try {
    return JSON.parse(localStorage.getItem("carrinho")) || [];
  } catch {
    return [];
  }
}

function salvarCarrinho(lista) {
  localStorage.setItem("carrinho", JSON.stringify(lista));
  atualizarBolhaCarrinho();
}

function atualizarBolhaCarrinho() {
  const total = carrinho().length;
  if (total > 0) {
    bolhaCarrinho.style.display = "flex";
    bolhaCarrinho.textContent = total;
  } else {
    bolhaCarrinho.style.display = "none";
  }
}

function mostrarToast(texto) {
  toast.textContent = texto;
  toast.classList.add("mostrar");
  setTimeout(() => toast.classList.remove("mostrar"), 2200);
}

function ajustarBarraConta() {
  const usuario = usuarioLogado();
  if (usuario) {
    linkConta.textContent = usuario.nome.split(" ")[0];
    linkConta.href = "/postar";
  }
}

async function buscarProdutos() {
  const resposta = await fetch("/api/produtos");
  if (!resposta.ok) throw new Error(`HTTP ${resposta.status}`);
  return resposta.json();
}

function criarPin(produto) {
  const article = document.createElement("article");
  article.className = "pin";

  const imagem = produto.imagem || `https://placehold.co/400x520/AED9E0/23262e?text=${encodeURIComponent(produto.nomeProduto)}`;

  article.innerHTML = `
    ${produto.disponivel === false ? '<span class="fita">esgotado</span>' : ""}
    <img class="pin-imagem" src="${imagem}" alt="${produto.nomeProduto}" loading="lazy" />
    <div class="pin-corpo">
      <p class="pin-nome">${produto.nomeProduto}</p>
      ${produto.descricao ? `<p class="pin-desc">${produto.descricao}</p>` : ""}
      <div class="pin-rodape">
        <span class="preco">R$ ${Number(produto.preco).toFixed(2)}</span>
        <div class="pin-acoes">
          <button class="icone-btn" title="Favoritar" data-favoritar="${produto.id}">♥</button>
          <button class="btn btn-coral" data-comprar="${produto.id}">comprar</button>
        </div>
      </div>
    </div>
  `;
  return article;
}

function renderizar(lista) {
  mosaico.innerHTML = "";
  if (lista.length === 0) {
    vazio.style.display = "block";
    return;
  }
  vazio.style.display = "none";
  for (const produto of lista) {
    mosaico.appendChild(criarPin(produto));
  }
}

async function comprar(produtoId) {
  const usuario = usuarioLogado();
  if (!usuario) {
    mostrarToast("Entre na sua conta para comprar 🔒");
    setTimeout(() => (window.location.href = "/login"), 900);
    return;
  }

  try {
    const resposta = await fetch("/api/carrinho", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ usuario_id: usuario.id, produto_id: produtoId }),
    });
    const dados = await resposta.json();
    if (!resposta.ok) throw new Error(dados.erro || "Não foi possível comprar.");

    const lista = carrinho();
    lista.push(dados);
    salvarCarrinho(lista);
    mostrarToast("Adicionado ao carrinho ✓");
  } catch (erro) {
    mostrarToast(erro.message);
  }
}

async function favoritar(produtoId) {
  const usuario = usuarioLogado();
  if (!usuario) {
    mostrarToast("Entre na sua conta para favoritar 🔒");
    return;
  }
  try {
    const resposta = await fetch("/api/favoritos", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ usuario_id: usuario.id, produto_id: produtoId }),
    });
    const dados = await resposta.json();
    if (!resposta.ok) throw new Error(dados.erro || "Não foi possível favoritar.");
    mostrarToast("Favoritado ♥");
  } catch (erro) {
    mostrarToast(erro.message);
  }
}

mosaico.addEventListener("click", (evento) => {
  const comprarId = evento.target.getAttribute("data-comprar");
  const favoritarId = evento.target.getAttribute("data-favoritar");
  if (comprarId) comprar(Number(comprarId));
  if (favoritarId) favoritar(Number(favoritarId));
});

campoBusca.addEventListener("input", () => {
  const termo = campoBusca.value.trim().toLowerCase();
  const filtrados = produtos.filter((p) => p.nomeProduto.toLowerCase().includes(termo));
  renderizar(filtrados);
});

document.getElementById("btn-carrinho").addEventListener("click", () => {
  const total = carrinho().length;
  mostrarToast(total > 0 ? `Você tem ${total} item(ns) no carrinho 🛒` : "Seu carrinho está vazio");
});

async function iniciar() {
  ajustarBarraConta();
  atualizarBolhaCarrinho();
  try {
    produtos = await buscarProdutos();
    renderizar(produtos);
  } catch (erro) {
    vazio.style.display = "block";
    vazio.querySelector("p").textContent = "Não foi possível carregar os produtos.";
  }
}