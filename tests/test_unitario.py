from servicos import _texto_obrigatorio
import pytest

def test_texto_obrigatorio():
    resultado = _texto_obrigatorio("luisa", "nome")
    assert resultado == "luisa"