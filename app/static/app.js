const COLUNAS = {
  usuarios: [
    { chave: "id", titulo: "ID" },
    { chave: "nome", titulo: "Nome" },
    { chave: "email", titulo: "E-mail" },
    { chave: "cpf", titulo: "CPF" },
  ],
  produtos: [
    { chave: "id", titulo: "ID" },
    { chave: "nomeProduto", titulo: "Produto" },
    { chave: "preco", titulo: "Preço" },
    { chave: "estoque", titulo: "Estoque" },
    { chave: "disponivel", titulo: "Disp." },
    { chave: "imagem", titulo: "Foto" },
  ],
  pedidos: [
    { chave: "id", titulo: "ID" },
    { chave: "total", titulo: "Total" },
    { chave: "status", titulo: "Status" },
    { chave: "created_at", titulo: "Data" },
  ],
  enderecos: [
    { chave: "id", titulo: "ID" },
    { chave: "rua", titulo: "Rua" },
    { chave: "numero", titulo: "Nº" },
    { chave: "cidade", titulo: "Cidade" },
    { chave: "usuario_id", titulo: "Usuário" },
  ],
  favoritos: [
    { chave: "id", titulo: "ID" },
    { chave: "usuario_id", titulo: "ID Usuário" },
    { chave: "produto_id", titulo: "ID Produto" },
  ],
  carrinhos: [
    { chave: "id", titulo: "ID" },
    { chave: "usuario_id", titulo: "ID Usuário" },
    { chave: "produto_id", titulo: "ID Produto" },
  ],
  inspiracoes: [
    { chave: "id", titulo: "ID" },
    { chave: "titulo", titulo: "Título" },
    { chave: "descricao", titulo: "Descrição" },
    { chave: "usuario_id", titulo: "ID Usuário" },
    { chave: "imagem", titulo: "Foto" },
  ],
};

const TITULOS = {
  usuarios: { lista: "Usuários", form: "Novo usuário" },
  produtos: { lista: "Produtos", form: "Novo Produto" },
  pedidos: { lista: "Pedidos", form: "Ver Pedidos" },
  enderecos: { lista: "Endereços", form: "Novo Endereço" },
  favoritos: { lista: "Favoritos", form: "Adicionar Favorito" },
  carrinhos: { lista: "Carrinho", form: "Adicionar ao Carrinho" },
  inspiracoes: { lista: "Inspirações", form: "Nova Inspiração" },
};

const CAMPOS = {
  usuarios: [
    { nome: "nome", rotulo: "Nome", obrigatorio: true },
    { nome: "email", rotulo: "E-mail", tipo: "email" },
    { nome: "senha", rotulo: "Senha", tipo: "password", obrigatorio: true },
    { nome: "cpf", rotulo: "CPF", obrigatorio: true },
  ],
  produtos: [
    { nome: "nomeProduto", rotulo: "Nome do Produto", obrigatorio: true },
    { nome: "preco", rotulo: "Preço", tipo: "number", obrigatorio: true },
    { nome: "descricao", rotulo: "Descrição" },
    { nome: "usuario_id", rotulo: "Vendedor", tipo: "select", origem: "usuarios", obrigatorio: true },
    { nome: "imagem", rotulo: "Foto do Produto", tipo: "file" },
  ],
  enderecos: [
    { nome: "cep", rotulo: "CEP", obrigatorio: true },
    { nome: "rua", rotulo: "Rua", obrigatorio: true },
    { nome: "numero", rotulo: "Número", tipo: "number", obrigatorio: true },
    { nome: "bairro", rotulo: "Bairro", obrigatorio: true },
    { nome: "cidade", rotulo: "Cidade", obrigatorio: true },
    { nome: "estado", rotulo: "Estado", obrigatorio: true },
    { nome: "usuario_id", rotulo: "Usuário", tipo: "select", origem: "usuarios", obrigatorio: true },
  ],
  favoritos: [
    { nome: "usuario_id", rotulo: "Usuário", tipo: "select", origem: "usuarios", obrigatorio: true },
    { nome: "produto_id", rotulo: "Produto", tipo: "select", origem: "produtos", obrigatorio: true },
  ],
  carrinhos: [
    { nome: "usuario_id", rotulo: "Usuário", tipo: "select", origem: "usuarios", obrigatorio: true },
    { nome: "produto_id", rotulo: "Produto", tipo: "select", origem: "produtos", obrigatorio: true },
  ],
  pedidos: [], // Geralmente criado via Checkout, não formulário direto aqui
  inspiracoes: [
    { nome: "titulo", rotulo: "Título", obrigatorio: true },
    { nome: "descricao", rotulo: "Descrição", obrigatorio: true },
    { nome: "usuario_id", rotulo: "Usuário", tipo: "select", origem: "usuarios", obrigatorio: true },
    { nome: "imagem", rotulo: "Foto da Inspiração", tipo: "file" },
  ],
};

