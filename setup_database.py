"""
Script didático: DDL (create/drop tables) + DML (inserts) com sessão explícita.
Execute na raiz do projeto: python setup_database.py
"""

from datetime import datetime

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
                disponivel=True,
                created_at=datetime.now(),
            ),
            models.Produto(
                nomeProduto="Produto 2",
                preco=20.00,
                descricao="Descrição 2",
                disponivel=True,
                created_at=datetime.now(),
            ),
        ]
        session.add_all(produtos)
        session.flush()


        print("Inserindo turmas...")
        turmas = [
            models.Turma(
                nome="luisalinda123",
                codigo="MAT-2026-A",
                usuario_id=usuarios[0].id,
            ),
            models.Turma(
                nome="Física B",
                codigo="FIS-2026-B",
                usuario_id=usuarios[0].id,
            ),
            models.Turma(
                nome="Português A",
                codigo="PORT-2026-A",
                usuario_id=usuarios[1].id,
            ),
        ]
        session.add_all(turmas)
        session.flush()

        print("Inserindo alunos...")
        alunos = [
            models.Aluno(
                nome="Ana Costa",
                email="ana@escola.example",
                turma_id=turmas[0].id,
                endereco="asdasdsad"
            ),
            models.Aluno(
                nome="Bruno Lima",
                email="bruno@escola.example",
                turma_id=turmas[0].id,
                endereco="asdasdsad"
            ),
            models.Aluno(
                nome="Carla Dias",
                email="carla@escola.example",
                turma_id=turmas[1].id,
                endereco="asdasdsad"
            ),
            models.Aluno(
                nome="Diego Rocha",
                email="diego@escola.example",
                turma_id=turmas[2].id,
                endereco="asdasdsad"
            ),
        ]
        session.add_all(alunos)
####

        print("Inserindo Departamentos...")
        departamentos = [
            models.Departamento(
                nome="Contabilidade"
            ),
            models.Departamento(
                nome="Financeiro"
            ),
        ]
        session.add_all(departamentos)
        session.flush()

####

#####
        print("Inserindo TipoAnimais...")
        tipoAnimais = [
            models.TipoAnimal(
                nome="Canino"
            ),
            models.TipoAnimal(
                nome="Felino",
            ),
        ]
        session.add_all(tipoAnimais)
        session.flush()

###
        print("Inserindo Animais...")
        animais = [
            models.Animal(
                nome="Dante",
                id_tipo_animal=tipoAnimais[0].id,
                created_at=datetime.now(),
            ),
            models.Animal(
                nome="Toby",
                id_tipo_animal=tipoAnimais[1].id,
                created_at=datetime.now(),
            ),
        ]
        session.add_all(animais)
        session.flush()


###
        print("Inserindo funcionários...")
        funcionarios = [
            models.Funcionario(
                nome="Daniel Eletronicos",
                email="eletronico@gmail.com",
                senha="123456",
                id_departamento=departamentos[0].id,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
            models.Funcionario(
                nome="Daniel Livros",
                email="livro@gmail.com",
                senha="123456",
                id_departamento=departamentos[1].id,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
        ]
        session.add_all(funcionarios)
        
        session.commit()
        print("\nSucesso! Commit concluído.")

        np = len(session.scalars(select(models.Usuario)).all())
        nt = len(session.scalars(select(models.Turma)).all())
        na = len(session.scalars(select(models.Aluno)).all())
        print(f"- Usuários: {np}")
        print(f"- Turmas: {nt}")
        print(f"- Alunos: {na}")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    populate_database()
