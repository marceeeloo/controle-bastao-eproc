# ============================================
# CONTROLE DE BASTÃO Informática 2026
# Versão: Completa sem Integrações Externas
# ============================================
import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta, date, time as dt_time
from operator import itemgetter
from streamlit_autorefresh import st_autorefresh
import random
import base64
import os

import json
from pathlib import Path

# Arquivo de persistência
STATE_FILE = Path("bastao_state.json")

# --- Constantes de Colaboradores ---
COLABORADORES = sorted([
    "Frederico Augusto Costa Gonçalves",
    "Ramon Shander de Almeida",
    "Marcelo Batista Amaral",
    "Rodrigo Marinho Marques", 
    "Otávio Reis",
    "Judson Heleno Faleiro",
    "Roner Ribeiro Júnior",
    "Warley Roberto de Oliveira Cruz",
    "Marcio Rodrigues Alves",
    "Igor Eduardo Martins",
    "Leonardo goncalves fleury",
    "Marcelo dos Santos Dutra",
    "Daniely Cristina Cunha Mesquita",
    "Celso Daniel Vilano Cardoso",
    "Pollyanna Silva Pereira",
    "Cinthia Mery Facion"
])

# --- Constantes de Opções ---
REG_USUARIO_OPCOES = ["Cartório", "Externo"]
REG_SISTEMA_OPCOES = ["Conveniados", "Outros", "Eproc", "Themis", "JPE", "SIAP"]
REG_CANAL_OPCOES = ["Presencial", "Telefone", "Email", "Whatsapp", "Outros"]
REG_DESFECHO_OPCOES = ["Resolvido - Informática", "Escalonado"]


# Emoji do Bastão
BASTAO_EMOJI = "🥂"

# ============================================
# FUNÇÕES AUXILIARES
# ============================================


def save_state():
    """Salva estado atual em JSON"""
    try:
        data = {
            'bastao_queue': st.session_state.bastao_queue,
            'status_texto': st.session_state.status_texto,
            'bastao_start_time': st.session_state.bastao_start_time.isoformat() if st.session_state.bastao_start_time else None,
            'bastao_counts': st.session_state.bastao_counts,
            'simon_ranking': st.session_state.simon_ranking,
            'daily_logs': st.session_state.daily_logs,
            'checks': {nome: st.session_state.get(f'check_{nome}', False) for nome in COLABORADORES}
        }
        STATE_FILE.write_text(json.dumps(data, default=str, ensure_ascii=False, indent=2))
    except:
        pass

def load_state():
    """Carrega estado do JSON"""
    try:
        if STATE_FILE.exists():
            data = json.loads(STATE_FILE.read_text())
            st.session_state.bastao_queue = data.get('bastao_queue', [])
            st.session_state.status_texto = data.get('status_texto', {nome: 'Indisponível' for nome in COLABORADORES})
            
            time_str = data.get('bastao_start_time')
            st.session_state.bastao_start_time = datetime.fromisoformat(time_str) if time_str else None
            
            st.session_state.bastao_counts = data.get('bastao_counts', {nome: 0 for nome in COLABORADORES})
            st.session_state.simon_ranking = data.get('simon_ranking', [])
            st.session_state.daily_logs = data.get('daily_logs', [])
            
            for nome, val in data.get('checks', {}).items():
                st.session_state[f'check_{nome}'] = val
            return True
    except:
        pass
    return False



def apply_modern_styles():
    """Aplica design profissional moderno"""
    st.markdown("""<style>
    /* Importar fonte moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Reset e Base */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    .main {
        background: #f1f5f9 !important;
        padding: 1.5rem !important;
    }
    
    /* Container principal */
    .block-container {
        max-width: 1400px !important;
        padding: 1rem !important;
    }
    
    /* Remover header padrão Streamlit */
    header {
        background: transparent !important;
    }
    
    /* Botões modernos */
    .stButton > button {
        background: white !important;
        color: #0f172a !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        transition: all 0.15s ease !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
    }
    
    .stButton > button:hover {
        background: #f8fafc !important;
        border-color: #cbd5e1 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08) !important;
        transform: translateY(-1px) !important;
    }
    
    .stButton > button[kind="primary"] {
        background: #2563eb !important;
        color: white !important;
        border-color: #2563eb !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: #1d4ed8 !important;
        border-color: #1d4ed8 !important;
    }
    
    /* Inputs */
    .stSelectbox > div > div,
    .stTextInput > div > div,
    .stTextArea > div > div {
        border-radius: 10px !important;
        border: 1px solid #e2e8f0 !important;
        background: white !important;
        font-size: 0.875rem !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #cbd5e1 !important;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #0f172a !important;
        font-weight: 600 !important;
    }
    
    h1 {
        font-size: 1.75rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        font-size: 1.25rem !important;
        margin-bottom: 0.75rem !important;
    }
    
    h3 {
        font-size: 1.1rem !important;
        margin-bottom: 0.5rem !important;
        color: #475569 !important;
    }
    
    /* Alertas */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 10px !important;
        border: 1px solid !important;
        padding: 0.875rem !important;
        font-size: 0.875rem !important;
    }
    
    .stSuccess {
        background: #f0fdf4 !important;
        border-color: #bbf7d0 !important;
        color: #166534 !important;
    }
    
    .stError {
        background: #fef2f2 !important;
        border-color: #fecaca !important;
        color: #991b1b !important;
    }
    
    .stWarning {
        background: #fefce8 !important;
        border-color: #fef08a !important;
        color: #854d0e !important;
    }
    
    .stInfo {
        background: #eff6ff !important;
        border-color: #bfdbfe !important;
        color: #1e40af !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: white !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        padding: 0.875rem !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: #f8fafc !important;
        border-color: #cbd5e1 !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: white !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    
    /* Métricas */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: #0f172a !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem !important;
        color: #64748b !important;
        font-weight: 500 !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
    
    /* Divisor */
    hr {
        border: none !important;
        height: 1px !important;
        background: #e2e8f0 !important;
        margin: 1.5rem 0 !important;
    }
    
    /* Tabelas */
    .dataframe {
        font-size: 0.875rem !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }
    
    .dataframe thead th {
        background: #f8fafc !important;
        color: #0f172a !important;
        font-weight: 600 !important;
        padding: 0.75rem !important;
        border-bottom: 2px solid #e2e8f0 !important;
    }
    
    .dataframe tbody td {
        padding: 0.75rem !important;
        border-bottom: 1px solid #f1f5f9 !important;
    }
    
    /* Checkbox */
    .stCheckbox {
        font-size: 0.875rem !important;
    }
    
    /* Remover elementos desnecessários */
    .stDeployButton {
        display: none !important;
    }
    
    button[title="View fullscreen"] {
        display: none !important;
    }
    
    /* Responsivo */
    @media (max-width: 768px) {
        .block-container {
            padding: 0.5rem !important;
        }
    }
    </style>""", unsafe_allow_html=True)

