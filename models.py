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
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=True)
    # endereco_id = Column(Integer, ForeignKey("enderecos.idEndereco"), nullable=False)
    # favorito_id = Column(Integer, ForeignKey("favoritos.idFavorito"), nullable=True)
    # carrinho_id = Column(Integer, ForeignKey("carrinhos.idCarrinho"), nullable=True)
    # created_at = Column(DateTime, default=datetime.now)
    
    # endereco = relationship("Endereco", back_populates="usuarios")
    # favorito = relationship("Favorito", back_populates="usuarios")
    # carrinho = relationship("Carrinho", back_populates="usuarios")
    produto = relationship("Produto", back_populates="usuario")
    turmas = relationship("Turma", back_populates="usuario")
    
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha,
            "cpf": self.cpf,
            "produto_id": self.produto_id,
            # "endereco_id": self.endereco_id,
            # "favorito_id": self.favorito_id,
            # "carrinho_id": self.carrinho_id,
            # "created_at": self.created_at
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
    # favoritos_id = Column(Integer, ForeignKey("favoritos.idFavorito"), nullable=True)

    usuario = relationship("Usuario", back_populates="produto")
    # favoritos = relationship("Favorito", back_populates="produtos")

    def to_dict(self):
        return {
            "id": self.id,
            "nomeProduto": self.nomeProduto,
            "preco": self.preco,
            "descricao": self.descricao,
            "imagem": self.imagem,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            # "favoritos_id": self.favoritos_id
        }

    def __repr__(self):
        return f"<Produto {self.id} {self.nomeProduto!r}>"
    
    
class Favoritos(Base):
    __tablenmae__ = "favoritos"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    
class Turma(Base):
    __tablename__ = "turmas"

    id = Column(Integer, primary_key=True)
    nome = Column(String(120), nullable=False)
    codigo = Column(String(40), unique=True, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    usuario = relationship("Usuario", back_populates="turmas")
    alunos = relationship("Aluno", back_populates="turma")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "codigo": self.codigo,
            "usuario_id": self.usuario_id,
        }

    def __repr__(self):
        return f"<Turma {self.id} {self.codigo!r}>"


class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True)
    nome = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, nullable=True)
    turma_id = Column(Integer, ForeignKey("turmas.id"), nullable=False)
    endereco = Column(String(120), nullable=False)


    turma = relationship("Turma", back_populates="alunos")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "turma_id": self.turma_id,
            "endereco": self.endereco
        }

    def __repr__(self):
        return f"<Aluno {self.id} {self.nome!r} {self.endereco!r}>"


class Funcionario(Base):
    __tablename__ = "funcionarios"
    id = Column(Integer, primary_key=True)
    nome = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, nullable=True)
    senha = Column(String(120), nullable=False)
    id_departamento = Column(Integer, ForeignKey("departamentos.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    departamento = relationship("Departamento", back_populates="funcionarios")


    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha,
            "id_departamento": self.id_departamento,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f"<Funcionario {self.id} {self.nome!r}>" 


class Departamento(Base):
    __tablename__ = "departamentos"
    id = Column(Integer, primary_key=True)
    nome = Column(String(120), nullable=False)

    funcionarios = relationship("Funcionario", back_populates="departamento")


    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
        }

    def __repr__(self):
        return f"<Departamento {self.id} {self.nome!r}>"



########

class Animal(Base):
    __tablename__ = "animais"

    id = Column(Integer, primary_key=True)
    nome = Column(String(120), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    id_tipo_animal = Column(Integer, ForeignKey("tipo_animal.id"), nullable=False)

    tipo_animal = relationship("TipoAnimal", back_populates="animais")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "id_tipo_animal": self.id_tipo_animal,
            "created": self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f"<Animal {self.id} {self.nome!r}>"



class TipoAnimal(Base):
    __tablename__ = "tipo_animal"

    id = Column(Integer, primary_key=True)
    nome = Column(String(120), nullable=False)

    animais = relationship("Animal", back_populates="tipo_animal")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome
        }

    def __repr__(self):
        return f"<TipoAnimal {self.id} {self.nome!r}>"
