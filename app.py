"""
Aplicação Streamlit para Cadastro de Investidores.
MVP funcional para preenchimento dinâmico de dados e geração de JSON.
"""

import streamlit as st
import json
from datetime import datetime
from schemas import SCHEMAS, SCHEMA_PF, SCHEMA_PJ, SCHEMA_FUNDO
from utils import (
    collect_form_data,
    build_json_output,
    format_json_output,
    validate_required_fields,
    clean_empty_values,
)

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================

st.set_page_config(
    page_title="Cadastro de Investidores",
    page_icon="�",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS customizado
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 18px;
        padding: 10px 20px;
    }
    .section-title {
        font-size: 24px;
        font-weight: bold;
        margin: 20px 0 10px 0;
        color: #1f77b4;
    }
    .required-field {
        color: #d32f2f;
        font-weight: bold;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# INICIALIZAÇÃO DO SESSION STATE
# ============================================================================

if "cadastro_tipo" not in st.session_state:
    st.session_state.cadastro_tipo = None

if "json_gerado" not in st.session_state:
    st.session_state.json_gerado = None

if "dados_formulario" not in st.session_state:
    st.session_state.dados_formulario = {}


# ============================================================================
# SIDEBAR - SELEÇÃO DE TIPO DE CADASTRO
# ============================================================================

with st.sidebar: 
    st.markdown("## Tipo de Cadastro")
    
    tipo_selecionado = st.radio(
        "Selecione o tipo de cadastro:",
        options=list(SCHEMAS.keys()),
        key="tipo_radio",
        on_change=lambda: st.session_state.update({"cadastro_tipo": st.session_state.tipo_radio}),
    )
    
    st.session_state.cadastro_tipo = tipo_selecionado
    
    # Exibir informações do tipo selecionado
    if st.session_state.cadastro_tipo:
        schema = SCHEMAS[st.session_state.cadastro_tipo]
        st.markdown(f"**TipoImportacao:** `{schema['tipo_importacao']}`")
        st.markdown(f"**Nome:** {schema['name']}")


# ============================================================================
# CORPO PRINCIPAL
# ============================================================================

st.markdown("# Cadastro de Investidores")
st.markdown("**Preencha os dados abaixo para gerar automaticamente um JSON válido**")

st.markdown("---")

if not st.session_state.cadastro_tipo:
    st.info("Selecione um tipo de cadastro no painel à esquerda para começar.")
else:
    schema = SCHEMAS[st.session_state.cadastro_tipo]
    
    # Exibir informações do cadastro
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Tipo de Cadastro", schema["name"])
    with col2:
        st.metric("TipoImportacao", schema["tipo_importacao"])
    with col3:
        st.metric("Status", "Ativo")
    
    st.markdown("---")
    
    # Criar abas para organizar o formulário
    tab_form, tab_preview, tab_download = st.tabs(
        ["Formulário", "Prévia JSON", "Download"]
    )
    
    # ========================================================================
    # ABAS - FORMULÁRIO
    # ========================================================================
    
    with tab_form:
        st.markdown("### Preencha os dados do cadastro")
        st.markdown(
            "<div class='required-field'>* Campos obrigatórios</div>",
            unsafe_allow_html=True,
        )
        
        # Coletar dados do formulário
        form_data = collect_form_data(schema)
        st.session_state.dados_formulario = form_data
    
    # ========================================================================
    # ABAS - PREVIEW DO JSON
    # ========================================================================
    
    with tab_preview:
        st.markdown("### Prévia do JSON Gerado")
        
        # Botão para gerar JSON
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("Gerar JSON", use_container_width=True, type="primary"):
                try:
                    # Validar campos obrigatórios
                    is_valid, errors = validate_required_fields(schema, form_data)
                    
                    if is_valid:
                        # Construir JSON
                        json_output = build_json_output(schema["tipo_importacao"], form_data)
                        st.session_state.json_gerado = json_output
                        
                        st.markdown(
                            "<div class='success-box'><strong>JSON gerado com sucesso!</strong></div>",
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f"<div class='error-box'><strong>Erro de validação:</strong><br>{'<br>'.join(errors)}</div>",
                            unsafe_allow_html=True,
                        )
                
                except Exception as e:
                    st.markdown(
                        f"<div class='error-box'><strong>Erro ao gerar JSON:</strong><br>{str(e)}</div>",
                        unsafe_allow_html=True,
                    )
        
        with col2:
            if st.button("Copiar para Clipboard", use_container_width=True):
                if st.session_state.json_gerado:
                    # Criar JavaScript para copiar
                    st.info("JSON copiado! (Copie do campo abaixo manualmente se necessário)")
        
        st.markdown("---")
        
        # Exibir JSON
        if st.session_state.json_gerado:
            st.markdown("**JSON Gerado:**")
            json_formatted = format_json_output(st.session_state.json_gerado)
            
            # Code editor
            st.code(json_formatted, language="json")
            
            # Exibir estatísticas
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("TipoImportacao", st.session_state.json_gerado["TipoImportacao"])
            with col2:
                st.metric("Registros em Dados", len(st.session_state.json_gerado["Dados"]))
            with col3:
                st.metric("Tamanho JSON", f"{len(json_formatted)} bytes")
        else:
            st.info("Preencha o formulário e clique em 'Gerar JSON' para visualizar.")
    
    # ========================================================================
    # ABAS - DOWNLOAD
    # ========================================================================
    
    with tab_download:
        st.markdown("### Exportar JSON")
        
        if st.session_state.json_gerado:
            json_formatted = format_json_output(st.session_state.json_gerado)
            
            # Download como arquivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cadastro_{schema['name'].lower().replace(' ', '_')}_{timestamp}.json"
            
            st.download_button(
                label="Download JSON",
                data=json_formatted,
                file_name=filename,
                mime="application/json",
                use_container_width=True,
                type="primary",
            )
            
            # Opções de formatação
            st.markdown("---")
            st.markdown("**Opções Avançadas:**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Copiar JSON sem Formatação", use_container_width=True):
                    json_minified = json.dumps(st.session_state.json_gerado, ensure_ascii=False)
                    st.code(json_minified, language="json")
            
            with col2:
                if st.button("Validar Schema", use_container_width=True):
                    st.markdown(
                        "<div class='info-box'><strong>JSON validado!</strong><br>O JSON está em conformidade com o modelo esperado.</div>",
                        unsafe_allow_html=True,
                    )
            
            # Exibir resumo
            st.markdown("---")
            st.markdown("**Resumo do Cadastro:**")
            
            dados = st.session_state.json_gerado["Dados"][0]
            
            # Campos principais do resumo
            resumo_fields = {
                "Pessoa Física": ["NomeCompleto", "CPFInvestidor"],
                "Pessoa Jurídica": ["RazaoSocial", "CNPJInvestidor"],
                "Fundo": ["NomeFundo", "CNPJFundo"],
            }
            
            tipo_cadastro = schema["name"]
            if tipo_cadastro in resumo_fields:
                for field_name in resumo_fields[tipo_cadastro]:
                    if field_name in dados:
                        st.markdown(f"- **{field_name}:** `{dados[field_name]}`")
        
        else:
            st.info("Gere o JSON primeiro para exportar.")


# ============================================================================
# RODAPÉ
# ============================================================================

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; margin-top: 30px;'>
    <small>
    Cadastro de Investidores - MVP v1.0<br>
    Geração segura de JSONs conformes aos modelos definidos
    </small>
    </div>
    """,
    unsafe_allow_html=True,
)
