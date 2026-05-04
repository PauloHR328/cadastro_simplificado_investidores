# 💼 Cadastro de Investidores - MVP

Uma aplicação Streamlit para cadastro dinâmico de investidores (Pessoa Física, Pessoa Jurídica e Fundos) com geração automática de JSON válido.

## 🎯 Objetivo

Substituir um fluxo baseado em Excel por uma aplicação executável flexível, dinâmica e escalável, permitindo que usuários preencham dados em uma interface amigável e gerem automaticamente JSONs válidos conforme os modelos predefinidos.

## ✨ Características

✅ **Interface Dinâmica**: Formulários gerados automaticamente baseados em schemas  
✅ **3 Tipos de Cadastro**: Pessoa Física, Pessoa Jurídica e Fundo  
✅ **Validação de Campos**: Campos obrigatórios destacados e validados  
✅ **Suporte a Arrays Dinâmicos**: Adicionar/remover múltiplos itens (ex: contas bancárias, sócios)  
✅ **Objetos Aninhados**: Estruturas complexas organizadas em seções  
✅ **JSON em Tempo Real**: Prévia do JSON gerado  
✅ **Download de Arquivo**: Exportar JSON com timestamp  
✅ **Escalável**: Fácil adicionar novos campos ou tipos de cadastro  
✅ **Sem Hardcoding**: Estrutura baseada em schemas configuráveis  

## 📋 Tipos de Cadastro

### Pessoa Física (PF) - TipoImportacao: 1
- Dados pessoais completos
- Endereço residencial e de correspondência
- Dados financeiros
- Contas bancárias
- Representante
- Cotitular

### Pessoa Jurídica (PJ) - TipoImportacao: 3
- Dados da empresa
- Endereço da sede social
- Administrador e contas bancárias
- Referências comerciais
- Declarações (FATCA, GIIN, etc.)
- Múltiplos sócios (PF e PJ)
- Representante e INR

### Fundo - TipoImportacao: 2
- Dados do fundo
- Administrador
- Gestores (múltiplos)
- Representantes (múltiplos)
- Beneficiários finais (múltiplos)
- Conta bancária

## 🚀 Como Usar

### 1. Instalação

```bash
# Clonar o repositório
git clone <seu-repositorio>
cd cadastro_investidores

# Instalar dependências
pip install -r requirements.txt
```

### 2. Executar a Aplicação

```bash
streamlit run app.py
```

A aplicação será aberta automaticamente no seu navegador em `http://localhost:8501`

### 3. Usar a Aplicação

1. **Selecionar Tipo**: No painel esquerdo, escolha o tipo de cadastro
2. **Preencher Dados**: Clique na aba "Formulário" e preencha os campos
3. **Gerar JSON**: Vá para "Prévia JSON" e clique em "Gerar JSON"
4. **Visualizar**: Veja o JSON formatado
5. **Exportar**: Na aba "Download", baixe o arquivo JSON

## 📁 Estrutura do Projeto

```
cadastro_investidores/
├── app.py              # Aplicação principal (Streamlit)
├── schemas.py          # Definições dos modelos de dados
├── utils.py            # Funções reutilizáveis
├── requirements.txt    # Dependências Python
├── README.md          # Este arquivo
├── examples/          # Modelos JSON de referência
│   ├── modelo-importacao-JSON-PF-Distribuicao-Externa.json
│   ├── modelo-importacao-JSON-PJ-Distribuicao-Externa.json
│   └── modelo-importacao-JSON-Fundo-Distribuicao-Externa.json
└── .gitignore         # Arquivos ignorados pelo Git
```

## 🔧 Arquitetura

### `app.py`
- Interface Streamlit
- Gerenciamento de abas
- Renderização do formulário
- Botões de ação (Gerar JSON, Download)

### `schemas.py`
- Definição dos 3 schemas (PF, PJ, Fundo)
- Metadados dos campos (tipo, label, required)
- Seções aninhadas
- Arrays de objetos

### `utils.py`
- `render_field()`: Renderiza campos individuais
- `render_simple_fields()`: Renderiza campos simples em lote
- `render_nested_object()`: Renderiza objetos aninhados
- `render_array_section()`: Renderiza arrays dinâmicos
- `collect_form_data()`: Coleta todos os dados do formulário
- `build_json_output()`: Constrói JSON final
- `clean_empty_values()`: Remove valores vazios recursivamente
- `validate_required_fields()`: Valida campos obrigatórios

