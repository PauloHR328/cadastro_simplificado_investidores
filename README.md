# 💼 Cadastro de Investidores e Documentos Word

Uma aplicação Streamlit com dois fluxos isolados em abas:

- Cadastro dinâmico de investidores (Pessoa Física, Pessoa Jurídica e Fundos) com geração automática de JSON válido
- Geração em lote de documentos Word a partir de templates `.docx` com variáveis `{{ variavel }}`
- Geração em lote de PDFs editáveis a partir de templates `.pdf` com campos de formulário

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
✅ **Templates Word Dinâmicos**: Upload de `.docx`, extração automática de variáveis e formulário dinâmico  
✅ **Lote Manual de Documentos**: Adição e remoção de múltiplos registros sem uso de Excel  
✅ **Download Consolidado**: Geração de múltiplos `.docx` em um único `.zip`  
✅ **PDFs Editáveis**: Leitura de campos de formulário e preenchimento automático em lote  

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

#### Aba 1: Cadastro de Investidores

1. **Selecionar Tipo**: No painel esquerdo, escolha o tipo de cadastro
2. **Preencher Dados**: Clique na aba "Formulário" e preencha os campos
3. **Gerar JSON**: Vá para "Prévia JSON" e clique em "Gerar JSON"
4. **Visualizar**: Veja o JSON formatado
5. **Exportar**: Na aba "Download", baixe o arquivo JSON

#### Aba 2: Documentos Word em Lote

1. **Escolher origem do template**: Selecione um arquivo já salvo em `templates/` ou envie um `.docx` / `.pdf`
2. **Revisar variáveis**: Confira a lista de campos detectados automaticamente
3. **Adicionar registros**: Preencha o formulário dinâmico e clique em "Adicionar registro"
4. **Gerar documentos**: Clique em "Gerar documentos" para montar todos os arquivos
5. **Baixar o lote**: Faça o download do `.zip` com todos os documentos gerados

Observação:

- Para `.docx`, o template deve usar placeholders `{{ variavel }}`
- Para `.pdf`, o arquivo precisa ser editável e conter campos de formulário

### 4. Exemplo de uso do fluxo Word

Template:

```text
Contrato referente a {{ nome }}
CNPJ: {{ cnpj }}
Data de assinatura: {{ data_assinatura }}
```

Registros adicionados manualmente:

1. `nome = Empresa Alpha`, `cnpj = 12.345.678/0001-90`, `data_assinatura = 05/05/2026`
2. `nome = Empresa Beta`, `cnpj = 98.765.432/0001-10`, `data_assinatura = 06/05/2026`

Resultado:

- `2` documentos `.docx` gerados automaticamente
- `1` arquivo `.zip` disponível para download

## 📁 Estrutura do Projeto

```
cadastro_investidores/
├── app.py              # Aplicação principal (Streamlit)
├── schemas.py          # Definições dos modelos de dados
├── utils.py            # Funções reutilizáveis
├── requirements.txt    # Dependências Python
├── word_template_utils.py  # Utilitários do fluxo de documentos Word
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

### `word_template_utils.py`
- `extract_template_variables()`: Lê o `.docx` e encontra placeholders únicos
- `extract_pdf_form_fields()`: Lê os campos de um PDF editável
- `extract_template_fields()`: Escolhe a estratégia correta para `.docx` ou `.pdf`
- `normalize_record()`: Normaliza os valores informados antes da geração
- `render_document()`: Preenche um template Word com os dados do registro
- `render_pdf_document()`: Preenche um PDF editável com os dados do registro
- `generate_documents_zip()`: Gera múltiplos `.docx` ou `.pdf` e compacta tudo em `.zip`

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
- **Abas principais**: Cadastro de Investidores | Documentos Word em Lote
- **Abas internas do cadastro**: Formulário | Prévia JSON | Download
- **Expanders**: Seções organizáveis
- **Buttons Dinâmicos**: Adicionar/remover itens em arrays
- **Code Editor**: Exibição formatada do JSON
- **Métricas**: Tipo, TipoImportacao, Registros
- **Feedback Visual**: Caixas de sucesso/erro
- **Formulário dinâmico Word**: Inputs gerados a partir das variáveis do template
- **Formulário dinâmico PDF**: Inputs gerados a partir dos campos do formulário editável
- **Lista de registros**: Remoção individual e geração em lote

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
- **docxtpl**: Preenchimento de templates `.docx`
- **python-docx**: Leitura de conteúdo e estrutura de documentos Word
- **pypdf**: Leitura e preenchimento de formulários PDF editáveis

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
