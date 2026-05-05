"""
Funções utilitárias para renderização de formulários e geração de JSON.
"""

import streamlit as st
import json
from datetime import date
from typing import Any, Dict, List


def render_text_field(label: str, field_key: str, required: bool = False, placeholder: str = "") -> Any:
    """Renderiza um campo de texto."""
    kwargs = {
        "label": f"{label} {'*' if required else ''}",
        "key": field_key,
        "value": st.session_state.get(field_key, ""),
        "placeholder": placeholder,
    }
    return st.text_input(**kwargs)


def render_number_field(label: str, field_key: str, required: bool = False) -> Any:
    """Renderiza um campo numérico."""
    kwargs = {
        "label": f"{label} {'*' if required else ''}",
        "key": field_key,
        "value": st.session_state.get(field_key, 0),
    }
    return st.number_input(**kwargs)


def render_date_field(label: str, field_key: str, required: bool = False) -> Any:
    """Renderiza um campo de data."""
    current_value = st.session_state.get(field_key, None)
    if isinstance(current_value, str):
        try:
            current_value = date.fromisoformat(current_value)
        except:
            current_value = None
    
    kwargs = {
        "label": f"{label} {'*' if required else ''}",
        "key": field_key,
        "value": current_value,
    }
    return st.date_input(**kwargs)


def render_checkbox_field(label: str, field_key: str, required: bool = False) -> Any:
    """Renderiza um checkbox."""
    kwargs = {
        "label": f"{label} {'*' if required else ''}",
        "key": field_key,
        "value": st.session_state.get(field_key, False),
    }
    return st.checkbox(**kwargs)


def render_field(label: str, field_key: str, field_type: str, required: bool = False) -> Any:
    """Renderiza um campo baseado no tipo."""
    if field_type == "text":
        return render_text_field(label, field_key, required)
    elif field_type == "number":
        return render_number_field(label, field_key, required)
    elif field_type == "date":
        return render_date_field(label, field_key, required)
    elif field_type == "checkbox":
        return render_checkbox_field(label, field_key, required)
    else:
        return render_text_field(label, field_key, required)


def render_simple_fields(fields: Dict, field_prefix: str = "") -> Dict[str, Any]:
    """Renderiza campos simples (não-objeto)."""
    results = {}
    
    for field_name, field_config in fields.items():
        if isinstance(field_config, dict) and "type" in field_config:
            field_type = field_config.get("type", "text")
            
            # Pula campos tipo objeto ou array
            if field_type in ["object", "array"]:
                continue
            
            label = field_config.get("label", field_name)
            required = field_config.get("required", False)
            full_key = f"{field_prefix}_{field_name}" if field_prefix else field_name
            
            value = render_field(label, full_key, field_type, required)
            
            # Conversão de tipos
            if field_type == "date" and value:
                value = value.isoformat()
            elif field_type == "number":
                if value == 0 and not st.session_state.get(full_key, None):
                    value = None
            
            results[field_name] = value
    
    return results


def render_nested_object(
    section_name: str,
    fields: Dict,
    field_prefix: str = "",
    nesting_level: int = 0,
) -> Dict[str, Any]:
    """Renderiza um objeto aninhado evitando expanders dentro de expanders."""

    def _render_object_fields() -> Dict[str, Any]:
        results = {}
        for field_name, field_config in fields.items():
            if isinstance(field_config, dict):
                if field_config.get("type") == "object":
                    nested_fields = field_config.get("fields", {})
                    full_key = f"{field_prefix}_{field_name}" if field_prefix else field_name
                    results[field_name] = render_nested_object(
                        field_name,
                        nested_fields,
                        full_key,
                        nesting_level=nesting_level + 1,
                    )
                elif "type" in field_config and field_config["type"] not in ["object", "array"]:
                    field_type = field_config.get("type", "text")
                    label = field_config.get("label", field_name)
                    required = field_config.get("required", False)
                    full_key = f"{field_prefix}_{field_name}" if field_prefix else field_name

                    value = render_field(label, full_key, field_type, required)

                    if field_type == "date" and value:
                        value = value.isoformat()
                    elif field_type == "number":
                        if value == 0 and not st.session_state.get(full_key, None):
                            value = None

                    results[field_name] = value

        return results

    if nesting_level == 0:
        with st.expander(f"{section_name}", expanded=False):
            return _render_object_fields()

    st.markdown(f"**{section_name}**")
    with st.container():
        return _render_object_fields()