const elementoStatus = document.getElementById("status");
const elementoTituloLista = document.getElementById("titulo-lista");
const elementoTituloFormulario = document.getElementById("titulo-formulario");
const elementoCabecalho = document.getElementById("cabecalho");
const elementoCorpo = document.getElementById("corpo");
const elementoCampos = document.getElementById("campos");
const formulario = document.getElementById("formulario");
const mensagemFormulario = document.getElementById("mensagem-formulario");
const botaoRecarregar = document.getElementById("botao-recarregar");
const abas = document.querySelectorAll(".aba");
const seletorUsuarioAtivo = document.getElementById("usuario-ativo");

let tipoAtual = "usuarios";
let usuarioLogadoId = null;

async function buscar(tipo) {
  const resposta = await fetch(`/api/${tipo}`);
  if (!resposta.ok) throw new Error(`HTTP ${resposta.status}`);
  return resposta.json();
}

async function carregar(tipo) {
  tipoAtual = tipo;
  elementoTituloLista.textContent = TITULOS[tipo].lista;
  elementoTituloFormulario.textContent = TITULOS[tipo].form;
  limparMensagem();

  await renderizarFormulario(tipo);
  renderizarCabecalho(tipo);
  elementoCorpo.innerHTML = "";

  elementoStatus.classList.remove("erro");
  elementoStatus.textContent = "Carregando...";

  try {
    let dados = await buscar(tipo);
    
    // Filtrar dados para mostrar apenas o que pertence ao usuário logado
    const tiposPessoais = ["carrinhos", "favoritos", "enderecos", "inspiracoes", "pedidos"];
    if (tiposPessoais.includes(tipo)) {
      if (!usuarioLogadoId) {
        dados = [];
        elementoStatus.textContent = "Selecione um usuário no topo para ver seus dados.";
      } else {
        dados = dados.filter(item => {
          // Pedidos usam comprador_id, os outros usam usuario_id
          const idDono = item.usuario_id || item.comprador_id;
          return String(idDono) === String(usuarioLogadoId);
        });
        elementoStatus.textContent = `${dados.length} registro(s) seu(s) carregado(s).`;
      }
    } else {
      elementoStatus.textContent = `${dados.length} registro(s) carregado(s).`;
    }

    renderizarLinhas(tipo, dados);
  } catch (erro) {
    elementoStatus.textContent = `Falha ao carregar: ${erro.message}`;
    elementoStatus.classList.add("erro");
  }
}

function renderizarCabecalho(tipo) {
  elementoCabecalho.innerHTML = "";
  for (const coluna of COLUNAS[tipo]) {
    const th = document.createElement("th");
    th.textContent = coluna.titulo;
    elementoCabecalho.appendChild(th);
  }
}

function renderizarLinhas(tipo, dados) {
  if (!dados.length) {
    const tr = document.createElement("tr");
    const td = document.createElement("td");
    td.colSpan = COLUNAS[tipo].length;
    td.className = "vazio";
    td.textContent = "Nenhum registro encontrado.";
    tr.appendChild(td);
    elementoCorpo.appendChild(tr);
    return;
  }

  for (const item of dados) {
    const tr = document.createElement("tr");
    for (const coluna of COLUNAS[tipo]) {
      const td = document.createElement("td");
      const valor = item[coluna.chave];
      if (coluna.chave === "imagem" && valor) {
        const img = document.createElement("img");
        img.src = valor;
        img.className = "img-tabela";
        td.appendChild(img);
      } else {
        td.textContent = valor === null || valor === undefined ? "—" : valor;
      }
      tr.appendChild(td);
    }
    elementoCorpo.appendChild(tr);
  }
}

async function renderizarFormulario(tipo) {
  elementoCampos.innerHTML = "";
  for (const campo of CAMPOS[tipo]) {
    const wrapper = document.createElement("div");
    wrapper.className = "campo";

    const label = document.createElement("label");
    label.htmlFor = `campo-${campo.nome}`;
    label.textContent = campo.rotulo + (campo.obrigatorio ? " *" : "");
    wrapper.appendChild(label);

    if (campo.tipo === "select") {
      const select = document.createElement("select");
      select.id = `campo-${campo.nome}`;
      select.name = campo.nome;
      if (campo.obrigatorio) select.required = true;

      const placeholder = document.createElement("option");
      placeholder.value = "";
      placeholder.textContent = "Selecione...";
      select.appendChild(placeholder);

      try {
        const itens = await buscar(campo.origem);
        for (const item of itens) {
          const option = document.createElement("option");
          option.value = item.id;
          option.textContent = rotuloItem(campo.origem, item);
          select.appendChild(option);
        }
        // Auto-selecionar se for o campo de usuário e tivermos alguém logado
        if (campo.nome === "usuario_id" && usuarioLogadoId) {
          select.value = usuarioLogadoId;
        }
      } catch (erro) {
        const option = document.createElement("option");
        option.disabled = true;
        option.textContent = `Erro ao carregar: ${erro.message}`;
        select.appendChild(option);
      }

      wrapper.appendChild(select);
    } else {
      const input = document.createElement("input");
      input.type = campo.tipo || "text";
      input.id = `campo-${campo.nome}`;
      input.name = campo.nome;
      if (campo.obrigatorio) input.required = true;
      wrapper.appendChild(input);
    }

    elementoCampos.appendChild(wrapper);
  }
}

