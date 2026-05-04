"""
Configurações da aplicação Cadastro de Investidores.
"""

# Configurações gerais
APP_NAME = "Cadastro de Investidores"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "MVP para cadastro dinâmico de investidores com geração automática de JSON"

# Configurações Streamlit
STREAMLIT_PAGE_TITLE = "Cadastro de Investidores"
STREAMLIT_PAGE_ICON = "💼"
STREAMLIT_LAYOUT = "wide"

# Configurações de validação
VALIDATE_REQUIRED_FIELDS = True
CLEAN_EMPTY_VALUES = True
REMOVE_ZERO_VALUES = True

# Configurações de formatação
JSON_INDENT = 2
DATE_FORMAT = "%Y-%m-%d"
ENSURE_ASCII = False

# Tipos de cadastro habilitados
ENABLED_TYPES = [
    "Pessoa Física",
    "Pessoa Jurídica",
    "Fundo",
]

# Campos obrigatórios por tipo
REQUIRED_FIELDS = {
    "Pessoa Física": [
        "NomeCompleto",
        "CPFInvestidor",
        "DataNascimento",
        "CNPJDistribuidor",
    ],
    "Pessoa Jurídica": [
        "RazaoSocial",
        "CNPJInvestidor",
        "CNPJDistribuidor",
    ],
    "Fundo": [
        "NomeFundo",
        "CNPJFundo",
        "DataConstituicao",
        "CNPJDistribuidor",
    ],
}

# Mapeamento de TipoImportacao
TIPO_IMPORTACAO_MAP = {
    "Pessoa Física": 1,
    "Pessoa Jurídica": 3,
    "Fundo": 2,
}

# Configurações de UI
UI_COLORS = {
    "primary": "#1f77b4",
    "success": "#2ca02c",
    "error": "#d62728",
    "warning": "#ff7f0e",
}

# Limites de arrays
MAX_ARRAY_ITEMS = None  # None = sem limite
MIN_ARRAY_ITEMS = 1
DEFAULT_ARRAY_ITEMS = 1

# Configurações de cache
ENABLE_CACHE = True
CACHE_TTL = 3600  # 1 hora em segundos

# Configurações de logging
ENABLE_LOGGING = True
LOG_LEVEL = "INFO"
LOG_FILE = "cadastro_investidores.log"