def render_array_section(section_name: str, fields: Dict, field_prefix: str = "") -> List[Dict[str, Any]]:
    """Renderiza uma seção com array de objetos com add/remove dinâmico."""
    # Inicializar array no session state
    array_key = f"array_{field_prefix}" if field_prefix else f"array_{section_name}"
    
    if array_key not in st.session_state:
        st.session_state[array_key] = [{}]
    
    st.markdown(f"### {section_name}")
    
    items = st.session_state[array_key]
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button(f"Adicionar {section_name}", key=f"add_{array_key}"):
            st.session_state[array_key].append({})
            st.rerun()
    
    with col2:
        if len(items) > 1:
            if st.button(f"Remover último {section_name}", key=f"remove_{array_key}"):
                st.session_state[array_key].pop()
                st.rerun()
    
    # Renderizar cada item do array
    results = []
    for idx, item in enumerate(items):
        with st.expander(f"{section_name} #{idx + 1}", expanded=(idx == 0)):
            item_data = {}
            
            for field_name, field_config in fields.items():
                if isinstance(field_config, dict) and "type" in field_config:
                    field_type = field_config.get("type", "text")
                    
                    if field_type == "object":
                        nested_fields = field_config.get("fields", {})
                        item_data[field_name] = render_nested_object(
                            field_name,
                            nested_fields,
                            f"{array_key}_{idx}",
                            nesting_level=1,
                        )
                    else:
                        label = field_config.get("label", field_name)
                        required = field_config.get("required", False)
                        full_key = f"{array_key}_{idx}_{field_name}"
                        
                        value = render_field(label, full_key, field_type, required)
                        
                        # Conversão de tipos
                        if field_type == "date" and value:
                            value = value.isoformat()
                        elif field_type == "number":
                            if value == 0 and not st.session_state.get(full_key, None):
                                value = None
                        
                        item_data[field_name] = value
            
            results.append(item_data)
    
    return results


def collect_form_data(schema: Dict) -> Dict[str, Any]:
    """Coleta todos os dados do formulário baseado no schema."""
    data = {}
    
    # Campos simples
    fields = schema.get("fields", {})
    data.update(render_simple_fields(fields))
    
    # Seções (objetos aninhados e arrays)
    sections = schema.get("sections", {})
    
    for section_name, section_config in sections.items():
        section_type = section_config.get("type", "object")
        
        if section_type == "array":
            field_config = section_config.get("fields", {})
            data[section_name] = render_array_section(section_name, field_config, section_name)
        else:
            field_config = section_config.get("fields", {})
            data[section_name] = render_nested_object(section_config.get("label", section_name), field_config, section_name)
    
    return data


def build_json_output(tipo_importacao: int, dados: Dict[str, Any]) -> Dict[str, Any]:
    """Constrói o JSON final com a estrutura correta."""
    # Limpeza de valores vazios
    dados_limpo = {}
    
    for key, value in dados.items():
        if value is None:
            continue
        elif isinstance(value, str) and value == "":
            continue
        elif isinstance(value, dict):
            # Limpar dicts vazios recursivamente
            cleaned = clean_empty_values(value)
            if cleaned:
                dados_limpo[key] = cleaned
        elif isinstance(value, list):
            # Limpar arrays vazios
            cleaned_list = [clean_empty_values(item) if isinstance(item, dict) else item for item in value]
            cleaned_list = [item for item in cleaned_list if item]
            if cleaned_list:
                dados_limpo[key] = cleaned_list
        else:
            dados_limpo[key] = value
    
    return {
        "TipoImportacao": tipo_importacao,
        "Dados": [dados_limpo]
    }


def clean_empty_values(obj: Any) -> Any:
    """Remove valores vazios recursivamente."""
    if isinstance(obj, dict):
        cleaned = {}
        for k, v in obj.items():
            if v is None or v == "" or v == 0:
                continue
            elif isinstance(v, dict):
                cleaned_v = clean_empty_values(v)
                if cleaned_v:
                    cleaned[k] = cleaned_v
            elif isinstance(v, list):
                cleaned_v = [clean_empty_values(item) if isinstance(item, dict) else item for item in v]
                cleaned_v = [item for item in cleaned_v if item not in [None, "", 0]]
                if cleaned_v:
                    cleaned[k] = cleaned_v
            else:
                cleaned[k] = v
        return cleaned
    return obj


def format_json_output(data: Dict) -> str:
    """Formata o JSON para exibição e download."""
    return json.dumps(data, indent=2, ensure_ascii=False)


def validate_required_fields(schema: Dict, data: Dict) -> tuple[bool, List[str]]:
    """Valida campos obrigatórios."""
    errors = []
    
    fields = schema.get("fields", {})
    for field_name, field_config in fields.items():
        if field_config.get("required", False):
            value = data.get(field_name)
            if value is None or value == "" or value == 0:
                label = field_config.get("label", field_name)
                errors.append(f"Campo obrigatório: {label}")
    
    return len(errors) == 0, errors
