from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, nullable=True)
    senha = Column(String(120), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    
    enderecos = relationship("Endereco", back_populates="usuario")
    favoritos = relationship("Favorito", back_populates="usuario")
    carrinhos = relationship("Carrinho", back_populates="usuario")
    mensagens = relationship("Mensagem", back_populates="usuario")
    
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha,
            "cpf": self.cpf,
        }
        
    def __repr__(self):
        return f"<Usuario {self.id} {self.nome} {self.email}>"

class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True)
    nomeProduto = Column(String(120), nullable=False)
    preco = Column(Float(precision=2), nullable=False)
    descricao = Column(String(120), nullable=True)
    imagem = Column(String(120), nullable=True)
    disponivel = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)

    favoritos = relationship("Favorito", back_populates="produto")
    carrinhos = relationship("Carrinho", back_populates="produto")

    def to_dict(self):
        return {
            "id": self.id,
            "nomeProduto": self.nomeProduto,
            "preco": self.preco,
            "descricao": self.descricao,
            "imagem": self.imagem,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<Produto {self.id} {self.nomeProduto!r}>"
    
    
class Favorito(Base):
    __tablename__ = "favoritos"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)

    usuario = relationship("Usuario", back_populates="favoritos")
    produto = relationship("Produto", back_populates="favoritos")

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "produto_id": self.produto_id,
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
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

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

    def __repr__(self):
        return f"<Endereco {self.id} {self.cep!r}>"
    
class Carrinho(Base):
    __tablename__ = "carrinhos"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)

    usuario = relationship("Usuario", back_populates="carrinhos")
    produto = relationship("Produto", back_populates="carrinhos")

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "produto_id": self.produto_id,
        }
        
    def __repr__(self):
        return f"<Carrinho {self.id} {self.produto_id!r}>"
    
    
class Mensagem(Base):
    __tablename__ = "mensagens"
    id = Column(Integer, primary_key=True)
    descricao = Column(String(120), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    usuario = relationship("Usuario", back_populates="mensagens")
    
    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "usuario_id": self.usuario_id,
        }
    
    def __repr__(self):
        return f"<Mensagem {self.id} {self.descricao!r}>"