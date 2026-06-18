from unittest.mock import MagicMock, patch
from servicos import cadastrar_usuario

def test_cadastrar_usuario_valido():
    
    usuario = MagicMock()
    
    #Arrange
    usuario.to_dict.return_value = {
        "id": 1,
        "nome": "Luisa",
        "email": "luisabieniek17@gmail.com",
        "senha": "senha123",
        "cpf": "12345678900"
    }
    
    session_fake = MagicMock()
    #Act
    with patch("servicos.SessionLocal", return_value=session_fake):
        with patch("servicos.Usuario", return_value=usuario):
            
            resultado = cadastrar_usuario({
                "nome": "Luisa",
                "email": "luisabieniek17@gmail.com",
                "senha": "senha123",
                "cpf": "12345678900"
            })
    #Assert
    assert resultado == {
        "id": 1,
        "nome": "Luisa",
        "email": "luisabieniek17@gmail.com",
        "senha": "senha123",
        "cpf": "12345678900"
    }