def format_time_duration(duration):
    if not isinstance(duration, timedelta): return '--:--:--'
    s = int(duration.total_seconds())
    h, s = divmod(s, 3600)
    m, s = divmod(s, 60)
    return f'{h:02}:{m:02}:{s:02}'

def init_session_state():
    """Inicializa o estado da sessão"""
    # Se já foi inicializado, não fazer nada
    if 'initialized' in st.session_state:
        return
    
    # Marcar como inicializado
    st.session_state.initialized = True
    
    # Lista de todos os campos necessários com valores padrão
    defaults = {
        'bastao_queue': [],
        'status_texto': {nome: 'Indisponível' for nome in COLABORADORES},
        'bastao_start_time': None,
        'bastao_counts': {nome: 0 for nome in COLABORADORES},
        'active_view': None,
        'chamado_guide_step': 0,
        'simon_sequence': [],
        'simon_user_input': [],
        'simon_status': 'start',
        'simon_level': 1,
        'simon_ranking': [],
        'daily_logs': [],
        'success_message': None,
        'success_message_time': None,
    }
    
    # Tentar carregar estado salvo
    loaded = load_state()
    
    # Inicializar TODOS os campos (mesmo que tenha carregado do JSON)
    for key, default in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default
    
    # Inicializar checkboxes
    for nome in COLABORADORES:
        if f'check_{nome}' not in st.session_state:
            st.session_state[f'check_{nome}'] = False

def find_next_holder_index(current_index, queue):
    if not queue: return -1
    num_colab = len(queue)
    if num_colab == 0: return -1
    next_idx = (current_index + 1) % num_colab
    attempts = 0
    while attempts < num_colab:
        colaborador = queue[next_idx]
        if st.session_state.get(f'check_{colaborador}'): return next_idx
        next_idx = (next_idx + 1) % num_colab
        attempts += 1
    return -1

def check_and_assume_baton():
    queue = st.session_state.bastao_queue
    current_holder = next((c for c, s in st.session_state.status_texto.items() if 'Bastão' in s), None)
    is_current_valid = (current_holder and current_holder in queue and st.session_state.get(f'check_{current_holder}'))
    first_eligible_index = find_next_holder_index(-1, queue)
    first_eligible_holder = queue[first_eligible_index] if first_eligible_index != -1 else None
    
    should_have_baton = None
    if is_current_valid: should_have_baton = current_holder
    elif first_eligible_holder: should_have_baton = first_eligible_holder

    changed = False
    for c in COLABORADORES:
        s_text = st.session_state.status_texto.get(c, '')
        if c != should_have_baton and 'Bastão' in s_text:
            st.session_state.status_texto[c] = 'Indisponível'
            changed = True

    if should_have_baton:
        s_current = st.session_state.status_texto.get(should_have_baton, '')
        if 'Bastão' not in s_current:
            old_status = s_current
            new_status = f"Bastão | {old_status}" if old_status and old_status != "Indisponível" else "Bastão"
            st.session_state.status_texto[should_have_baton] = new_status
            st.session_state.bastao_start_time = datetime.now()
            changed = True
    elif not should_have_baton:
        if current_holder:
            st.session_state.status_texto[current_holder] = 'Indisponível'
            changed = True
        st.session_state.bastao_start_time = None

    return changed

def toggle_queue(colaborador):
    
    if colaborador in st.session_state.bastao_queue:
        st.session_state.bastao_queue.remove(colaborador)
        st.session_state[f'check_{colaborador}'] = False
        current_s = st.session_state.status_texto.get(colaborador, '')
        if current_s == '' or current_s == 'Bastão':
            st.session_state.status_texto[colaborador] = 'Indisponível'
    else:
        st.session_state.bastao_queue.append(colaborador)
        st.session_state[f'check_{colaborador}'] = True
        current_s = st.session_state.status_texto.get(colaborador, 'Indisponível')
        if current_s == 'Indisponível':
            st.session_state.status_texto[colaborador] = ''

    check_and_assume_baton()

def rotate_bastao():
    """Passa o bastão para o próximo colaborador"""
    
    # Verificar quem está selecionado
    selected = st.session_state.get('colaborador_selectbox')
    
    queue = st.session_state.bastao_queue
    current_holder = next((c for c, s in st.session_state.status_texto.items() if 'Bastão' in s), None)
    
    if not current_holder:
        st.warning('⚠️ Ninguém tem o bastão no momento.')
        return
    
    # VALIDAÇÃO: só quem tem o bastão pode passar
    if selected != current_holder:
        st.error(f'❌ Somente **{current_holder}** pode passar o bastão!')
        st.info(f'💡 Selecione "{current_holder}" no menu acima para passar o bastão.')
        return
    
    if not queue or current_holder not in queue:
        st.warning('⚠️ O detentor do bastão não está na fila.')
        check_and_assume_baton()
        return

    try:
        current_index = queue.index(current_holder)
    except ValueError:
        check_and_assume_baton()
        return

    next_idx = find_next_holder_index(current_index, queue)
    
    if next_idx != -1:
        next_holder = queue[next_idx]
        
        old_h_status = st.session_state.status_texto[current_holder]
        new_h_status = old_h_status.replace('Bastão | ', '').replace('Bastão', '').strip()
        if not new_h_status: new_h_status = ''
        st.session_state.status_texto[current_holder] = new_h_status
        
        old_n_status = st.session_state.status_texto.get(next_holder, '')
        new_n_status = f"Bastão | {old_n_status}" if old_n_status else "Bastão"
        st.session_state.status_texto[next_holder] = new_n_status
        st.session_state.bastao_start_time = datetime.now()
        
        st.session_state.bastao_counts[current_holder] = st.session_state.bastao_counts.get(current_holder, 0) + 1
        
        st.session_state.success_message = f"🎉 Bastão passou de **{current_holder}** para **{next_holder}**!"
        st.session_state.success_message_time = datetime.now()
        save_state()
        st.rerun()
    else:
        st.warning('⚠️ Não há próximo(a) colaborador(a) elegível na fila.')
        check_and_assume_baton()

