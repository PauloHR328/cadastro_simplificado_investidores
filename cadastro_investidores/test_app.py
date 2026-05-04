"""
Testes básicos para a aplicação Cadastro de Investidores.
Execute com: python test_app.py
"""

import sys
import json
from schemas import SCHEMAS, SCHEMA_PF, SCHEMA_PJ, SCHEMA_FUNDO
from utils import (
    build_json_output,
    clean_empty_values,
    format_json_output,
)


def test_schemas():
    """Testa se todos os schemas estão corretamente definidos."""
    print("\n" + "=" * 60)
    print("TESTE 1: Validação de Schemas")
    print("=" * 60)
    
    assert "Pessoa Física" in SCHEMAS, "Schema PF não encontrado"
    assert "Pessoa Jurídica" in SCHEMAS, "Schema PJ não encontrado"
    assert "Fundo" in SCHEMAS, "Schema Fundo não encontrado"
    
    assert SCHEMA_PF["tipo_importacao"] == 1, "TipoImportacao PF incorreto"
    assert SCHEMA_PJ["tipo_importacao"] == 3, "TipoImportacao PJ incorreto"
    assert SCHEMA_FUNDO["tipo_importacao"] == 2, "TipoImportacao Fundo incorreto"
    
    print("✅ Schema Pessoa Física (PF):")
    print(f"   - TipoImportacao: {SCHEMA_PF['tipo_importacao']}")
    print(f"   - Campos simples: {len(SCHEMA_PF.get('fields', {}))}")
    print(f"   - Seções: {len(SCHEMA_PF.get('sections', {}))}")
    
    print("✅ Schema Pessoa Jurídica (PJ):")
    print(f"   - TipoImportacao: {SCHEMA_PJ['tipo_importacao']}")
    print(f"   - Campos simples: {len(SCHEMA_PJ.get('fields', {}))}")
    print(f"   - Seções: {len(SCHEMA_PJ.get('sections', {}))}")
    
    print("✅ Schema Fundo:")
    print(f"   - TipoImportacao: {SCHEMA_FUNDO['tipo_importacao']}")
    print(f"   - Campos simples: {len(SCHEMA_FUNDO.get('fields', {}))}")
    print(f"   - Seções: {len(SCHEMA_FUNDO.get('sections', {}))}")


def test_json_build_pf():
    """Testa construção de JSON para Pessoa Física."""
    print("\n" + "=" * 60)
    print("TESTE 2: Construção de JSON - Pessoa Física")
    print("=" * 60)
    
    dados = {
        "NomeCompleto": "João Silva",
        "CPFInvestidor": "12345678900",
        "DataNascimento": "1990-05-15",
        "CNPJDistribuidor": "12345678000190",
        "Email": "joao@example.com",
        "Endereco": {
            "Rua": "Rua A",
            "Numero": 123,
            "Cidade": "São Paulo",
            "Uf": "SP",
        }
    }
    
    json_output = build_json_output(1, dados)
    
    assert json_output["TipoImportacao"] == 1, "TipoImportacao incorreto"
    assert len(json_output["Dados"]) == 1, "Dados array deve ter 1 elemento"
    assert json_output["Dados"][0]["NomeCompleto"] == "João Silva", "Nome incorreto"
    
    json_str = format_json_output(json_output)
    print("✅ JSON gerado com sucesso:")
    print(json_str[:200] + "...")


def test_json_build_pj():
    """Testa construção de JSON para Pessoa Jurídica."""
    print("\n" + "=" * 60)
    print("TESTE 3: Construção de JSON - Pessoa Jurídica")
    print("=" * 60)
    
    dados = {
        "RazaoSocial": "Empresa XYZ Ltda",
        "NomeFantasia": "Empresa XYZ",
        "CNPJInvestidor": "12345678000190",
        "CNPJDistribuidor": "98765432000171",
        "EnderecoSedeSocial": {
            "Rua": "Avenida B",
            "Numero": 456,
            "Cidade": "Rio de Janeiro",
            "Uf": "RJ",
        }
    }
    
    json_output = build_json_output(3, dados)
    
    assert json_output["TipoImportacao"] == 3, "TipoImportacao incorreto"
    assert len(json_output["Dados"]) == 1, "Dados array deve ter 1 elemento"
    assert json_output["Dados"][0]["RazaoSocial"] == "Empresa XYZ Ltda", "Razão Social incorreta"
    
    json_str = format_json_output(json_output)
    print("✅ JSON gerado com sucesso:")
    print(json_str[:200] + "...")


