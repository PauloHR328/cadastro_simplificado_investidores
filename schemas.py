"""
Schemas para os 3 tipos de cadastro de investidores.
Cada schema define a estrutura dinâmica para renderização de formulários.
"""

# Mapeamento de tipos Python para tipos de campo
TYPE_MAPPING = {
    "string": "text",
    "number": "number",
    "integer": "number",
    "boolean": "checkbox",
    "date": "date",
    "float": "number",
}


def get_field_type(value):
    """Deduz o tipo de campo baseado no valor de exemplo."""
    if isinstance(value, bool):
        return "checkbox"
    elif isinstance(value, int):
        return "number"
    elif isinstance(value, float):
        return "number"
    elif isinstance(value, str):
        if "date" in value.lower() or value == "2024-12-31" or value == "2024-12-10":
            return "date"
        return "text"
    return "text"


# ============================================================================
# SCHEMA PESSOA FÍSICA (PF) - TipoImportacao: 1
# ============================================================================

SCHEMA_PF = {
    "name": "Pessoa Física",
    "tipo_importacao": 1,
    "fields": {
        "NomeCompleto": {"type": "text", "required": True, "label": "Nome Completo"},
        "CPFInvestidor": {"type": "text", "required": True, "label": "CPF"},
        "DataNascimento": {"type": "date", "required": True, "label": "Data de Nascimento"},
        "CNPJDistribuidor": {"type": "text", "required": True, "label": "CNPJ do Distribuidor"},
        "CodigoClassificacaoTributaria": {"type": "number", "required": False, "label": "Código Classificação Tributária"},
        "CodigoClassificacaoCvm": {"type": "number", "required": False, "label": "Código Classificação CVM"},
        "CodigoClassificacaoANBIMA": {"type": "number", "required": False, "label": "Código Classificação ANBIMA"},
        "Naturalidade": {"type": "text", "required": False, "label": "Naturalidade"},
        "CodigoPaisNacionalidade": {"type": "number", "required": False, "label": "Código País Nacionalidade"},
        "CodigoPaisDomicilioFiscal": {"type": "number", "required": False, "label": "Código País Domicílio Fiscal"},
        "NIF": {"type": "text", "required": False, "label": "NIF"},
        "TipoNIF": {"type": "number", "required": False, "label": "Tipo NIF"},
        "OutroCodigoPaisDomicilioFiscal": {"type": "number", "required": False, "label": "Outro Código País Domicílio Fiscal"},
        "OutroNIF": {"type": "text", "required": False, "label": "Outro NIF"},
        "OutroTipoNIF": {"type": "number", "required": False, "label": "Outro Tipo NIF"},
        "DDI": {"type": "number", "required": False, "label": "DDI"},
        "DDD": {"type": "number", "required": False, "label": "DDD"},
        "Telefone": {"type": "number", "required": False, "label": "Telefone"},
        "Email": {"type": "text", "required": False, "label": "Email"},
        "USPerson": {"type": "checkbox", "required": False, "label": "É US Person"},
        "ProfissaoOcupacao": {"type": "number", "required": False, "label": "Profissão/Ocupação"},
    },
    "sections": {
        "Endereco": {
            "label": "Endereço Residencial",
            "fields": {
                "Rua": {"type": "text", "required": False, "label": "Rua"},
                "Numero": {"type": "number", "required": False, "label": "Número"},
                "Complemento": {"type": "text", "required": False, "label": "Complemento"},
                "Bairro": {"type": "text", "required": False, "label": "Bairro"},
                "CEP": {"type": "text", "required": False, "label": "CEP"},
                "Cidade": {"type": "text", "required": False, "label": "Cidade"},
                "Uf": {"type": "text", "required": False, "label": "UF"},
                "CodigoPais": {"type": "number", "required": False, "label": "Código País"},
            }
        },
        "EnderecoCorrespondencia": {
            "label": "Endereço de Correspondência",
            "fields": {
                "TipoEndereco": {"type": "number", "required": False, "label": "Tipo Endereço"},
                "Endereco": {
                    "type": "object",
                    "fields": {
                        "Rua": {"type": "text", "required": False, "label": "Rua"},
                        "Numero": {"type": "number", "required": False, "label": "Número"},
                        "Complemento": {"type": "text", "required": False, "label": "Complemento"},
                        "Bairro": {"type": "text", "required": False, "label": "Bairro"},
                        "CEP": {"type": "text", "required": False, "label": "CEP"},
                        "Cidade": {"type": "text", "required": False, "label": "Cidade"},
                        "Uf": {"type": "text", "required": False, "label": "UF"},
                        "CodigoPais": {"type": "number", "required": False, "label": "Código País"},
                    }
                }
            }
        },
        "DadosFinanceiros": {
            "label": "Dados Financeiros",
            "fields": {
                "CodigoTipoOpcaoRecurso": {"type": "number", "required": False, "label": "Código Tipo Opção Recurso"},
                "DadosRenda": {
                    "type": "object",
                    "fields": {
                        "RendaMensal": {"type": "checkbox", "required": False, "label": "Renda Mensal"},
                        "PartilhaBens": {"type": "checkbox", "required": False, "label": "Partilha Bens"},
                        "Heranca": {"type": "checkbox", "required": False, "label": "Herança"},
                        "Aposentadoria": {"type": "checkbox", "required": False, "label": "Aposentadoria"},
                        "AluguelPropriedades": {"type": "checkbox", "required": False, "label": "Aluguel Propriedades"},
                        "Doacao": {"type": "checkbox", "required": False, "label": "Doação"},
                        "OutrosEspecifique": {"type": "text", "required": False, "label": "Outros (Especifique)"},
                    }
                },
                "RendaMensal": {"type": "number", "required": False, "label": "Renda Mensal (R$)"},
                "PatrimonioTotal": {"type": "number", "required": False, "label": "Patrimônio Total (R$)"},
                "OutrosRendimentosAnual": {"type": "number", "required": False, "label": "Outros Rendimentos Anuais (R$)"},
                "OrigemOutrosRendimentosAnual": {"type": "text", "required": False, "label": "Origem Outros Rendimentos"},
            }
        },
        "ContaBancaria": {
            "label": "Contas Bancárias",
            "type": "array",
            "fields": {
                "CodigoBanco": {"type": "number", "required": False, "label": "Código Banco"},
                "NumeroAgencia": {"type": "text", "required": False, "label": "Número Agência"},
                "NumeroConta": {"type": "text", "required": False, "label": "Número Conta"},
                "DigitoConta": {"type": "text", "required": False, "label": "Dígito Conta"},
            }
        },
        "Representante": {
            "label": "Representante",
            "fields": {
                "TipoRepresentante": {"type": "number", "required": False, "label": "Tipo Representante"},
                "Nome": {"type": "text", "required": False, "label": "Nome"},
                "CPF": {"type": "number", "required": False, "label": "CPF"},
                "DataNascimento": {"type": "date", "required": False, "label": "Data Nascimento"},
                "CodigoPaisNacionalidade": {"type": "number", "required": False, "label": "Código País Nacionalidade"},
                "Naturalidade": {"type": "text", "required": False, "label": "Naturalidade"},
                "CodigoTipoDocumento": {"type": "number", "required": False, "label": "Código Tipo Documento"},
                "NumeroDocumento": {"type": "text", "required": False, "label": "Número Documento"},
                "DDI": {"type": "number", "required": False, "label": "DDI"},
                "DDD": {"type": "number", "required": False, "label": "DDD"},
                "Celular": {"type": "number", "required": False, "label": "Celular"},
                "Email": {"type": "text", "required": False, "label": "Email"},
                "CodigoPaisDomicilioFiscal": {"type": "number", "required": False, "label": "Código País Domicílio Fiscal"},
                "NIF": {"type": "text", "required": False, "label": "NIF"},
                "TipoNIF": {"type": "number", "required": False, "label": "Tipo NIF"},
                "OutroCodigoPaisDomicilioFiscal": {"type": "number", "required": False, "label": "Outro Código País Domicílio Fiscal"},
                "OutroNIF": {"type": "text", "required": False, "label": "Outro NIF"},
                "OutroTipoNIF": {"type": "number", "required": False, "label": "Outro Tipo NIF"},
                "Endereco": {
                    "type": "object",
                    "fields": {
                        "Rua": {"type": "text", "required": False, "label": "Rua"},
                        "Numero": {"type": "number", "required": False, "label": "Número"},
                        "Complemento": {"type": "text", "required": False, "label": "Complemento"},
                        "Bairro": {"type": "text", "required": False, "label": "Bairro"},
                        "CEP": {"type": "text", "required": False, "label": "CEP"},
                        "Cidade": {"type": "text", "required": False, "label": "Cidade"},
                        "Uf": {"type": "text", "required": False, "label": "UF"},
                        "CodigoPais": {"type": "number", "required": False, "label": "Código País"},
                    }
                },
            }
        },
        "Cotitular": {
            "label": "Cotitular",
            "optional": True,
            "fields": {
                "NomeCompleto": {"type": "text", "required": False, "label": "Nome Completo"},
                "CPFInvestidor": {"type": "text", "required": False, "label": "CPF"},
                "DataNascimento": {"type": "date", "required": False, "label": "Data Nascimento"},
                "Naturalidade": {"type": "text", "required": False, "label": "Naturalidade"},
                "CodigoPaisNacionalidade": {"type": "number", "required": False, "label": "Código País Nacionalidade"},
                "CodigoPaisDomicilioFiscal": {"type": "number", "required": False, "label": "Código País Domicílio Fiscal"},
                "NIF": {"type": "text", "required": False, "label": "NIF"},
                "TipoNIF": {"type": "number", "required": False, "label": "Tipo NIF"},
                "OutroCodigoPaisDomicilioFiscal": {"type": "number", "required": False, "label": "Outro Código País Domicílio Fiscal"},
                "OutroNIF": {"type": "text", "required": False, "label": "Outro NIF"},
                "OutroTipoNIF": {"type": "number", "required": False, "label": "Outro Tipo NIF"},
                "DDI": {"type": "number", "required": False, "label": "DDI"},
                "DDD": {"type": "number", "required": False, "label": "DDD"},
                "Telefone": {"type": "number", "required": False, "label": "Telefone"},
                "Email": {"type": "text", "required": False, "label": "Email"},
                "USPerson": {"type": "checkbox", "required": False, "label": "É US Person"},
                "ProfissaoOcupacao": {"type": "number", "required": False, "label": "Profissão/Ocupação"},
            }
        },
    }
}