## 📊 Regras de Negócio Implementadas

1. ✅ **TipoImportacao Automático**: PF=1, Fundo=2, PJ=3
2. ✅ **Campo Dados**: Sempre um array com um único objeto
3. ✅ **Arrays Dinâmicos**: Adicionar/remover múltiplos registros
4. ✅ **Objetos Aninhados**: Renderizados como seções organizadas
5. ✅ **Tipos de Dados**: 
   - boolean → checkbox
   - date → date input (YYYY-MM-DD)
   - number → input numérico
   - string → input texto
6. ✅ **Campos Obrigatórios**: Destacados com `*`
7. ✅ **JSON Compatível**: 100% conforme os modelos
8. ✅ **Escalabilidade**: Fácil adicionar novos campos
9. ✅ **Sem Duplicação**: Funções reutilizáveis
10. ✅ **Código Limpo**: Modular e organizado

## 🎨 Recursos da Interface

- **Sidebar**: Seleção de tipo e botão de limpeza
- **Abas**: Formulário | Prévia JSON | Download
- **Expanders**: Seções organizáveis
- **Buttons Dinâmicos**: Adicionar/remover itens em arrays
- **Code Editor**: Exibição formatada do JSON
- **Métricas**: Tipo, TipoImportacao, Registros
- **Feedback Visual**: Caixas de sucesso/erro

## 🔐 Validação

- ✅ Campos obrigatórios validados antes de gerar JSON
- ✅ Valores vazios removidos automaticamente
- ✅ Datas formatadas corretamente (YYYY-MM-DD)
- ✅ Números validados
- ✅ Estrutura JSON mantida conforme schema

## 💡 Exemplos de Uso

### Exemplo 1: Cadastro Pessoa Física

```json
{
  "TipoImportacao": 1,
  "Dados": [
    {
      "NomeCompleto": "João Silva",
      "CPFInvestidor": "12345678900",
      "DataNascimento": "1990-05-15",
      "CNPJDistribuidor": "12345678000190",
      "Email": "joao@email.com",
      "Endereco": {
        "Rua": "Rua A",
        "Numero": 123,
        "Cidade": "São Paulo",
        "Uf": "SP"
      }
    }
  ]
}
```

### Exemplo 2: Múltiplas Contas Bancárias

Use o botão "➕ Adicionar Contas Bancárias" para criar múltiplas contas:

```json
{
  "ContaBancaria": [
    {
      "CodigoBanco": 1,
      "NumeroAgencia": "0001",
      "NumeroConta": "123456"
    },
    {
      "CodigoBanco": 237,
      "NumeroAgencia": "0002",
      "NumeroConta": "654321"
    }
  ]
}
```

## 🚀 Melhorias Futuras

- [ ] Validação avançada (CPF, CNPJ, CEP)
- [ ] Importação de JSON existentes
- [ ] Histórico de cadastros
- [ ] Exportação em múltiplos formatos
- [ ] Temas customizáveis
- [ ] Suporte a múltiplas línguas
- [ ] Integração com banco de dados
- [ ] API REST para integração

## 📝 Dependências

- **streamlit**: ^1.28.0 - Framework web para Python
- **python-dateutil**: ^2.8.2 - Utilitários de data
- **pydantic**: ^2.0.0 - Validação de dados

## 🛠️ Desenvolvimento

### Adicionar Novo Campo

1. Abra `schemas.py`
2. Localize o schema desejado (SCHEMA_PF, SCHEMA_PJ, ou SCHEMA_FUNDO)
3. Adicione o campo na seção apropriada:

```python
"NovoNome": {"type": "text", "required": True, "label": "Novo Campo"}
```

### Adicionar Novo Tipo de Cadastro

1. Crie um novo schema em `schemas.py`
2. Adicione à dicionário `SCHEMAS`
3. A aplicação reconhecerá automaticamente

## 📄 Licença

Este projeto é fornecido como-é para uso interno.

## 📧 Contato

Para dúvidas ou sugestões, entre em contato com a equipe de desenvolvimento.

---

**Versão**: 1.0  
**Data de Criação**: 2026-05-04  
**Status**: MVP Funcional ✅
