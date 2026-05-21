"""
Script didático: DDL (create/drop tables) + DML (inserts) com sessão explícita.
Execute na raiz do projeto: python setup_database.py
"""

from datetime import datetime, timezone

from sqlalchemy import select

from database import Base, SessionLocal, engine
import models  # noqa: F401 — registra tabelas no metadata


def populate_database():
    print("Limpando e criando tabelas...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()

    try:
        print("Inserindo usuários...")
        usuarios = [
            models.Usuario(nome="Maria Silva", email="maria@escola.example", senha="123456", cpf="123.456.789-00"),
            models.Usuario(nome="João Santos", email="joao.santos@escola.example", senha="123456", cpf="987.654.321-00"),
        ]
        session.add_all(usuarios)
        session.flush()
        
        print("Inserindo produtos...")
        produtos = [
            models.Produto(
                nomeProduto="Produto 1",
                preco=10.00,
                descricao="Descrição 1",
                estoque=10,
                disponivel=True,
                imagem="https://placehold.co/100x100?text=Produto+1",
                usuario_id=usuarios[0].id,
                created_at=datetime.now(timezone.utc),
            ),
            models.Produto(
                nomeProduto="Produto 2",
                preco=20.00,
                descricao="Descrição 2",
                estoque=5,
                disponivel=True,
                imagem="https://placehold.co/100x100?text=Produto+2",
                usuario_id=usuarios[1].id,
                created_at=datetime.now(timezone.utc),
            ),
        ]
        session.add_all(produtos)
        session.flush()
        
        print("Inserindo favoritos...")
        favoritos = [
            models.Favorito(
                usuario_id=usuarios[0].id,
                produto_id=produtos[0].id,
            ),
        ]
        session.add_all(favoritos)
        session.flush()
        
        print("Inserindo endereços...")
        enderecos = [
            models.Endereco(
                cep="12345678",
                rua="Rua A",
                numero=123,
                bairro="Bairro X",
                cidade="Cidade Y",
                estado="Estado Z",
                complemento="Complemento 1",
                usuario_id=usuarios[0].id,
            ),
        ]
        session.add_all(enderecos)
        session.flush()
        
        print("Inserindo carrinhos...")
        carrinhos = [
            models.Carrinho(
                usuario_id=usuarios[0].id,
                produto_id=produtos[0].id,
            ),
        ]
        session.add_all(carrinhos)
        session.flush()
        
        print("Inserindo inspirações...")
        inspiracoes = [
            models.Inspiracao(
                titulo="Minha Primeira Inspiração",
                descricao="Uma descrição detalhada da inspiração.",
                usuario_id=usuarios[0].id,
                imagem="https://placehold.co/100x100?text=Inspiracao+1", # Adicionado imagem para consistência
            ),
        ]
        session.add_all(inspiracoes)
        session.flush()
        
        session.commit()
        print("\nSucesso! Commit concluído.")

        nu = len(session.scalars(select(models.Usuario)).all())
        np = len(session.scalars(select(models.Produto)).all())
        nf = len(session.scalars(select(models.Favorito)).all())
        ne = len(session.scalars(select(models.Endereco)).all())
        nc = len(session.scalars(select(models.Carrinho)).all())
        ni = len(session.scalars(select(models.Inspiracao)).all())
        print(f"- Usuários: {nu}")
        print(f"- Produtos: {np}")
        print(f"- Favoritos: {nf}")
        print(f"- Endereços: {ne}")
        print(f"- Carrinhos: {nc}")
        print(f"- Inspirações: {ni}")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    populate_database()
