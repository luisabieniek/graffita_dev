from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text, Boolean, Numeric, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum

# ==========================================
# ENUMS PARA PADRONIZAÇÃO DE STATUS REAL
# ==========================================
class StatusPedido(str, enum.Enum):
    AGUARDANDO_PAGAMENTO = "aguardando_pagamento"
    PAGO = "pago"
    EM_PREPARACAO = "em_preparacao"
    ENVIADO = "enviado"
    ENTREGUE = "entregue"
    CANCELADO = "cancelado"

class StatusPagamento(str, enum.Enum):
    PENDENTE = "pendente"
    APROVADO = "aprovado"
    RECUSADO = "recusado"
    ESTORNADO = "estornado"

class TipoPagamento(str, enum.Enum):
    PIX = "pix"
    CARTAO_CREDITO = "cartao_credito"
    BOLETO = "boleto"

class StatusEntrega(str, enum.Enum):
    EM_PREPARACAO = "em_preparacao"
    POSTADO = "postado"
    EM_TRANSITO = "em_transito"
    SAIU_PARA_ENTREGA = "saiu_para_entrega"
    ENTREGUE = "entregue"
    FALHA_NA_ENTREGA = "falha_na_entrega"


# ==========================================
# TABELAS DE ASSOCIAÇÃO (MUITOS PARA MUITOS)
# ==========================================
item_tags = Table(
    "item_tags",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), nullable=False),
    Column("inspiracao_id", Integer, ForeignKey("inspiracoes.id", ondelete="CASCADE"), nullable=True),
    Column("produto_id", Integer, ForeignKey("produtos.id", ondelete="CASCADE"), nullable=True),
)

# ==========================================
# MODELOS DE ENTIDADES
# ==========================================

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    senha = Column(String(255), nullable=False)
    cpf = Column(String(14), unique=True, index=True, nullable=False)
    biografia = Column(Text, nullable=True)
    foto_perfil = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True, nullable=False)
    
    produtos = relationship("Produto", back_populates="usuario", cascade="all, delete-orphan")
    enderecos = relationship("Endereco", back_populates="usuario", cascade="all, delete-orphan")
    favoritos = relationship("Favorito", back_populates="usuario", cascade="all, delete-orphan")
    itens_carrinho = relationship("Carrinho", back_populates="usuario", cascade="all, delete-orphan")
    inspiracoes = relationship("Inspiracao", back_populates="usuario", cascade="all, delete-orphan")
    pedidos = relationship("Pedido", back_populates="comprador")
    
    mensagens_enviadas = relationship("MensagemChat", foreign_keys="MensagemChat.remetente_id", back_populates="remetente", cascade="all, delete-orphan")
    mensagens_recebidas = relationship("MensagemChat", foreign_keys="MensagemChat.destinatario_id", back_populates="destinatario", cascade="all, delete-orphan")
    avaliacoes_feitas = relationship("AvaliacaoProduto", back_populates="usuario", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "cpf": self.cpf,
            "biografia": self.biografia,
            "foto_perfil": self.foto_perfil,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), unique=True, index=True, nullable=False)
    
    def to_dict(self):
        return {"id": self.id, "nome": self.nome}