def test_json_build_fundo():
    """Testa construção de JSON para Fundo."""
    print("\n" + "=" * 60)
    print("TESTE 4: Construção de JSON - Fundo")
    print("=" * 60)
    
    dados = {
        "NomeFundo": "Fundo de Investimento ABC",
        "CNPJFundo": "12345678000190",
        "DataConstituicao": "2020-01-15",
        "CNPJDistribuidor": "98765432000171",
        "Administrador": {
            "Nome": "Administradora XYZ",
            "CpfCnpj": "12345678000191",
        }
    }
    
    json_output = build_json_output(2, dados)
    
    assert json_output["TipoImportacao"] == 2, "TipoImportacao incorreto"
    assert len(json_output["Dados"]) == 1, "Dados array deve ter 1 elemento"
    assert json_output["Dados"][0]["NomeFundo"] == "Fundo de Investimento ABC", "Nome Fundo incorreto"
    
    json_str = format_json_output(json_output)
    print("✅ JSON gerado com sucesso:")
    print(json_str[:200] + "...")


def test_clean_empty_values():
    """Testa limpeza de valores vazios."""
    print("\n" + "=" * 60)
    print("TESTE 5: Limpeza de Valores Vazios")
    print("=" * 60)
    
    obj = {
        "Nome": "João",
        "Email": "",
        "Telefone": 0,
        "Endereco": {
            "Rua": "Rua A",
            "Numero": 0,
            "Cidade": "",
        },
        "Vazio": None,
    }
    
    cleaned = clean_empty_values(obj)
    
    assert "Email" not in cleaned, "Email vazio deveria ser removido"
    assert "Telefone" not in cleaned, "Telefone 0 deveria ser removido"
    assert "Vazio" not in cleaned, "Valor None deveria ser removido"
    assert cleaned["Nome"] == "João", "Nome deveria ser mantido"
    assert "Numero" not in cleaned["Endereco"], "Numero 0 deveria ser removido"
    
    print("✅ Limpeza realizada com sucesso:")
    print(json.dumps(cleaned, indent=2, ensure_ascii=False))


def test_format_json():
    """Testa formatação de JSON."""
    print("\n" + "=" * 60)
    print("TESTE 6: Formatação de JSON")
    print("=" * 60)
    
    json_obj = {
        "TipoImportacao": 1,
        "Dados": [{"Nome": "João", "CPF": "123"}]
    }
    
    formatted = format_json_output(json_obj)
    
    assert isinstance(formatted, str), "Resultado deve ser string"
    assert "TipoImportacao" in formatted, "JSON deve conter TipoImportacao"
    assert formatted.count("\n") > 0, "JSON deve ser formatado com indentação"
    
    # Validar que pode ser parseado novamente
    parsed = json.loads(formatted)
    assert parsed["TipoImportacao"] == 1, "JSON parseado deve ser válido"
    
    print("✅ JSON formatado com sucesso:")
    print(formatted)


def run_all_tests():
    """Executa todos os testes."""
    print("\n" + "=" * 60)
    print("INICIANDO TESTES - Cadastro de Investidores")
    print("=" * 60)
    
    try:
        test_schemas()
        test_json_build_pf()
        test_json_build_pj()
        test_json_build_fundo()
        test_clean_empty_values()
        test_format_json()
        
        print("\n" + "=" * 60)
        print("✅ TODOS OS TESTES PASSARAM COM SUCESSO!")
        print("=" * 60 + "\n")
        return True
        
    except AssertionError as e:
        print(f"\n❌ ERRO NO TESTE: {str(e)}")
        return False
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {str(e)}")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