# ============================================================================
# SCHEMA PESSOA JURÍDICA (PJ) - TipoImportacao: 3
# ============================================================================

SCHEMA_PJ = {
    "name": "Pessoa Jurídica",
    "tipo_importacao": 3,
    "fields": {
        "RazaoSocial": {"type": "text", "required": True, "label": "Razão Social"},
        "NomeFantasia": {"type": "text", "required": False, "label": "Nome Fantasia"},
        "CNPJInvestidor": {"type": "text", "required": True, "label": "CNPJ Investidor"},
        "CNPJDistribuidor": {"type": "text", "required": True, "label": "CNPJ Distribuidor"},
        "AtividadeEconomicaPrincipal": {"type": "number", "required": False, "label": "Atividade Econômica Principal"},
        "CNAE": {"type": "text", "required": False, "label": "CNAE"},
        "CodigoPais": {"type": "number", "required": False, "label": "Código País"},
        "CodigoClassificacaoTributaria": {"type": "number", "required": False, "label": "Código Classificação Tributária"},
        "CodigoClassificacaoCvm": {"type": "number", "required": False, "label": "Código Classificação CVM"},
        "CodigoClassificacaoANBIMA": {"type": "number", "required": False, "label": "Código Classificação ANBIMA"},
        "CodigoPaisDomicilioFiscal": {"type": "number", "required": False, "label": "Código País Domicílio Fiscal"},
        "TipoNIF": {"type": "number", "required": False, "label": "Tipo NIF"},
        "NIF": {"type": "text", "required": False, "label": "NIF"},
        "OutroCodigoPaisDomicilioFiscal": {"type": "number", "required": False, "label": "Outro Código País Domicílio Fiscal"},
        "OutroNIF": {"type": "text", "required": False, "label": "Outro NIF"},
        "OutroTipoNIF": {"type": "number", "required": False, "label": "Outro Tipo NIF"},
        "USPerson": {"type": "checkbox", "required": False, "label": "É US Person"},
        "SituacaoPatrimonial": {"type": "number", "required": False, "label": "Situação Patrimonial"},
        "FaturamentoMedio": {"type": "number", "required": False, "label": "Faturamento Médio"},
    },
    "sections": {
        "EnderecoSedeSocial": {
            "label": "Endereço Sede Social",
            "fields": {
                "Rua": {"type": "text", "required": False, "label": "Rua"},
                "Numero": {"type": "number", "required": False, "label": "Número"},
                "Complemento": {"type": "text", "required": False, "label": "Complemento"},
                "Bairro": {"type": "text", "required": False, "label": "Bairro"},
                "CEP": {"type": "text", "required": False, "label": "CEP"},
                "Cidade": {"type": "text", "required": False, "label": "Cidade"},
                "Uf": {"type": "text", "required": False, "label": "UF"},
                "CodigoPais": {"type": "number", "required": False, "label": "Código País"},
            }
        },
        "Administrador": {
            "label": "Administrador",
            "fields": {
                "Nome": {"type": "text", "required": False, "label": "Nome"},
                "CNPJ": {"type": "text", "required": False, "label": "CNPJ"},
            }
        },
        "ContaBancaria": {
            "label": "Contas Bancárias",
            "type": "array",
            "fields": {
                "CodigoBanco": {"type": "number", "required": False, "label": "Código Banco"},
                "NumeroAgencia": {"type": "text", "required": False, "label": "Número Agência"},
                "NumeroConta": {"type": "text", "required": False, "label": "Número Conta"},
                "DigitoConta": {"type": "text", "required": False, "label": "Dígito Conta"},
            }
        },
        "ReferenciasComerciais": {
            "label": "Referências Comerciais",
            "type": "array",
            "fields": {
                "Nome": {"type": "text", "required": False, "label": "Nome"},
                "DDI": {"type": "number", "required": False, "label": "DDI"},
                "DDD": {"type": "number", "required": False, "label": "DDD"},
                "NumeroTelefone": {"type": "number", "required": False, "label": "Número Telefone"},
            }
        },
        "DeclaracaoCliente": {
            "label": "Declaração do Cliente",
            "fields": {
                "AtividadeFinanceira": {"type": "checkbox", "required": False, "label": "Atividade Financeira"},
                "PFFI": {"type": "checkbox", "required": False, "label": "PFFI"},
                "GIIN": {"type": "number", "required": False, "label": "GIIN"},
                "InstituicaoFinanceiraAdereFATCA": {"type": "checkbox", "required": False, "label": "Instituição Financeira Adere FATCA"},
                "DCFFIRegistrada": {"type": "checkbox", "required": False, "label": "DCFFI Registrada"},
                "DCFFICertificada": {"type": "checkbox", "required": False, "label": "DCFFI Certificada"},
                "DCFFITipoEntidade": {"type": "text", "required": False, "label": "DCFFI Tipo Entidade"},
                "InstituicaoFinanceiraNaoParticipante": {"type": "checkbox", "required": False, "label": "Instituição Financeira Não Participante"},
                "BeneficiariaEfetivaIsenta": {"type": "checkbox", "required": False, "label": "Beneficiária Efetiva Isenta"},
                "BeneficiariaEfetivaIsentaTipoEntidade": {"type": "text", "required": False, "label": "Beneficiária Efetiva Isenta Tipo Entidade"},
                "NFFE": {"type": "checkbox", "required": False, "label": "NFFE"},
                "NFFETipoEntidade": {"type": "text", "required": False, "label": "NFFE Tipo Entidade"},
                "PessoaFisicaEUAComParticipacaoSubstancial": {"type": "checkbox", "required": False, "label": "Pessoa Física EUA Com Participação Substancial"},
                "MaisDe50PorcentoReceitaAtivosEstritamenteAtividades": {"type": "checkbox", "required": False, "label": "Mais de 50% Receita Ativos Estritamente Atividades"},
            }
        },
        "SociosPessoaJuridica": {
            "label": "Sócios Pessoa Jurídica",
            "type": "array",
            "fields": {
                "RazaoSocial": {"type": "text", "required": False, "label": "Razão Social"},
                "CodigoPaisSede": {"type": "number", "required": False, "label": "Código País Sede"},
                "CNPJ": {"type": "text", "required": False, "label": "CNPJ"},
                "CNPJEmpresaSocio": {"type": "text", "required": False, "label": "CNPJ Empresa Sócio"},
                "CodigoPaisDomicilioFiscal": {"type": "number", "required": False, "label": "Código País Domicílio Fiscal"},
                "TipoNIF": {"type": "number", "required": False, "label": "Tipo NIF"},
                "NIF": {"type": "text", "required": False, "label": "NIF"},
                "CodigoOutroPaisDomicilioFiscal": {"type": "number", "required": False, "label": "Código Outro País Domicílio Fiscal"},
                "OutroTipoNIF": {"type": "number", "required": False, "label": "Outro Tipo NIF"},
                "OutroNIF": {"type": "text", "required": False, "label": "Outro NIF"},
                "OutroCodigoPaisDomicilioFiscal": {"type": "number", "required": False, "label": "Outro Código País Domicílio Fiscal"},
                "ParticipacaoSociedade": {"type": "number", "required": False, "label": "Participação Sociedade (%)"},
                "DDI": {"type": "number", "required": False, "label": "DDI"},
                "DDD": {"type": "number", "required": False, "label": "DDD"},
                "Telefone": {"type": "number", "required": False, "label": "Telefone"},
                "Email": {"type": "text", "required": False, "label": "Email"},
            }
        },
        "SociosPessoaFisica": {
            "label": "Sócios Pessoa Física",
            "type": "array",
            "fields": {
                "NomeCompleto": {"type": "text", "required": False, "label": "Nome Completo"},
                "CPF": {"type": "text", "required": False, "label": "CPF"},
                "CNPJEmpresaSocio": {"type": "text", "required": False, "label": "CNPJ Empresa Sócio"},
                "DataNascimento": {"type": "date", "required": False, "label": "Data Nascimento"},
                "Naturalidade": {"type": "text", "required": False, "label": "Naturalidade"},
                "CodigoPaisNacionalidade": {"type": "number", "required": False, "label": "Código País Nacionalidade"},
                "CodigoTipoDocumento": {"type": "number", "required": False, "label": "Código Tipo Documento"},
                "NumeroDocumento": {"type": "text", "required": False, "label": "Número Documento"},
                "PossuiCidadania": {"type": "checkbox", "required": False, "label": "Possui Cidadania"},
                "CodigoPaisCidadania": {"type": "number", "required": False, "label": "Código País Cidadania"},
                "OutroCodigoPaisCidadania": {"type": "number", "required": False, "label": "Outro Código País Cidadania"},
                "CodigoPaisDomicilioFiscal": {"type": "number", "required": False, "label": "Código País Domicílio Fiscal"},
                "TipoNIF": {"type": "number", "required": False, "label": "Tipo NIF"},
                "NIF": {"type": "number", "required": False, "label": "NIF"},
                "OutroCodigoPaisDomicilioFiscal": {"type": "number", "required": False, "label": "Outro Código País Domicílio Fiscal"},
                "OutroTipoNIF": {"type": "number", "required": False, "label": "Outro Tipo NIF"},
                "OutroNIF": {"type": "text", "required": False, "label": "Outro NIF"},
                "DDI": {"type": "number", "required": False, "label": "DDI"},
                "DDD": {"type": "number", "required": False, "label": "DDD"},
                "Telefone": {"type": "number", "required": False, "label": "Telefone"},
                "Email": {"type": "text", "required": False, "label": "Email"},
            }
        },
        "Representante": {
            "label": "Representante",
            "fields": {
                "FormaRepresentacao": {"type": "number", "required": False, "label": "Forma Representação"},
                "TipoRepresentante": {"type": "number", "required": False, "label": "Tipo Representante"},
                "Nome": {"type": "text", "required": False, "label": "Nome"},
                "CPF": {"type": "number", "required": False, "label": "CPF"},
                "DataNascimento": {"type": "date", "required": False, "label": "Data Nascimento"},
                "CodigoPaisNacionalidade": {"type": "number", "required": False, "label": "Código País Nacionalidade"},
                "Naturalidade": {"type": "text", "required": False, "label": "Naturalidade"},
                "CodigoTipoDocumento": {"type": "number", "required": False, "label": "Código Tipo Documento"},
                "NumeroDocumento": {"type": "text", "required": False, "label": "Número Documento"},
                "CodigoPaisDomicilioFiscal": {"type": "number", "required": False, "label": "Código País Domicílio Fiscal"},
                "TipoNIF": {"type": "number", "required": False, "label": "Tipo NIF"},
                "NIF": {"type": "text", "required": False, "label": "NIF"},
                "OutroCodigoPaisDomicilioFiscal": {"type": "number", "required": False, "label": "Outro Código País Domicílio Fiscal"},
                "OutroTipoNIF": {"type": "number", "required": False, "label": "Outro Tipo NIF"},
                "OutroNIF": {"type": "text", "required": False, "label": "Outro NIF"},
                "DDI": {"type": "number", "required": False, "label": "DDI"},
                "DDD": {"type": "number", "required": False, "label": "DDD"},
                "Celular": {"type": "number", "required": False, "label": "Celular"},
                "Email": {"type": "text", "required": False, "label": "Email"},
            }
        },
        "INR": {
            "label": "INR (Intermediário Não Residente)",
            "optional": True,
            "fields": {
                "TipoRepresentante": {"type": "number", "required": False, "label": "Tipo Representante"},
                "Nome": {"type": "text", "required": False, "label": "Nome"},
                "CPF": {"type": "number", "required": False, "label": "CPF"},
                "DataNascimento": {"type": "date", "required": False, "label": "Data Nascimento"},
                "CodigoPaisNacionalidade": {"type": "number", "required": False, "label": "Código País Nacionalidade"},
                "Naturalidade": {"type": "text", "required": False, "label": "Naturalidade"},
                "CodigoTipoDocumento": {"type": "number", "required": False, "label": "Código Tipo Documento"},
                "NumeroDocumento": {"type": "text", "required": False, "label": "Número Documento"},
                "CodigoPaisDomicilioFiscal": {"type": "number", "required": False, "label": "Código País Domicílio Fiscal"},
                "TipoNIF": {"type": "number", "required": False, "label": "Tipo NIF"},
                "NIF": {"type": "text", "required": False, "label": "NIF"},
                "OutroCodigoPaisDomicilioFiscal": {"type": "number", "required": False, "label": "Outro Código País Domicílio Fiscal"},
                "OutroTipoNIF": {"type": "number", "required": False, "label": "Outro Tipo NIF"},
                "OutroNIF": {"type": "text", "required": False, "label": "Outro NIF"},
                "DDI": {"type": "number", "required": False, "label": "DDI"},
                "DDD": {"type": "number", "required": False, "label": "DDD"},
                "Celular": {"type": "number", "required": False, "label": "Celular"},
                "Email": {"type": "text", "required": False, "label": "Email"},
            }
        },
    }
}