def update_status(new_status_part, force_exit_queue=False):
    selected = st.session_state.colaborador_selectbox
    
    if not selected or selected == 'Selecione um nome':
        st.warning('Selecione um(a) colaborador(a).')
        return

    blocking_statuses = ['Almoço', 'Ausente', 'Saída rápida']
    should_exit_queue = new_status_part in blocking_statuses or force_exit_queue
    
    if should_exit_queue:
        final_status = new_status_part
        st.session_state[f'check_{selected}'] = False
        if selected in st.session_state.bastao_queue:
            st.session_state.bastao_queue.remove(selected)
    else:
        current = st.session_state.status_texto.get(selected, '')
        parts = [p.strip() for p in current.split('|') if p.strip()]
        type_of_new = new_status_part.split(':')[0]
        cleaned_parts = []
        for p in parts:
            if p == 'Indisponível': continue
            if p.startswith(type_of_new): continue
            cleaned_parts.append(p)
        cleaned_parts.append(new_status_part)
        cleaned_parts.sort(key=lambda x: 0 if 'Bastão' in x else 1 if 'Atividade' in x else 2)
        final_status = " | ".join(cleaned_parts)
    
    was_holder = next((True for c, s in st.session_state.status_texto.items() if 'Bastão' in s and c == selected), False)
    
    if was_holder and not should_exit_queue:
        if 'Bastão' not in final_status:
            final_status = f"Bastão | {final_status}"
    
    st.session_state.status_texto[selected] = final_status
    
    if was_holder and should_exit_queue:
        check_and_assume_baton()

def leave_specific_status(colaborador, status_type_to_remove):
    old_status = st.session_state.status_texto.get(colaborador, '')
    parts = [p.strip() for p in old_status.split('|')]
    new_parts = [p for p in parts if status_type_to_remove not in p and p]
    new_status = " | ".join(new_parts)
    if not new_status and colaborador not in st.session_state.bastao_queue:
        new_status = 'Indisponível'
    st.session_state.status_texto[colaborador] = new_status
    check_and_assume_baton()

def enter_from_indisponivel(colaborador):
    if colaborador not in st.session_state.bastao_queue:
        st.session_state.bastao_queue.append(colaborador)
    st.session_state[f'check_{colaborador}'] = True
    st.session_state.status_texto[colaborador] = ''
    check_and_assume_baton()


