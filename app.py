"""
Aplicação Streamlit para cadastro de investidores e geração de documentos Word.
"""

import json
from datetime import date, datetime
from pathlib import Path

import streamlit as st

from schemas import SCHEMAS
from utils import (
    build_json_output,
    collect_form_data,
    format_json_output,
    validate_required_fields,
)
from word_template_utils import (
    build_download_zip_name,
    detect_template_kind,
    extract_template_fields,
    format_variable_label,
    generate_documents_zip,
    is_date_variable,
    normalize_record,
    summarize_record,
)


TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"


def initialize_session_state() -> None:
    """Inicializa as chaves usadas pela aplicação."""
    defaults = {
        "cadastro_tipo": None,
        "json_gerado": None,
        "dados_formulario": {},
        "word_template_signature": None,
        "word_template_name": None,
        "word_variables": [],
        "word_variable_types": {},
        "word_records": [],
        "word_generated_zip": None,
        "word_generated_files": [],
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_word_generation_state() -> None:
    """Limpa resultados gerados para evitar download de arquivos defasados."""
    st.session_state.word_generated_zip = None
    st.session_state.word_generated_files = []


def setup_page() -> None:
    """Configura página e estilos compartilhados."""
    st.set_page_config(
        page_title="Cadastro de Investidores",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
        .main {
            padding-top: 2rem;
        }
        .stTabs [data-baseweb="tab-list"] button {
            font-size: 18px;
            padding: 10px 20px;
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
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    """Mantém o fluxo atual de seleção do cadastro na sidebar."""
    with st.sidebar:
        st.markdown("## Tipo de Cadastro")
        st.caption("Esta seleção afeta apenas a aba Cadastro de Investidores.")

        tipo_selecionado = st.radio(
            "Selecione o tipo de cadastro:",
            options=list(SCHEMAS.keys()),
            key="tipo_radio",
            on_change=lambda: st.session_state.update(
                {"cadastro_tipo": st.session_state.tipo_radio}
            ),
        )

        st.session_state.cadastro_tipo = tipo_selecionado

        if st.session_state.cadastro_tipo:
            schema = SCHEMAS[st.session_state.cadastro_tipo]
            st.markdown(f"**TipoImportacao:** `{schema['tipo_importacao']}`")
            st.markdown(f"**Nome:** {schema['name']}")


def render_investor_registration_tab() -> None:
    """Renderiza o fluxo existente de cadastro e geração de JSON."""
    st.markdown("## Cadastro de Investidores")
    st.markdown(
        "**Preencha os dados abaixo para gerar automaticamente um JSON válido**"
    )
    st.markdown("---")

    if not st.session_state.cadastro_tipo:
        st.info("Selecione um tipo de cadastro no painel à esquerda para começar.")
        return

    schema = SCHEMAS[st.session_state.cadastro_tipo]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Tipo de Cadastro", schema["name"])
    with col2:
        st.metric("TipoImportacao", schema["tipo_importacao"])
    with col3:
        st.metric("Status", "Ativo")

    st.markdown("---")

    tab_form, tab_preview, tab_download = st.tabs(
        ["Formulário", "Prévia JSON", "Download"]
    )

    with tab_form:
        st.markdown("### Preencha os dados do cadastro")
        st.markdown(
            "<div class='required-field'>* Campos obrigatórios</div>",
            unsafe_allow_html=True,
        )

        form_data = collect_form_data(schema)
        st.session_state.dados_formulario = form_data

    with tab_preview:
        st.markdown("### Prévia do JSON Gerado")

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Gerar JSON", use_container_width=True, type="primary"):
                try:
                    is_valid, errors = validate_required_fields(schema, form_data)

                    if is_valid:
                        json_output = build_json_output(
                            schema["tipo_importacao"], form_data
                        )
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
                except Exception as exc:
                    st.markdown(
                        f"<div class='error-box'><strong>Erro ao gerar JSON:</strong><br>{exc}</div>",
                        unsafe_allow_html=True,
                    )

        with col2:
            if st.button("Copiar para Clipboard", use_container_width=True):
                if st.session_state.json_gerado:
                    st.info("JSON copiado! Copie do campo abaixo manualmente se necessário.")

        st.markdown("---")

        if st.session_state.json_gerado:
            st.markdown("**JSON Gerado:**")
            json_formatted = format_json_output(st.session_state.json_gerado)
            st.code(json_formatted, language="json")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    "TipoImportacao", st.session_state.json_gerado["TipoImportacao"]
                )
            with col2:
                st.metric("Registros em Dados", len(st.session_state.json_gerado["Dados"]))
            with col3:
                st.metric("Tamanho JSON", f"{len(json_formatted)} bytes")
        else:
            st.info("Preencha o formulário e clique em 'Gerar JSON' para visualizar.")

    with tab_download:
        st.markdown("### Exportar JSON")

        if not st.session_state.json_gerado:
            st.info("Gere o JSON primeiro para exportar.")
            return

        json_formatted = format_json_output(st.session_state.json_gerado)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = (
            f"cadastro_{schema['name'].lower().replace(' ', '_')}_{timestamp}.json"
        )

        st.download_button(
            label="Download JSON",
            data=json_formatted,
            file_name=filename,
            mime="application/json",
            use_container_width=True,
            type="primary",
        )

        st.markdown("---")
        st.markdown("**Opções Avançadas:**")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Copiar JSON sem Formatação", use_container_width=True):
                json_minified = json.dumps(
                    st.session_state.json_gerado, ensure_ascii=False
                )
                st.code(json_minified, language="json")

        with col2:
            if st.button("Validar Schema", use_container_width=True):
                st.markdown(
                    "<div class='info-box'><strong>JSON validado!</strong><br>O JSON está em conformidade com o modelo esperado.</div>",
                    unsafe_allow_html=True,
                )

        st.markdown("---")
        st.markdown("**Resumo do Cadastro:**")

        dados = st.session_state.json_gerado["Dados"][0]
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


def render_word_documents_tab() -> None:
    """Renderiza o fluxo de geração de documentos em lote."""
    st.markdown("## Geração de Documentos Word e PDF")
    st.markdown(
        "Selecione um template salvo em `templates/` ou envie um `.docx` ou `.pdf` editável. "
        "Para Word, o template deve usar variáveis no formato `{{ variavel }}`. "
        "Para PDF, os campos serão lidos diretamente do formulário editável."
    )

    template_mode = st.radio(
        "Origem do template",
        options=["Selecionar template salvo", "Fazer upload de template"],
        horizontal=True,
        key="word_template_mode",
    )

    template_name = None
    template_bytes = None

    if template_mode == "Selecionar template salvo":
        saved_templates = sorted(
            [
                *TEMPLATES_DIR.glob("*.docx"),
                *TEMPLATES_DIR.glob("*.pdf"),
            ]
        )
        if not saved_templates:
            st.warning(
                "Nenhum template `.docx` ou `.pdf` foi encontrado na pasta `templates/`. "
                "Adicione arquivos lá ou use o modo de upload."
            )
            return

        template_options = {
            template_path.name: template_path for template_path in saved_templates
        }
        selected_template_name = st.selectbox(
            "Template salvo",
            options=list(template_options.keys()),
            key="saved_template_select",
        )
        selected_template_path = template_options[selected_template_name]

        try:
            template_bytes = selected_template_path.read_bytes()
            template_name = selected_template_path.name
        except OSError as exc:
            st.error(f"Não foi possível ler o template selecionado. Detalhes: {exc}")
            return
    else:
        uploaded_template = st.file_uploader(
            "Upload do template",
            type=["docx", "pdf"],
            help="Envie um `.docx` com placeholders ou um `.pdf` editável com campos de formulário.",
            key="word_template_uploader",
        )

        if not uploaded_template:
            st.info(
                "Faça upload de um template `.docx` ou `.pdf` editável para montar os registros."
            )
            return

        template_bytes = uploaded_template.getvalue()
        template_name = uploaded_template.name

        if not template_bytes:
            st.error("Não foi possível ler o arquivo enviado. Tente novamente com outro `.docx`.")
            return

    template_signature = f"{template_mode}:{template_name}:{len(template_bytes)}"
    if st.session_state.word_template_signature != template_signature:
        st.session_state.word_template_signature = template_signature
        st.session_state.word_template_name = template_name
        st.session_state.word_records = []
        st.session_state.word_variables = []
        st.session_state.word_variable_types = {}
        reset_word_generation_state()

    try:
        template_kind = detect_template_kind(template_name)
        variables = extract_template_fields(template_bytes, template_name)
    except Exception as exc:
        st.error(
            "Não foi possível processar o template enviado. "
            f"Verifique se o arquivo é um `.docx` válido ou um `.pdf` editável. Detalhes: {exc}"
        )
        return

    if not variables:
        if template_kind == "word":
            st.warning(
                "Nenhuma variável foi encontrada no template. Use placeholders no formato `{{ variavel }}`."
            )
        else:
            st.warning(
                "Nenhum campo editável foi encontrado no PDF. Este fluxo funciona apenas com PDFs que tenham formulário."
            )
        return

    st.session_state.word_variables = variables

    for variable in variables:
        st.session_state.word_variable_types.setdefault(
            variable,
            "data" if is_date_variable(variable) else "texto",
        )

    stale_variables = set(st.session_state.word_variable_types) - set(variables)
    for stale_variable in stale_variables:
        del st.session_state.word_variable_types[stale_variable]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Template carregado", Path(template_name).name)
    with col2:
        st.metric("Campos detectados", len(variables))
    with col3:
        st.metric("Registros adicionados", len(st.session_state.word_records))

    st.markdown("### Campos detectados")
    if template_kind == "word":
        st.caption("Você pode ajustar o tipo de cada variável antes de preencher os registros.")
    else:
        st.caption("Os campos foram lidos do formulário do PDF. Você pode ajustar o tipo para facilitar o preenchimento.")
    for variable in variables:
        col_label, col_type = st.columns([2, 1])
        with col_label:
            st.text_input(
                "Variável detectada",
                value=variable,
                disabled=True,
                key=f"word_variable_label_{variable}",
            )
        with col_type:
            selected_type = st.selectbox(
                "Tipo",
                options=["texto", "data"],
                index=0 if st.session_state.word_variable_types[variable] == "texto" else 1,
                key=f"word_variable_type_{variable}",
            )
            st.session_state.word_variable_types[variable] = selected_type

    st.markdown("### Adicionar registro")
    with st.form("word_record_form", clear_on_submit=True):
        new_record = {}
        for variable in variables:
            label = format_variable_label(variable)
            field_key = f"word_input_{variable}"

            if st.session_state.word_variable_types.get(variable) == "data":
                new_record[variable] = st.date_input(
                    label,
                    value=None,
                    min_value=date(1900, 1, 1),
                    max_value=date(2100, 12, 31),
                    key=field_key,
                )
            else:
                new_record[variable] = st.text_input(label, key=field_key)

        add_record = st.form_submit_button(
            "Adicionar registro",
            type="primary",
            use_container_width=True,
        )

    if add_record:
        normalized_record = normalize_record(new_record, variables)
        st.session_state.word_records.append(normalized_record)
        reset_word_generation_state()
        st.success("Registro adicionado à lista com sucesso.")
        st.rerun()

    st.markdown("### Registros adicionados")
    if not st.session_state.word_records:
        st.info("Nenhum registro foi adicionado ainda.")
    else:
        st.dataframe(st.session_state.word_records, use_container_width=True)

        for index, record in enumerate(st.session_state.word_records, start=1):
            with st.expander(f"Registro {index}: {summarize_record(record)}"):
                st.json(record)
                if st.button(
                    "Remover registro",
                    key=f"remove_word_record_{index}",
                    use_container_width=True,
                ):
                    st.session_state.word_records.pop(index - 1)
                    reset_word_generation_state()
                    st.rerun()

    st.markdown("### Gerar documentos")
    if not st.session_state.word_records:
        st.info("Adicione ao menos um registro para habilitar a geração dos documentos.")
        return

    if st.button("Gerar documentos", type="primary", use_container_width=True):
        try:
            zip_bytes, generated_files = generate_documents_zip(
                template_bytes=template_bytes,
                template_name=template_name,
                variables=variables,
                records=st.session_state.word_records,
            )
            st.session_state.word_generated_zip = zip_bytes
            st.session_state.word_generated_files = generated_files
            st.success(
                f"{len(generated_files)} documento(s) gerado(s) com sucesso."
            )
        except Exception as exc:
            st.error(f"Erro ao gerar os documentos: {exc}")

    if st.session_state.word_generated_zip:
        download_name = build_download_zip_name(template_name)
        st.download_button(
            label="Download do pacote ZIP",
            data=st.session_state.word_generated_zip,
            file_name=download_name,
            mime="application/zip",
            use_container_width=True,
        )

        st.markdown("**Arquivos prontos para download:**")
        for generated_file in st.session_state.word_generated_files:
            st.markdown(f"- `{generated_file}`")


def render_footer() -> None:
    """Renderiza o rodapé da aplicação."""
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; margin-top: 30px;'>
        <small>
        Cadastro de Investidores - MVP v1.1<br>
        Fluxos separados em abas para JSON e documentos Word
        </small>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    """Ponto de entrada da aplicação."""
    setup_page()
    initialize_session_state()
    render_sidebar()

    st.markdown("# Cadastro de Investidores")
    st.caption("A aplicação agora inclui uma aba isolada para automação de documentos Word.")

    tab_investidores, tab_word = st.tabs(
        ["Cadastro de Investidores", "Documentos Word em Lote"]
    )

    with tab_investidores:
        render_investor_registration_tab()

    with tab_word:
        render_word_documents_tab()

    render_footer()


if __name__ == "__main__":
    main()