# ============================================================================
# SCHEMA FUNDO - TipoImportacao: 2
# ============================================================================

SCHEMA_FUNDO = {
    "name": "Fundo",
    "tipo_importacao": 2,
    "fields": {
        "NomeFundo": {"type": "text", "required": True, "label": "Nome do Fundo"},
        "CNPJFundo": {"type": "text", "required": True, "label": "CNPJ Fundo"},
        "DataConstituicao": {"type": "date", "required": True, "label": "Data de Constituição"},
        "CNPJDistribuidor": {"type": "text", "required": True, "label": "CNPJ Distribuidor"},
        "CodigoClassificacaoTributaria": {"type": "number", "required": False, "label": "Código Classificação Tributária"},
        "CodigoClassificacaoCvm": {"type": "number", "required": False, "label": "Código Classificação CVM"},
        "CodigoClassificacaoANBIMA": {"type": "number", "required": False, "label": "Código Classificação ANBIMA"},
        "EnderecoCorrespondencia": {"type": "number", "required": False, "label": "Endereço Correspondência"},
        "InformeReceitaFederal": {"type": "checkbox", "required": False, "label": "Informe Receita Federal"},
        "CETIP": {"type": "number", "required": False, "label": "CETIP"},
        "CodigoTipoRepresentante": {"type": "number", "required": False, "label": "Código Tipo Representante"},
    },
    "sections": {
        "ContaBancaria": {
            "label": "Conta Bancária",
            "fields": {
                "CodigoBanco": {"type": "number", "required": False, "label": "Código Banco"},
                "NumeroAgencia": {"type": "text", "required": False, "label": "Número Agência"},
                "NumeroConta": {"type": "text", "required": False, "label": "Número Conta"},
                "DigitoConta": {"type": "text", "required": False, "label": "Dígito Conta"},
            }
        },
        "Administrador": {
            "label": "Administrador",
            "fields": {
                "Nome": {"type": "text", "required": False, "label": "Nome"},
                "CpfCnpj": {"type": "text", "required": False, "label": "CPF/CNPJ"},
                "DDI": {"type": "number", "required": False, "label": "DDI"},
                "DDD": {"type": "number", "required": False, "label": "DDD"},
                "Celular": {"type": "number", "required": False, "label": "Celular"},
                "Email": {"type": "text", "required": False, "label": "Email"},
                "Endereco": {
                    "type": "object",
                    "fields": {
                        "Rua": {"type": "text", "required": False, "label": "Rua"},
                        "Numero": {"type": "number", "required": False, "label": "Número"},
                        "Complemento": {"type": "text", "required": False, "label": "Complemento"},
                        "Bairro": {"type": "text", "required": False, "label": "Bairro"},
                        "CEP": {"type": "text", "required": False, "label": "CEP"},
                        "Cidade": {"type": "text", "required": False, "label": "Cidade"},
                        "Uf": {"type": "text", "required": False, "label": "UF"},
                        "CodigoPais": {"type": "number", "required": False, "label": "Código País"},
                    }
                },
            }
        },
        "Gestores": {
            "label": "Gestores",
            "type": "array",
            "fields": {
                "Nome": {"type": "text", "required": False, "label": "Nome"},
                "CpfCnpj": {"type": "text", "required": False, "label": "CPF/CNPJ"},
                "DDI": {"type": "number", "required": False, "label": "DDI"},
                "DDD": {"type": "number", "required": False, "label": "DDD"},
                "Celular": {"type": "number", "required": False, "label": "Celular"},
                "Email": {"type": "text", "required": False, "label": "Email"},
            }
        },
        "Representantes": {
            "label": "Representantes",
            "type": "array",
            "fields": {
                "TipoRepresentante": {"type": "number", "required": False, "label": "Tipo Representante"},
                "Nome": {"type": "text", "required": False, "label": "Nome"},
                "CPF": {"type": "number", "required": False, "label": "CPF"},
                "DDI": {"type": "number", "required": False, "label": "DDI"},
                "DDD": {"type": "number", "required": False, "label": "DDD"},
                "Celular": {"type": "number", "required": False, "label": "Celular"},
                "Email": {"type": "text", "required": False, "label": "Email"},
                "DataNascimento": {"type": "date", "required": False, "label": "Data Nascimento"},
                "CodigoPaisNacionalidade": {"type": "number", "required": False, "label": "Código País Nacionalidade"},
                "Naturalidade": {"type": "text", "required": False, "label": "Naturalidade"},
                "CodigoTipoDocumento": {"type": "number", "required": False, "label": "Código Tipo Documento"},
                "NumeroDocumento": {"type": "text", "required": False, "label": "Número Documento"},
                "CodigoPaisDomicilioFiscal": {"type": "number", "required": False, "label": "Código País Domicílio Fiscal"},
            }
        },
        "BeneficiariosFinais": {
            "label": "Beneficiários Finais",
            "type": "array",
            "fields": {
                "RazaoSocial": {"type": "text", "required": False, "label": "Razão Social"},
                "CpfCnpj": {"type": "text", "required": False, "label": "CPF/CNPJ"},
                "Participacao": {"type": "number", "required": False, "label": "Participação (%)"},
                "Cep": {"type": "text", "required": False, "label": "CEP"},
                "NumeroEndereco": {"type": "number", "required": False, "label": "Número Endereço"},
                "RendaMensal": {"type": "number", "required": False, "label": "Renda Mensal"},
                "PatrimonioTotal": {"type": "number", "required": False, "label": "Patrimônio Total"},
                "CodigoPais": {"type": "number", "required": False, "label": "Código País"},
            }
        },
    }
}

# Dicionário centralizado de schemas
SCHEMAS = {
    "Pessoa Física": SCHEMA_PF,
    "Pessoa Jurídica": SCHEMA_PJ,
    "Fundo": SCHEMA_FUNDO,
}

SCHEMAS_BY_TYPE = {
    1: SCHEMA_PF,
    2: SCHEMA_FUNDO,
    3: SCHEMA_PJ,
}