def gerar_html_relatorio(logs_filtrados):
    """Gera relatório HTML formatado"""
    html = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Relatório Informática</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .header {
                background: linear-gradient(135deg, #1f4788 0%, #2c5aa0 100%);
                color: white;
                padding: 30px;
                border-radius: 10px;
                text-align: center;
                margin-bottom: 30px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            .header h1 {
                margin: 0 0 10px 0;
                font-size: 28px;
            }
            .header p {
                margin: 5px 0;
                opacity: 0.9;
            }
            .registro {
                background: white;
                padding: 25px;
                margin-bottom: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                border-left: 5px solid #2c5aa0;
            }
            .registro-header {
                background-color: #e8f4f8;
                padding: 15px;
                margin: -25px -25px 20px -25px;
                border-radius: 8px 8px 0 0;
                border-bottom: 2px solid #2c5aa0;
            }
            .registro-header h2 {
                margin: 0;
                color: #1f4788;
                font-size: 20px;
            }
            .registro-tipo {
                display: inline-block;
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 14px;
                font-weight: bold;
                margin-left: 10px;
            }
            .tipo-atendimento {
                background-color: #4CAF50;
                color: white;
            }
            .tipo-horas {
                background-color: #FF9800;
                color: white;
            }
            .tipo-erro {
                background-color: #f44336;
                color: white;
            }
            .campo {
                margin: 12px 0;
                display: flex;
                border-bottom: 1px solid #eee;
                padding-bottom: 8px;
            }
            .campo-label {
                font-weight: bold;
                color: #1f4788;
                min-width: 150px;
                margin-right: 15px;
            }
            .campo-valor {
                color: #333;
                flex: 1;
            }
            .footer {
                text-align: center;
                margin-top: 40px;
                padding: 20px;
                color: #666;
                border-top: 2px solid #ddd;
            }
            @media print {
                body {
                    background-color: white;
                }
                .registro {
                    page-break-inside: avoid;
                    box-shadow: none;
                    border: 1px solid #ddd;
                }
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📊 RELATÓRIO DE REGISTROS - Informática</h1>
            <p>Sistema de Controle de Bastão</p>
            <p><strong>Gerado em:</strong> """ + datetime.now().strftime("%d/%m/%Y às %H:%M:%S") + """</p>
            <p><strong>Total de registros:</strong> """ + str(len(logs_filtrados)) + """</p>
        </div>
    """
    
    for idx, log in enumerate(logs_filtrados, 1):
        timestamp = log.get('timestamp', datetime.now())
        if isinstance(timestamp, str):
            try:
                timestamp = datetime.fromisoformat(timestamp)
            except:
                timestamp = datetime.now()
        
        data_hora = timestamp.strftime("%d/%m/%Y %H:%M:%S")
        colaborador = log.get('colaborador', 'N/A')
        
        # Determina tipo
        if 'usuario' in log:
            tipo = "ATENDIMENTO"
            classe_tipo = "tipo-atendimento"
            icone = "📝"
        elif 'inicio' in log and 'tempo' in log:
            tipo = "HORAS EXTRAS"
            classe_tipo = "tipo-horas"
            icone = "⏰"
        elif 'titulo' in log and 'relato' in log:
            tipo = "ERRO/NOVIDADE"
            classe_tipo = "tipo-erro"
            icone = "🐛"
        else:
            tipo = "REGISTRO"
            classe_tipo = "tipo-atendimento"
            icone = "📄"
        
        html += f"""
        <div class="registro">
            <div class="registro-header">
                <h2>{icone} REGISTRO #{idx} <span class="registro-tipo {classe_tipo}">{tipo}</span></h2>
            </div>
            
            <div class="campo">
                <div class="campo-label">📅 Data/Hora:</div>
                <div class="campo-valor">{data_hora}</div>
            </div>
            <div class="campo">
                <div class="campo-label">👤 Colaborador:</div>
                <div class="campo-valor">{colaborador}</div>
            </div>
        """
        
        # Campos específicos por tipo
        if 'usuario' in log:
            html += f"""
            <div class="campo">
                <div class="campo-label">👥 Usuário:</div>
                <div class="campo-valor">{log.get('usuario', 'N/A')}</div>
            </div>
            <div class="campo">
                <div class="campo-label">🏢 Setor:</div>
                <div class="campo-valor">{log.get('setor', 'N/A')}</div>
            </div>
            <div class="campo">
                <div class="campo-label">💻 Sistema:</div>
                <div class="campo-valor">{log.get('sistema', 'N/A')}</div>
            </div>
            <div class="campo">
                <div class="campo-label">📝 Descrição:</div>
                <div class="campo-valor">{log.get('descricao', 'N/A')}</div>
            </div>
            <div class="campo">
                <div class="campo-label">📞 Canal:</div>
                <div class="campo-valor">{log.get('canal', 'N/A')}</div>
            </div>
            <div class="campo">
                <div class="campo-label">✅ Desfecho:</div>
                <div class="campo-valor">{log.get('desfecho', 'N/A')}</div>
            </div>
            """
        
        elif 'inicio' in log and 'tempo' in log:
            html += f"""
            <div class="campo">
                <div class="campo-label">📅 Data:</div>
                <div class="campo-valor">{log.get('data', 'N/A')}</div>
            </div>
            <div class="campo">
                <div class="campo-label">🕐 Início:</div>
                <div class="campo-valor">{log.get('inicio', 'N/A')}</div>
            </div>
            <div class="campo">
                <div class="campo-label">⏱️ Tempo Total:</div>
                <div class="campo-valor">{log.get('tempo', 'N/A')}</div>
            </div>
            <div class="campo">
                <div class="campo-label">📝 Motivo:</div>
                <div class="campo-valor">{log.get('motivo', 'N/A')}</div>
            </div>
            """
        
        elif 'titulo' in log:
            html += f"""
            <div class="campo">
                <div class="campo-label">📌 Título:</div>
                <div class="campo-valor">{log.get('titulo', 'N/A')}</div>
            </div>
            <div class="campo">
                <div class="campo-label">🎯 Objetivo:</div>
                <div class="campo-valor">{log.get('objetivo', 'N/A')}</div>
            </div>
            <div class="campo">
                <div class="campo-label">🧪 Relato:</div>
                <div class="campo-valor">{log.get('relato', 'N/A')}</div>
            </div>
            <div class="campo">
                <div class="campo-label">🏁 Resultado:</div>
                <div class="campo-valor">{log.get('resultado', 'N/A')}</div>
            </div>
            """
        
        html += "</div>"
    
    html += """
        <div class="footer">
            <p>Sistema de Controle de Bastão - Informática/TJMG</p>
            <p>Relatório gerado automaticamente</p>
        </div>
    </body>
    </html>
    """
    
    return html

def handle_simon_game():
    COLORS = ["🔴", "🔵", "🟢", "🟡"]
    st.markdown("### 🧠 Jogo da Memória (Simon)")
    st.caption("Repita a sequência de cores!")
    
    if st.session_state.simon_status == 'start':
        if st.button("▶️ Iniciar Jogo", use_container_width=True):
            st.session_state.simon_sequence = [random.choice(COLORS)]
            st.session_state.simon_user_input = []
            st.session_state.simon_level = 1
            st.session_state.simon_status = 'showing'
            st.rerun()
            
    elif st.session_state.simon_status == 'showing':
        st.info(f"Nível {st.session_state.simon_level}: Memorize a sequência!")
        cols = st.columns(len(st.session_state.simon_sequence))
        for i, color in enumerate(st.session_state.simon_sequence):
            with cols[i]:
                st.markdown(f"<h1 style='text-align: center;'>{color}</h1>", unsafe_allow_html=True)
        st.markdown("---")
        if st.button("🙈 Já decorei! Responder", type="primary", use_container_width=True):
            st.session_state.simon_status = 'playing'
            st.rerun()
            
    elif st.session_state.simon_status == 'playing':
        st.markdown(f"**Nível {st.session_state.simon_level}** - Clique na ordem:")
        c1, c2, c3, c4 = st.columns(4)
        pressed = None
        if c1.button("🔴", use_container_width=True): pressed = "🔴"
        if c2.button("🔵", use_container_width=True): pressed = "🔵"
        if c3.button("🟢", use_container_width=True): pressed = "🟢"
        if c4.button("🟡", use_container_width=True): pressed = "🟡"
        
        if pressed:
            st.session_state.simon_user_input.append(pressed)
            current_idx = len(st.session_state.simon_user_input) - 1
            if st.session_state.simon_user_input[current_idx] != st.session_state.simon_sequence[current_idx]:
                st.session_state.simon_status = 'lost'
                st.rerun()
            elif len(st.session_state.simon_user_input) == len(st.session_state.simon_sequence):
                st.success("Correto! Próximo nível...")
                time.sleep(0.5)
                st.session_state.simon_sequence.append(random.choice(COLORS))
                st.session_state.simon_user_input = []
                st.session_state.simon_level += 1
                st.session_state.simon_status = 'showing'
                st.rerun()
                
        if st.session_state.simon_user_input:
            st.markdown(f"Sua resposta: {' '.join(st.session_state.simon_user_input)}")
            
    elif st.session_state.simon_status == 'lost':
        st.error(f"❌ Errou! Você chegou ao Nível {st.session_state.simon_level}.")
        st.markdown(f"Sequência correta era: {' '.join(st.session_state.simon_sequence)}")
        
        colaborador = st.session_state.colaborador_selectbox
        if colaborador and colaborador != 'Selecione um nome':
            score = st.session_state.simon_level
            current_ranking = st.session_state.simon_ranking
            found = False
            for entry in current_ranking:
                if entry['nome'] == colaborador:
                    if score > entry['score']:
                        entry['score'] = score
                    found = True
                    break
            if not found:
                current_ranking.append({'nome': colaborador, 'score': score})
            st.session_state.simon_ranking = sorted(current_ranking, key=lambda x: x['score'], reverse=True)[:5]
            st.success(f"Pontuação salva para {colaborador}!")
        else:
            st.warning("Selecione seu nome no menu superior para salvar no Ranking.")
            
        if st.button("Tentar Novamente"):
            st.session_state.simon_status = 'start'
            st.rerun()
            
    st.markdown("---")
    st.subheader("🏆 Ranking Global (Top 5)")
    ranking = st.session_state.simon_ranking
    if not ranking:
        st.markdown("_Nenhum recorde ainda._")
    else:
        df_rank = pd.DataFrame(ranking)
        st.table(df_rank)

def set_chamado_step(step_num):
    st.session_state.chamado_guide_step = step_num

def handle_chamado_submission():
    st.toast("Rascunho salvo localmente!", icon="✅")
    st.session_state.chamado_guide_step = 0

def manual_rerun():
    st.rerun()

def toggle_view(view_name):
    if st.session_state.active_view == view_name:
        st.session_state.active_view = None
    else:
        st.session_state.active_view = view_name
        if view_name == 'chamados':
            st.session_state.chamado_guide_step = 1

# ============================================
# INTERFACE PRINCIPAL
# ============================================

st.set_page_config(page_title="Controle Bastão Informática 2026", layout="wide", page_icon="🥂")
init_session_state()
apply_modern_styles()
st.components.v1.html("<script>window.scrollTo(0, 0);</script>", height=0)

# ==================== HEADER ====================
st.markdown("""
<div style="background: white; padding: 2rem; border-radius: 12px; margin-bottom: 2rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border-bottom: 3px solid #2563eb;">
    <div style="text-align: center;">
        <h1 style="color: #0f172a; margin: 0; font-size: 2rem; font-weight: 600; letter-spacing: -0.02em;">
            Controle de Bastão
        </h1>
        <p style="color: #64748b; margin: 0.5rem 0 0 0; font-size: 0.875rem; font-weight: 500;">
            Setor de Informática • TJMG • 2026
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== ENTRADA RÁPIDA ====================
with st.container():
    col_label, col_select, col_button = st.columns([1, 3, 1])
    
    with col_label:
        st.markdown("**Entrada Rápida**")
    
    with col_select:
        novo_responsavel = st.selectbox(
            "Selecione colaborador", 
            options=["Selecione..."] + COLABORADORES,
            label_visibility="collapsed", 
            key="quick_enter"
        )
    
    with col_button:
        if st.button("➕ Entrar", help="Entrar na fila imediatamente", use_container_width=True, type="primary"):
            if novo_responsavel and novo_responsavel != "Selecione...":
                toggle_queue(novo_responsavel)
                st.session_state.colaborador_selectbox = novo_responsavel
                st.success(f"✅ {novo_responsavel} entrou na fila!")
                save_state()
                st.rerun()

st.markdown("---")


# Auto-refresh
st_autorefresh(interval=8000, key='auto_rerun_key')

# Layout principal
col_principal, col_disponibilidade = st.columns([1.5, 1])
queue = st.session_state.bastao_queue
responsavel = next((c for c, s in st.session_state.status_texto.items() if 'Bastão' in s), None)

current_index = queue.index(responsavel) if responsavel in queue else -1
proximo_index = find_next_holder_index(current_index, queue)
proximo = queue[proximo_index] if proximo_index != -1 else None

restante = []
if proximo_index != -1:
    num_q = len(queue)
    start_check_idx = (proximo_index + 1) % num_q
    current_check_idx = start_check_idx
    checked_count = 0
    while checked_count < num_q:
        if current_check_idx == start_check_idx and checked_count > 0:
            break
        if 0 <= current_check_idx < num_q:
            colaborador = queue[current_check_idx]
            if colaborador != responsavel and colaborador != proximo and st.session_state.get(f'check_{colaborador}'):
                restante.append(colaborador)
        current_check_idx = (current_check_idx + 1) % num_q
        checked_count += 1

with col_principal:
    if responsavel:
        st.markdown(f"""
        <div style="background: white; border: 2px solid #e2e8f0; padding: 2rem; border-radius: 12px; margin-bottom: 1.5rem; box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);">
            <div>
                <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; color: #64748b; margin-bottom: 0.75rem;">
                    Responsável Atual
                </div>
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="font-size: 2rem; font-weight: 700; color: #0f172a; line-height: 1.2;">
                        {responsavel}
                    </div>
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style="flex-shrink: 0; opacity: 0.6;">
                        <rect x="10" y="2" width="4" height="20" rx="2" fill="#2563eb"/>
                        <circle cx="12" cy="3" r="2" fill="#2563eb"/>
                    </svg>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Métricas em cards separados
        col_metric1, col_metric2 = st.columns(2)
        
        duration = timedelta()
        if st.session_state.bastao_start_time:
            duration = datetime.now() - st.session_state.bastao_start_time
        
        with col_metric1:
            st.markdown(f"""
            <div style="background: white; border: 1px solid #e2e8f0; padding: 1.25rem; border-radius: 10px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
                <div style="color: #64748b; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.5rem;">
                    ⏱️ Tempo com Bastão
                </div>
                <div style="color: #0f172a; font-size: 1.5rem; font-weight: 700;">
                    {format_time_duration(duration)}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_metric2:
            rodadas = st.session_state.bastao_counts.get(responsavel, 0)
            st.markdown(f"""
            <div style="background: white; border: 1px solid #e2e8f0; padding: 1.25rem; border-radius: 10px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
                <div style="color: #64748b; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.5rem;">
                    🔄 Rodadas Hoje
                </div>
                <div style="color: #0f172a; font-size: 1.5rem; font-weight: 700;">
                    {rodadas}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: #eff6ff; border: 1px solid #bfdbfe; padding: 1.5rem; border-radius: 10px; text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">👥</div>
            <div style="color: #1e40af; font-weight: 500;">Nenhum colaborador com o bastão</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("##")
    st.header("Próximos da Fila")
    
    # Exibir mensagem de sucesso se existir
    if st.session_state.get('success_message') and st.session_state.get('success_message_time'):
        elapsed = (datetime.now() - st.session_state.success_message_time).total_seconds()
        if elapsed < 10:
            st.success(st.session_state.success_message)
        else:
            st.session_state.success_message = None
            st.session_state.success_message_time = None
    
    if proximo:
        st.markdown(f'### 1º: **{proximo}**')
    if restante:
        st.markdown(f'#### 2º em diante: {", ".join(restante)}')
    if not proximo and not restante:
        if responsavel:
            st.markdown('*Apenas o responsável atual é elegível.*')
        else:
            st.markdown('*Ninguém elegível na fila.*')
    elif not restante and proximo:
        st.markdown("&nbsp;")
    
    st.markdown("###")
    st.header("**Colaborador(a)**")
    st.selectbox('Selecione:', options=['Selecione um nome'] + COLABORADORES, key='colaborador_selectbox', label_visibility='collapsed')
    
    st.markdown("#### ")
    st.markdown("**Ações:**")
    
    row1_c1, row1_c2 = st.columns(2)
    row2_c1, row2_c2, row2_c3, row2_c4, row2_c5 = st.columns(5)
    
    row1_c1.button('🎯 Passar', on_click=rotate_bastao, use_container_width=True, help='Passa o bastão.', type='primary')
    
    row2_c1.button('🍽️ Almoço', on_click=update_status, args=('Almoço', True,), use_container_width=True)
    row2_c2.button('🎙️ Sessão', on_click=toggle_view, args=('menu_sessao',), use_container_width=True)
    row2_c3.button('🚶 Saída', on_click=update_status, args=('Saída rápida', True,), use_container_width=True)
    row2_c4.button('👤 Ausente', on_click=update_status, args=('Ausente', True,), use_container_width=True)
    
    # Menus contextuais
    if st.session_state.active_view == 'menu_sessao':
        with st.container(border=True):
            st.markdown("### Detalhes da Sessão")
            sessao_desc = st.text_input("Qual Câmara/Sessão?", placeholder="Ex: 1ª Cível...")
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                if st.button("Confirmar Sessão", type="primary", use_container_width=True):
                    if sessao_desc:
                        status_final = f"Sessão: {sessao_desc}"
                        update_status(status_final, force_exit_queue=True)
                        st.session_state.active_view = None
                        st.rerun()
                    else:
                        st.warning("Digite o nome da sessão.")
            with col_s2:
                if st.button("Cancelar", use_container_width=True, key='cancel_sessao'):
                    st.session_state.active_view = None
                    st.rerun()
    
    st.markdown("####")
    st.button('🔄 Atualizar (Manual)', on_click=manual_rerun, use_container_width=True)
    st.markdown("---")
    
    # Ferramentas
    c_tool1, c_tool2, c_tool3 = st.columns(3)
    c_tool4, c_tool5, c_tool6 = st.columns(3)
    
    c_tool1.button("🆘 Chamados", help="Guia de Abertura de Chamados", use_container_width=True, on_click=toggle_view, args=("chamados",))
    c_tool2.button("📝 Atendimento", help="Registrar Atendimento (Local)", use_container_width=True, on_click=toggle_view, args=("atendimentos",))
    c_tool3.button("⏰ H. Extras", help="Registrar Horas Extras (Local)", use_container_width=True, on_click=toggle_view, args=("hextras",))
    
    c_tool4.button("🧠 Descanso", help="Jogo e Ranking", use_container_width=True, on_click=toggle_view, args=("descanso",))
    c_tool5.button("🐛 Erro/Novidade", help="Relatar Erro (Local)", use_container_width=True, on_click=toggle_view, args=("erro_novidade",))
    c_tool6.button("📊 Relatórios", help="Ver Registros Salvos", use_container_width=True, on_click=toggle_view, args=("relatorios",))
    
    # Views das ferramentas
    if st.session_state.active_view == "chamados":
        with st.container(border=True):
            st.header("Guia de Abertura de Chamados")
            guide_step = st.session_state.get('chamado_guide_step', 1)
            
            if guide_step == 1:
                st.subheader("📄 Passo 1: Testes Iniciais")
                st.markdown("Antes de abrir o chamado, realize os procedimentos de suporte e testes necessários.")
                st.button("Próximo (Passo 2) ➡️", on_click=set_chamado_step, args=(2,))
            elif guide_step == 2:
                st.subheader("PASSO 2: Checklist de Abertura")
                st.markdown("**1. Dados do Usuário**\n**2. Dados do Processo**\n**3. Descrição do Erro**\n**4. Prints/Vídeo**")
                st.button("Próximo (Passo 3) ➡️", on_click=set_chamado_step, args=(3,))
            elif guide_step == 3:
                st.subheader("PASSO 3: Registrar e Informar")
                st.markdown("Envie e-mail ao usuário informando o número do chamado.")
                st.button("Próximo (Campo) ➡️", on_click=set_chamado_step, args=(4,))
            elif guide_step == 4:
                st.subheader("Campo de Digitação do Chamado")
                st.text_area("Rascunho do Chamado:", height=300, key="chamado_textarea", label_visibility="collapsed")
                if st.button("Salvar Rascunho Localmente", on_click=handle_chamado_submission, use_container_width=True, type="primary"):
                    pass
    
    elif st.session_state.active_view == "atendimentos":
        with st.container(border=True):
            st.markdown("### Registro de Atendimento (Local)")
            at_data = st.date_input("Data:", value=date.today(), format="DD/MM/YYYY", key="at_data")
            at_usuario = st.selectbox("Usuário:", REG_USUARIO_OPCOES, index=None, placeholder="Selecione...", key="at_user")
            at_nome_setor = st.text_input("Nome usuário - Setor:", key="at_setor")
            at_sistema = st.selectbox("Sistema:", REG_SISTEMA_OPCOES, index=None, placeholder="Selecione...", key="at_sys")
            at_descricao = st.text_input("Descrição:", key="at_desc")
            at_canal = st.selectbox("Canal:", REG_CANAL_OPCOES, index=None, placeholder="Selecione...", key="at_channel")
            at_desfecho = st.selectbox("Desfecho:", REG_DESFECHO_OPCOES, index=None, placeholder="Selecione...", key="at_outcome")
            
            if st.button("Salvar Registro Localmente", type="primary", use_container_width=True):
                colaborador = st.session_state.colaborador_selectbox
                if colaborador and colaborador != "Selecione um nome":
                    st.success("✅ Atendimento registrado localmente!")
                    log_entry = {
                        'timestamp': datetime.now(),
                        'colaborador': colaborador,
                        'data': at_data,
                        'usuario': at_usuario,
                        'setor': at_nome_setor,
                        'sistema': at_sistema,
                        'descricao': at_descricao,
                        'canal': at_canal,
                        'desfecho': at_desfecho
                    }
                    st.session_state.daily_logs.append(log_entry)
                else:
                    st.error("Selecione um colaborador.")
    
    elif st.session_state.active_view == "hextras":
        with st.container(border=True):
            st.markdown("### Registro de Horas Extras (Local)")
            he_data = st.date_input("Data:", value=date.today(), format="DD/MM/YYYY")
            he_inicio = st.time_input("Horário de Início:", value=dt_time(18, 0))
            he_tempo = st.text_input("Tempo Total (ex: 2h30):")
            he_motivo = st.text_input("Motivo da Hora Extra:")
            
            if st.button("Salvar HE Localmente", type="primary", use_container_width=True):
                colaborador = st.session_state.colaborador_selectbox
                if colaborador and colaborador != "Selecione um nome":
                    st.success("✅ Horas extras registradas localmente!")
                    he_entry = {
                        'timestamp': datetime.now(),
                        'colaborador': colaborador,
                        'data': he_data,
                        'inicio': he_inicio,
                        'tempo': he_tempo,
                        'motivo': he_motivo
                    }
                    st.session_state.daily_logs.append(he_entry)
                else:
                    st.error("Selecione um colaborador.")
    
    elif st.session_state.active_view == "descanso":
        with st.container(border=True):
            handle_simon_game()
    
    elif st.session_state.active_view == "erro_novidade":
        with st.container(border=True):
            st.markdown("### 🐛 Registro de Erro ou Novidade (Local)")
            en_titulo = st.text_input("Título:")
            en_objetivo = st.text_area("Objetivo:", height=100)
            en_relato = st.text_area("Relato:", height=200)
            en_resultado = st.text_area("Resultado:", height=150)
            
            if st.button("Salvar Relato Localmente", type="primary", use_container_width=True):
                colaborador = st.session_state.colaborador_selectbox
                if colaborador and colaborador != "Selecione um nome":
                    st.success("✅ Relato salvo localmente!")
                    erro_entry = {
                        'timestamp': datetime.now(),
                        'colaborador': colaborador,
                        'titulo': en_titulo,
                        'objetivo': en_objetivo,
                        'relato': en_relato,
                        'resultado': en_resultado
                    }
                    st.session_state.daily_logs.append(erro_entry)
                    st.session_state.active_view = None
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error("Selecione um colaborador.")
    
    elif st.session_state.active_view == "relatorios":
        with st.container(border=True):
            st.markdown("### 📊 Relatórios e Registros Salvos")
            
            logs = st.session_state.daily_logs
            
            if not logs:
                st.info("📭 Nenhum registro salvo ainda.")
                st.markdown("---")
                st.markdown("**Como usar:**")
                st.markdown("1. Use as abas acima para registrar atendimentos, horas extras, etc.")
                st.markdown("2. Clique em 'Salvar Localmente'")
                st.markdown("3. Os registros aparecerão aqui!")
            else:
                st.success(f"✅ **{len(logs)} registro(s) encontrado(s)**")
                
                # Filtros
                st.markdown("#### 🔍 Filtros")
                col_f1, col_f2 = st.columns(2)
                
                with col_f1:
                    tipo_filtro = st.selectbox(
                        "Tipo de Registro:",
                        ["Todos", "Atendimentos", "Horas Extras", "Erros/Novidades"]
                    )
                
                with col_f2:
                    colaboradores_nos_logs = list(set([log.get('colaborador', 'N/A') for log in logs]))
                    colaborador_filtro = st.selectbox(
                        "Colaborador:",
                        ["Todos"] + sorted(colaboradores_nos_logs)
                    )
                
                st.markdown("---")
                
                # Filtrar logs
                logs_filtrados = logs.copy()
                
                if tipo_filtro == "Atendimentos":
                    logs_filtrados = [l for l in logs_filtrados if 'usuario' in l]
                elif tipo_filtro == "Horas Extras":
                    logs_filtrados = [l for l in logs_filtrados if 'inicio' in l and 'tempo' in l]
                elif tipo_filtro == "Erros/Novidades":
                    logs_filtrados = [l for l in logs_filtrados if 'titulo' in l and 'relato' in l]
                
                if colaborador_filtro != "Todos":
                    logs_filtrados = [l for l in logs_filtrados if l.get('colaborador') == colaborador_filtro]
                
                st.markdown(f"#### 📋 Exibindo {len(logs_filtrados)} registro(s)")
                
                # Exibir logs
                for idx, log in enumerate(reversed(logs_filtrados), 1):
                    timestamp = log.get('timestamp', datetime.now())
                    if isinstance(timestamp, str):
                        try:
                            timestamp = datetime.fromisoformat(timestamp)
                        except:
                            timestamp = datetime.now()
                    
                    data_hora = timestamp.strftime("%d/%m/%Y %H:%M:%S")
                    colaborador = log.get('colaborador', 'N/A')
                    
                    # Identifica tipo de registro
                    if 'usuario' in log:
                        # Atendimento
                        with st.expander(f"📝 #{idx} - Atendimento - {colaborador} - {data_hora}"):
                            st.markdown(f"**👤 Colaborador:** {colaborador}")
                            st.markdown(f"**📅 Data:** {log.get('data', 'N/A')}")
                            st.markdown(f"**👥 Usuário:** {log.get('usuario', 'N/A')}")
                            st.markdown(f"**🏢 Setor:** {log.get('setor', 'N/A')}")
                            st.markdown(f"**💻 Sistema:** {log.get('sistema', 'N/A')}")
                            st.markdown(f"**📝 Descrição:** {log.get('descricao', 'N/A')}")
                            st.markdown(f"**📞 Canal:** {log.get('canal', 'N/A')}")
                            st.markdown(f"**✅ Desfecho:** {log.get('desfecho', 'N/A')}")
                    
                    elif 'inicio' in log and 'tempo' in log:
                        # Horas Extras
                        with st.expander(f"⏰ #{idx} - Horas Extras - {colaborador} - {data_hora}"):
                            st.markdown(f"**👤 Colaborador:** {colaborador}")
                            st.markdown(f"**📅 Data:** {log.get('data', 'N/A')}")
                            st.markdown(f"**🕐 Início:** {log.get('inicio', 'N/A')}")
                            st.markdown(f"**⏱️ Tempo Total:** {log.get('tempo', 'N/A')}")
                            st.markdown(f"**📝 Motivo:** {log.get('motivo', 'N/A')}")
                    
                    elif 'titulo' in log and 'relato' in log:
                        # Erro/Novidade
                        with st.expander(f"🐛 #{idx} - Erro/Novidade - {colaborador} - {data_hora}"):
                            st.markdown(f"**👤 Autor:** {colaborador}")
                            st.markdown(f"**📌 Título:** {log.get('titulo', 'N/A')}")
                            st.markdown(f"**🎯 Objetivo:**")
                            st.text(log.get('objetivo', 'N/A'))
                            st.markdown(f"**🧪 Relato:**")
                            st.text(log.get('relato', 'N/A'))
                            st.markdown(f"**🏁 Resultado:**")
                            st.text(log.get('resultado', 'N/A'))
                
                st.markdown("---")
                
                # Botões de ação
                col_a1, col_a2 = st.columns(2)
                
                with col_a1:
                    if st.button("🗑️ Limpar Todos os Registros", use_container_width=True):
                        st.session_state.daily_logs = []
                        st.success("✅ Registros limpos!")
                        time.sleep(1)
                        st.rerun()
                
                with col_a2:
                    # Exportar para HTML
                    if st.button("📥 Gerar Relatório HTML", use_container_width=True):
                        html_content = gerar_html_relatorio(logs_filtrados)
                        
                        # Botão de download
                        st.download_button(
                            label="⬇️ Baixar Relatório HTML",
                            data=html_content,
                            file_name=f"relatorio_informatica_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                            mime="text/html"
                        )
                        
                        # Exibir preview
                        st.success("✅ Relatório gerado! Clique no botão acima para baixar e abrir em nova aba.")
                        st.info("💡 Dica: Após baixar, clique duas vezes no arquivo .html para abrir no navegador")

# Coluna lateral (Disponibilidade)
with col_disponibilidade:
    st.markdown("###")
    st.header('Status dos(as) Colaboradores(as)')
    
    # Listas de status
    import re
    ui_lists = {
        'fila': [],
        'almoco': [],
        'saida': [],
        'ausente': [],
        'atividade_especifica': [],
        'sessao_especifica': [],
        'reuniao_especifica': [],
        'indisponivel': []
    }
    
    for nome in COLABORADORES:
        if nome in st.session_state.bastao_queue:
            ui_lists['fila'].append(nome)
        
        status = st.session_state.status_texto.get(nome, 'Indisponível')
        
        if status == '' or status is None:
            pass
        elif status == 'Almoço':
            ui_lists['almoco'].append(nome)
        elif status == 'Ausente':
            ui_lists['ausente'].append(nome)
        elif status == 'Saída rápida':
            ui_lists['saida'].append(nome)
        elif status == 'Indisponível':
            if nome not in st.session_state.bastao_queue:
                ui_lists['indisponivel'].append(nome)
        
        if 'Sessão:' in status:
            match = re.search(r'Sessão: (.*)', status)
            if match:
                ui_lists['sessao_especifica'].append((nome, match.group(1).split('|')[0].strip()))
        
                ui_lists['reuniao_especifica'].append((nome, match.group(1).split('|')[0].strip()))
        
        if 'Atividade:' in status:
            match = re.search(r'Atividade: (.*)', status)
            if match:
                ui_lists['atividade_especifica'].append((nome, match.group(1).split('|')[0].strip()))
    
    # Renderizar fila
    st.subheader(f'✅ Na Fila ({len(ui_lists["fila"])})')
    render_order = [c for c in queue if c in ui_lists["fila"]]
    if not render_order:
        st.markdown('_Ninguém na fila._')
    else:
        for nome in render_order:
            col_nome, col_check = st.columns([0.85, 0.15], vertical_alignment="center")
            key = f'chk_fila_{nome}'
            is_checked = True
            col_check.checkbox(' ', key=key, value=is_checked, on_change=toggle_queue, args=(nome,), label_visibility='collapsed')
            
            status_atual = st.session_state.status_texto.get(nome, '')
            extra_info = ""
            if "Atividade" in status_atual:
                extra_info += " 📋"
            
            if nome == responsavel:
                display = f'<span style="background-color: #FFD700; color: #000; padding: 2px 6px; border-radius: 5px; font-weight: bold;">🥂 {nome}</span>'
            else:
                display = f'**{nome}**{extra_info} :blue-background[Aguardando]'
            col_nome.markdown(display, unsafe_allow_html=True)
    st.markdown('---')
    
    # Função auxiliar para renderizar seções
    def render_section_detalhada(title, icon, lista_tuplas, tag_color, keyword_removal):
        st.subheader(f'{icon} {title} ({len(lista_tuplas)})')
        if not lista_tuplas:
            st.markdown(f'_Ninguém em {title.lower()}._')
        else:
            for nome, desc in sorted(lista_tuplas, key=lambda x: x[0]):
                col_nome, col_check = st.columns([0.85, 0.15], vertical_alignment="center")
                key_dummy = f'chk_status_{title}_{nome}'
                col_check.checkbox(' ', key=key_dummy, value=True, on_change=leave_specific_status, args=(nome, keyword_removal), label_visibility='collapsed')
                col_nome.markdown(f'**{nome}** :{tag_color}-background[{desc}]', unsafe_allow_html=True)
        st.markdown('---')
    
    def render_section_simples(title, icon, names, tag_color):
        st.subheader(f'{icon} {title} ({len(names)})')
        if not names:
            st.markdown(f'_Ninguém em {title.lower()}._')
        else:
            for nome in sorted(names):
                col_nome, col_check = st.columns([0.85, 0.15], vertical_alignment="center")
                key_dummy = f'chk_simples_{title}_{nome}'
                if title == 'Indisponível':
                    col_check.checkbox(' ', key=key_dummy, value=False, on_change=enter_from_indisponivel, args=(nome,), label_visibility='collapsed')
                else:
                    col_check.checkbox(' ', key=key_dummy, value=True, on_change=leave_specific_status, args=(nome, title), label_visibility='collapsed')
                col_nome.markdown(f'**{nome}** :{tag_color}-background[{title}]', unsafe_allow_html=True)
        st.markdown('---')
    
    render_section_detalhada('Em Demanda', '📋', ui_lists['atividade_especifica'], 'orange', 'Atividade')
    render_section_simples('Almoço', '🍽️', ui_lists['almoco'], 'red')
    render_section_detalhada('Sessão', '🎙️', ui_lists['sessao_especifica'], 'green', 'Sessão')
    render_section_simples('Saída rápida', '🚶', ui_lists['saida'], 'red')
    render_section_simples('Ausente', '👤', ui_lists['ausente'], 'violet')
    render_section_simples('Indisponível', '❌', ui_lists['indisponivel'], 'grey')

# Footer
st.markdown("---")
st.caption("Sistema de Controle de Bastão - Informática 2026 - Versão Local (Sem Integrações Externas)")