class Inspiracao(Base):
    __tablename__ = "inspiracoes"
    
    id = Column(Integer, primary_key=True)
    titulo = Column(String(120), nullable=False)
    descricao = Column(Text, nullable=False)
    imagem = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)

    usuario = relationship("Usuario", back_populates="inspiracoes")
    produto = relationship("Produto", back_populates="inspiracao", uselist=False)
    tags = relationship("Tag", secondary=item_tags)
    
    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "imagem": self.imagem,
            "usuario_id": self.usuario_id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True)
    nomeProduto = Column(String(120), nullable=False, index=True)
    preco = Column(Numeric(10, 2), nullable=False)
    descricao = Column(Text, nullable=True)
    estoque = Column(Integer, default=1, nullable=False)
    imagem = Column(String(255), nullable=True)
    disponivel = Column(Boolean, default=True, index=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    inspiracao_id = Column(Integer, ForeignKey("inspiracoes.id", ondelete="SET NULL"), nullable=True)

    usuario = relationship("Usuario", back_populates="produtos")
    inspiracao = relationship("Inspiracao", back_populates="produto")
    favoritos = relationship("Favorito", back_populates="produto", cascade="all, delete-orphan")
    carrinhos = relationship("Carrinho", back_populates="produto", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary=item_tags)
    avaliacoes = relationship("AvaliacaoProduto", back_populates="produto", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "nomeProduto": self.nomeProduto,
            "preco": float(self.preco),
            "descricao": self.descricao,
            "estoque": self.estoque,
            "imagem": self.imagem,
            "disponivel": self.disponivel,
            "usuario_id": self.usuario_id,
            "inspiracao_id": self.inspiracao_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

class Carrinho(Base):
    __tablename__ = "carrinhos"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id", ondelete="CASCADE"), nullable=False)
    quantidade = Column(Integer, default=1, nullable=False)

    usuario = relationship("Usuario", back_populates="itens_carrinho")
    produto = relationship("Produto", back_populates="carrinhos")

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "produto_id": self.produto_id,
            "quantidade": self.quantidade
        }

class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True)
    comprador_id = Column(Integer, ForeignKey("usuarios.id", ondelete="RESTRICT"), nullable=False, index=True)
    total = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum(StatusPedido), default=StatusPedido.AGUARDANDO_PAGAMENTO, nullable=False, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    
    comprador = relationship("Usuario", back_populates="pedidos")
    
    def to_dict(self):
        return {
            "id": self.id,
            "comprador_id": self.comprador_id,
            "total": float(self.total),
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }

class MensagemChat(Base):
    __tablename__ = "mensagens_chat"
    id = Column(Integer, primary_key=True)
    remetente_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    destinatario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    conteudo = Column(Text, nullable=False)
    lida = Column(Boolean, default=False, index=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    remetente = relationship("Usuario", foreign_keys=[remetente_id], back_populates="mensagens_enviadas")
    destinatario = relationship("Usuario", foreign_keys=[destinatario_id], back_populates="mensagens_recebidas")

    def to_dict(self):
        return {
            "id": self.id,
            "remetente_id": self.remetente_id,
            "destinatario_id": self.destinatario_id,
            "conteudo": self.conteudo,
            "lida": self.lida,
            "created_at": self.created_at.isoformat()
        }

class AvaliacaoProduto(Base):
    __tablename__ = "avaliacoes_produtos"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id", ondelete="CASCADE"), nullable=False)
    nota = Column(Integer, nullable=False)
    comentario = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    usuario = relationship("Usuario", back_populates="avaliacoes_feitas")
    produto = relationship("Produto", back_populates="avaliacoes")

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "produto_id": self.produto_id,
            "nota": self.nota,
            "comentario": self.comentario,
            "created_at": self.created_at.isoformat()
        }

class Endereco(Base):
    __tablename__ = "enderecos"
    id = Column(Integer, primary_key=True)
    cep = Column(String(8), nullable=False)
    rua = Column(String(120), nullable=False)
    numero = Column(Integer, nullable=False)
    bairro = Column(String(120), nullable=False)
    cidade = Column(String(120), nullable=False)
    estado = Column(String(120), nullable=False)
    complemento = Column(String(120), nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)

    usuario = relationship("Usuario", back_populates="enderecos")

    def to_dict(self):
        return {
            "id": self.id,
            "cep": self.cep,
            "rua": self.rua,
            "numero": self.numero,
            "bairro": self.bairro,
            "cidade": self.cidade,
            "estado": self.estado,
            "complemento": self.complemento,
            "usuario_id": self.usuario_id,
        }

class Favorito(Base):
    __tablename__ = "favoritos"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id", ondelete="CASCADE"), nullable=False)

    usuario = relationship("Usuario", back_populates="favoritos")
    produto = relationship("Produto", back_populates="favoritos")

    def to_dict(self):
        return {"id": self.id, "usuario_id": self.usuario_id, "produto_id": self.produto_id}