function rotuloItem(origem, item) {
  if (origem === "usuarios") return `${item.nome} (id ${item.id})`;
  if (origem === "produtos") return `${item.nomeProduto} - R$ ${item.preco}`;
  return `${item.id}`;
}

function limparMensagem() {
  mensagemFormulario.textContent = "";
  mensagemFormulario.classList.remove("sucesso", "erro");
}

async function enviarFormulario(evento) {
  evento.preventDefault();
  limparMensagem();

  let corpoRequisicao;
  let cabecalhos = {};

  if (tipoAtual === "produtos" || tipoAtual === "inspiracoes") {
    corpoRequisicao = new FormData();
    for (const campo of CAMPOS[tipoAtual]) {
      const elemento = formulario.elements[campo.nome];
      if (campo.tipo === "file") {
        if (elemento.files[0]) corpoRequisicao.append(campo.nome, elemento.files[0]);
      } else {
        corpoRequisicao.append(campo.nome, elemento.value.trim());
      }
    }
  } else {
    const dados = {};
    for (const campo of CAMPOS[tipoAtual]) {
      const elemento = formulario.elements[campo.nome];
      const valor = elemento.value.trim();
      if (campo.obrigatorio && !valor) {
        mensagemFormulario.textContent = `Preencha ${campo.rotulo}.`;
        mensagemFormulario.classList.add("erro");
        elemento.focus();
        return;
      }
      if (valor !== "") dados[campo.nome] = valor;
    }
    corpoRequisicao = JSON.stringify(dados);
    cabecalhos["Content-Type"] = "application/json";
  }

  const botao = formulario.querySelector("button[type=submit]");
  botao.disabled = true;
  try {
    const resposta = await fetch(`/api/${tipoAtual}`, {
      method: "POST",
      headers: (tipoAtual === "produtos" || tipoAtual === "inspiracoes") ? {} : cabecalhos,
      body: corpoRequisicao,
    });

    const corpo = await resposta.json().catch(() => ({}));
    if (!resposta.ok) {
      throw new Error(corpo.erro || `HTTP ${resposta.status}`);
    }

    mensagemFormulario.textContent = "Cadastrado com sucesso.";
    mensagemFormulario.classList.add("sucesso");
    formulario.reset();
    
    // Se cadastrou um usuário, atualiza a lista de login
    if (tipoAtual === "usuarios") {
        usuarioLogadoId = corpo.id; // Login Automático
        await atualizarSeletorUsuarios();
        seletorUsuarioAtivo.value = usuarioLogadoId;
    }

    await carregar(tipoAtual);
  } catch (erro) {
    mensagemFormulario.textContent = erro.message;
    mensagemFormulario.classList.add("erro");
  } finally {
    botao.disabled = false;
  }
}

abas.forEach((aba) => {
  aba.addEventListener("click", () => {
    abas.forEach((a) => a.classList.remove("ativa"));
    aba.classList.add("ativa");
    carregar(aba.dataset.tipo);
  });
});

async function atualizarSeletorUsuarios() {
    const usuarios = await buscar("usuarios");
    const valorAntigo = seletorUsuarioAtivo.value;
    seletorUsuarioAtivo.innerHTML = '<option value="">Ninguém selecionado</option>';
    usuarios.forEach(u => {
        const opt = document.createElement("option");
        opt.value = u.id;
        opt.textContent = u.nome;
        seletorUsuarioAtivo.appendChild(opt);
    });
    seletorUsuarioAtivo.value = valorAntigo;
}

seletorUsuarioAtivo.addEventListener("change", (e) => {
    usuarioLogadoId = e.target.value;
    carregar(tipoAtual);
});

botaoRecarregar.addEventListener("click", () => carregar(tipoAtual));
formulario.addEventListener("submit", enviarFormulario);

// Inicialização
async function init() {
    await atualizarSeletorUsuarios();
    await carregar("usuarios");
}

init();
