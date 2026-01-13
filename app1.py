# ============================================
# CONTROLE DE BASTÃO CESUPE 2026
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

# --- Constantes de Consultores ---
CONSULTORES = sorted([
    "Alex Paulo da Silva",
    "Dirceu Gonçalves Siqueira Neto",
    "Douglas de Souza Gonçalves",
    "Farley Leandro de Oliveira Juliano", 
    "Gleis da Silva Rodrigues",
    "Hugo Leonardo Murta",
    "Igor Dayrell Gonçalves Correa",
    "Jerry Marcos dos Santos Neto",
    "Jonatas Gomes Saraiva",
    "Leandro Victor Catharino",
    "Luiz Henrique Barros Oliveira",
    "Marcelo dos Santos Dutra",
    "Marina Silva Marques",
    "Marina Torres do Amaral",
    "Vanessa Ligiane Pimenta Santos"
])

# --- Constantes de Opções ---
REG_USUARIO_OPCOES = ["Cartório", "Gabinete", "Externo"]
REG_SISTEMA_OPCOES = ["Conveniados", "Outros", "Eproc", "Themis", "JPE", "SIAP"]
REG_CANAL_OPCOES = ["Presencial", "Telefone", "Email", "Whatsapp", "Outros"]
REG_DESFECHO_OPCOES = ["Resolvido - Cesupe", "Escalonado"]

CAMARAS_DICT = {
    "Cartório da 1ª Câmara Cível": "caciv1@tjmg.jus.br", "Cartório da 2ª Câmara Cível": "caciv2@tjmg.jus.br",
    "Cartório da 3ª Câmara Cível": "caciv3@tjmg.jus.br", "Cartório da 4ª Câmara Cível": "caciv4@tjmg.jus.br",
    "Cartório da 5ª Câmara Cível": "caciv5@tjmg.jus.br", "Cartório da 6ª Câmara Cível": "caciv6@tjmg.jus.br",
    "Cartório da 7ª Câmara Cível": "caciv7@tjmg.jus.br", "Cartório da 8ª Câmara Cível": "caciv8@tjmg.jus.br",
    "Cartório da 9ª Câmara Cível": "caciv9@tjmg.jus.br", "Cartório da 10ª Câmara Cível": "caciv10@tjmg.jus.br",
    "Cartório da 11ª Câmara Cível": "caciv11@tjmg.jus.br", "Cartório da 12ª Câmara Cível": "caciv12@tjmg.jus.br",
    "Cartório da 13ª Câmara Cível": "caciv13@tjmg.jus.br", "Cartório da 14ª Câmara Cível": "caciv14@tjmg.jus.br",
    "Cartório da 15ª Câmara Cível": "caciv15@tjmg.jus.br", "Cartório da 16ª Câmara Cível": "caciv16@tjmg.jus.br",
    "Cartório da 17ª Câmara Cível": "caciv17@tjmg.jus.br", "Cartório da 18ª Câmara Cível": "caciv18@tjmg.jus.br",
    "Cartório da 19ª Câmara Cível": "caciv19@tjmg.jus.br", "Cartório da 20ª Câmara Cível": "caciv20@tjmg.jus.br",
    "Cartório da 21ª Câmara Cível": "caciv21@tjmg.jus.br"
}
CAMARAS_OPCOES = sorted(list(CAMARAS_DICT.keys()))

OPCOES_ATIVIDADES_STATUS = ["HP", "E-mail", "WhatsApp Plantão", "Treinamento", "Homologação", "Redação Documentos", "Outros"]
OPCOES_PROJETOS = ["Soma", "Treinamentos Eproc", "Manuais Eproc", "Cartilhas Gabinetes", "Notebook Lm", "Inteligência artifical cartórios"]

# GIFs e Recursos
GIF_BASTAO_HOLDER = "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExa3Uwazd5cnNra2oxdDkydjZkcHdqcWN2cng0Y2N0cmNmN21vYXVzMiZlcD12MV9pbnRlcm5uYWxfZ2lmX2J5X2lkJmN0PWc/3rXs5J0hZkXwTZjuvM/giphy.gif"
BASTAO_EMOJI = "🥂"
GIF_URL_WARNING = 'https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExY2pjMDN0NGlvdXp1aHZ1ejJqMnY5MG1yZmN0d3NqcDl1bTU1dDJrciZlcD12MV9pbnRlcm5uYWxfZ2lmX2J5X2lkJmN0PWc/fXnRObM8Q0RkOmR5nf/giphy.gif'
GIF_URL_ROTATION = 'https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExdmx4azVxbGt4Mnk1cjMzZm5sMmp1YThteGJsMzcyYmhsdmFoczV0aSZlcD12MV9pbnRlcm5uYWxfZ2lmX2J5X2lkJmN0PWc/JpkZEKWY0s9QI4DGvF/giphy.gif'
GIF_URL_NEDRY = 'https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExMGNkMGx3YnNkcXQ2bHJmNTZtZThraHhuNmVoOTNmbG0wcDloOXAybiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/7kyWoqTue3po4/giphy.gif'

# ============================================
# SISTEMA DE CACHE GLOBAL (PERSISTÊNCIA)
# ============================================

# ============================================
# FUNÇÕES AUXILIARES
# ============================================

def format_time_duration(duration):
    if not isinstance(duration, timedelta): return '--:--:--'
    s = int(duration.total_seconds())
    h, s = divmod(s, 3600)
    m, s = divmod(s, 60)
    return f'{h:02}:{m:02}:{s:02}'

def init_session_state():
    """Inicializa o estado da sessão"""
    defaults = {
        'bastao_queue': [],
        'status_texto': {nome: 'Indisponível' for nome in CONSULTORES},
        'bastao_start_time': None,
        'bastao_counts': {nome: 0 for nome in CONSULTORES},
        'rotation_gif_start_time': None,
        'gif_warning': False,
        'auxilio_ativo': False,
        'active_view': None,
        'chamado_guide_step': 0,
        'simon_sequence': [],
        'simon_user_input': [],
        'simon_status': 'start',
        'simon_level': 1,
        'simon_ranking': [],
        'daily_logs': [],
        'last_jira_number': "",
        'success_message': None,
        'success_message_time': None,
    }
    
    for key, default in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default
    
    for nome in CONSULTORES:
        if f'check_{nome}' not in st.session_state:
            st.session_state[f'check_{nome}'] = False

def find_next_holder_index(current_index, queue):
    if not queue: return -1
    num_consultores = len(queue)
    if num_consultores == 0: return -1
    next_idx = (current_index + 1) % num_consultores
    attempts = 0
    while attempts < num_consultores:
        consultor = queue[next_idx]
        if st.session_state.get(f'check_{consultor}'): return next_idx
        next_idx = (next_idx + 1) % num_consultores
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
    for c in CONSULTORES:
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

def toggle_queue(consultor):
    st.session_state.gif_warning = False
    st.session_state.rotation_gif_start_time = None
    
    if consultor in st.session_state.bastao_queue:
        st.session_state.bastao_queue.remove(consultor)
        st.session_state[f'check_{consultor}'] = False
        current_s = st.session_state.status_texto.get(consultor, '')
        if current_s == '' or current_s == 'Bastão':
            st.session_state.status_texto[consultor] = 'Indisponível'
    else:
        st.session_state.bastao_queue.append(consultor)
        st.session_state[f'check_{consultor}'] = True
        current_s = st.session_state.status_texto.get(consultor, 'Indisponível')
        if current_s == 'Indisponível':
            st.session_state.status_texto[consultor] = ''

    check_and_assume_baton()



def rotate_bastao():
    """Passa o bastão para o próximo consultor (SEM PRECISAR SELECIONAR)"""
    st.session_state.gif_warning = False
    st.session_state.rotation_gif_start_time = None
    
    queue = st.session_state.bastao_queue
    current_holder = next((c for c, s in st.session_state.status_texto.items() if 'Bastão' in s), None)
    
    if not current_holder:
        st.warning('⚠️ Ninguém tem o bastão no momento.')
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
        st.session_state.rotation_gif_start_time = datetime.now()
        
        # Salva mensagem para exibir na área principal
        st.session_state.success_message = f"🎉 Bastão passou de **{current_holder}** para **{next_holder}**!"
        st.session_state.success_message_time = datetime.now()
        
        st.rerun()
    else:
        st.warning('⚠️ Não há próximo(a) consultor(a) elegível na fila.')
        check_and_assume_baton()

def update_status(new_status_part, force_exit_queue=False):
    selected = st.session_state.consultor_selectbox
    st.session_state.gif_warning = False
    st.session_state.rotation_gif_start_time = None
    
    if not selected or selected == 'Selecione um nome':
        st.warning('Selecione um(a) consultor(a).')
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
    


def leave_specific_status(consultor, status_type_to_remove):
    st.session_state.gif_warning = False
    old_status = st.session_state.status_texto.get(consultor, '')
    parts = [p.strip() for p in old_status.split('|')]
    new_parts = [p for p in parts if status_type_to_remove not in p and p]
    new_status = " | ".join(new_parts)
    if not new_status and consultor not in st.session_state.bastao_queue:
        new_status = 'Indisponível'
    st.session_state.status_texto[consultor] = new_status
    check_and_assume_baton()


def enter_from_indisponivel(consultor):
    st.session_state.gif_warning = False
    if consultor not in st.session_state.bastao_queue:
        st.session_state.bastao_queue.append(consultor)
    st.session_state[f'check_{consultor}'] = True
    st.session_state.status_texto[consultor] = ''
    check_and_assume_baton()


def render_fireworks():
    fireworks_css = """
    <style>
    @keyframes firework {
      0% { transform: translate(var(--x), var(--initialY)); width: var(--initialSize); opacity: 1; }
      50% { width: 0.5vmin; opacity: 1; }
      100% { width: var(--finalSize); opacity: 0; }
    }
    .firework,
    .firework::before,
    .firework::after {
      --initialSize: 0.5vmin; --finalSize: 45vmin; --particleSize: 0.2vmin;
      --color1: #ff0000; --color2: #ffd700; --color3: #b22222; --color4: #daa520; --color5: #ff4500; --color6: #b8860b;
      --y: -30vmin; --x: -50%; --initialY: 60vmin;
      content: ""; animation: firework 2s infinite; position: absolute; top: 50%; left: 50%;
      transform: translate(-50%, var(--y)); width: var(--initialSize); aspect-ratio: 1;
      background: radial-gradient(circle, var(--color1) var(--particleSize), #0000 0) 50% 0%,
        radial-gradient(circle, var(--color2) var(--particleSize), #0000 0) 100% 50%,
        radial-gradient(circle, var(--color3) var(--particleSize), #0000 0) 50% 100%,
        radial-gradient(circle, var(--color4) var(--particleSize), #0000 0) 0% 50%,
        radial-gradient(circle, var(--color5) var(--particleSize), #0000 0) 80% 90%,
        radial-gradient(circle, var(--color6) var(--particleSize), #0000 0) 95% 90%;
      background-size: var(--initialSize) var(--initialSize); background-repeat: no-repeat;
    }
    .firework::before { --x: -50%; --y: -50%; --initialY: -50%; transform: translate(-50%, -50%) rotate(40deg) scale(1.3) rotateY(40deg); }
    .firework::after { --x: -50%; --y: -50%; --initialY: -50%; transform: translate(-50%, -50%) rotate(170deg) scale(1.15) rotateY(-30deg); }
    .firework:nth-child(2) { --x: 30vmin; }
    .firework:nth-child(2), .firework:nth-child(2)::before, .firework:nth-child(2)::after {
      --color1: #ff0000; --color2: #ffd700; --color3: #8b0000; --color4: #daa520; --color5: #ff6347; --color6: #f0e68c;  
      --finalSize: 40vmin; left: 30%; top: 60%; animation-delay: -0.25s;
    }
    .firework:nth-child(3) { --x: -30vmin; --y: -50vmin; }
    .firework:nth-child(3), .firework:nth-child(3)::before, .firework:nth-child(3)::after {
      --color1: #ffd700; --color2: #ff4500; --color3: #b8860b; --color4: #cd5c5c; --color5: #800000; --color6: #ffa500;
      --finalSize: 35vmin; left: 70%; top: 60%; animation-delay: -0.4s;
    }
    </style>
    <div class="firework"></div><div class="firework"></div><div class="firework"></div>
    """
    st.markdown(fireworks_css, unsafe_allow_html=True)

def gerar_html_checklist(consultor_nome, camara_nome, data_sessao_formatada):
    consultor_formatado = f"@{consultor_nome}" if not consultor_nome.startswith("@") else consultor_nome
    html_template = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Acompanhamento de Sessão - {camara_nome}</title></head>
<body><div style="font-family: Arial, sans-serif; padding: 20px;">
<h2>Checklist Gerado para {camara_nome}</h2>
<p>Responsável: {consultor_formatado}</p>
<p>Data: {data_sessao_formatada}</p>
<p><em>(HTML gerado pelo sistema - pronto para uso)</em></p>
</div></body></html>
    """
    return html_template

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
        
        consultor = st.session_state.consultor_selectbox
        if consultor and consultor != 'Selecione um nome':
            score = st.session_state.simon_level
            current_ranking = st.session_state.simon_ranking
            found = False
            for entry in current_ranking:
                if entry['nome'] == consultor:
                    if score > entry['score']:
                        entry['score'] = score
                    found = True
                    break
            if not found:
                current_ranking.append({'nome': consultor, 'score': score})
            st.session_state.simon_ranking = sorted(current_ranking, key=lambda x: x['score'], reverse=True)[:5]
            st.success(f"Pontuação salva para {consultor}!")
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

def on_auxilio_change():
    pass  # Placeholder para futuras funcionalidades

def manual_rerun():
    st.session_state.gif_warning = False
    st.session_state.rotation_gif_start_time = None
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

st.set_page_config(page_title="Controle Bastão Cesupe 2026", layout="wide", page_icon="🥂")
init_session_state()
st.components.v1.html("<script>window.scrollTo(0, 0);</script>", height=0)
render_fireworks()

# Header
c_topo_esq, c_topo_dir = st.columns([2, 1], vertical_alignment="bottom")
with c_topo_esq:
    st.markdown(f"""<div style="display: flex; align-items: center; gap: 15px;">
    <h1 style="margin: 0; padding: 0; font-size: 2.2rem; color: #FFD700; text-shadow: 1px 1px 2px #B8860B;">
    Controle Bastão Cesupe 2026 {BASTAO_EMOJI}</h1>
    <img src="{GIF_BASTAO_HOLDER}" style="width: 120px; height: 120px; border-radius: 50%; border: 3px solid #FFD700;">
    </div>""", unsafe_allow_html=True)

with c_topo_dir:
    c_sub1, c_sub2 = st.columns([2, 1], vertical_alignment="bottom")
    with c_sub1:
        novo_responsavel = st.selectbox("Assumir Bastão (Rápido)", options=["Selecione"] + CONSULTORES, 
                                       label_visibility="collapsed", key="quick_enter")
    with c_sub2:
        if st.button("🚀 Entrar", help="Ficar disponível na fila imediatamente"):
            if novo_responsavel and novo_responsavel != "Selecione":
                toggle_queue(novo_responsavel)
                st.session_state.consultor_selectbox = novo_responsavel
                st.success(f"{novo_responsavel} agora está na fila!")
                st.rerun()

st.markdown("<hr style='border: 1px solid #FFD700; margin-top: 5px; margin-bottom: 20px;'>", unsafe_allow_html=True)

# GIFs e avisos
gif_start_time = st.session_state.get('rotation_gif_start_time')
show_gif = False
refresh_interval = 8000

if gif_start_time:
    elapsed = (datetime.now() - gif_start_time).total_seconds()
    if elapsed < 20:
        show_gif = True
        refresh_interval = 2000
    else:
        st.session_state.rotation_gif_start_time = None

st_autorefresh(interval=refresh_interval, key='auto_rerun_key')

if show_gif:
    st.image(GIF_URL_ROTATION, width=200, caption='Bastão Passado!')
if st.session_state.get('gif_warning', False):
    st.error('🚫 Ação inválida! Verifique as regras.')
    st.image(GIF_URL_WARNING, width=150)

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
            consultor = queue[current_check_idx]
            if consultor != responsavel and consultor != proximo and st.session_state.get(f'check_{consultor}'):
                restante.append(consultor)
        current_check_idx = (current_check_idx + 1) % num_q
        checked_count += 1

with col_principal:
    st.header("Responsável pelo Bastão")
    if responsavel:
        bg_color = "linear-gradient(135deg, #FFF8DC 0%, #FFFFFF 100%)"
        border_color = "#FFD700"
        text_color = "#000080"
        st.markdown(f"""<div style="background: {bg_color}; border: 3px solid {border_color}; padding: 25px; 
        border-radius: 15px; display: flex; align-items: center; box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3); margin-bottom: 20px;">
        <div style="flex-shrink: 0; margin-right: 25px;">
        <img src="{GIF_BASTAO_HOLDER}" style="width: 90px; height: 90px; border-radius: 50%; border: 2px solid {border_color};"></div>
        <div><span style="font-size: 14px; color: #555; font-weight: bold; text-transform: uppercase; letter-spacing: 1.5px;">
        Atualmente com:</span><br>
        <span style="font-size: 42px; font-weight: 800; color: {text_color}; line-height: 1.1;">{responsavel}</span>
        </div></div>""", unsafe_allow_html=True)
        
        duration = timedelta()
        if st.session_state.bastao_start_time:
            duration = datetime.now() - st.session_state.bastao_start_time
        st.caption(f"⏱️ Tempo com o bastão: **{format_time_duration(duration)}**")
    else:
        st.markdown('<h2>(Ninguém com o bastão)</h2>', unsafe_allow_html=True)
    
    st.markdown("###")
    st.header("Próximos da Fila")
    
    # Exibir mensagem de sucesso se existir
    if st.session_state.get('success_message') and st.session_state.get('success_message_time'):
        elapsed = (datetime.now() - st.session_state.success_message_time).total_seconds()
        if elapsed < 10:  # Mostra por 10 segundos
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
    st.header("**Consultor(a)**")
    st.selectbox('Selecione:', options=['Selecione um nome'] + CONSULTORES, key='consultor_selectbox', label_visibility='collapsed')
    
    st.markdown("#### ")
    st.markdown("**Ações:**")
    
    row1_c1, row1_c2, row1_c3 = st.columns(3)
    row2_c1, row2_c2, row2_c3, row2_c4, row2_c5 = st.columns(5)
    
    row1_c1.button('🎯 Passar', on_click=rotate_bastao, use_container_width=True, help='Passa o bastão.', type='primary')
    row1_c2.button('📋 Atividades', on_click=toggle_view, args=('menu_atividades',), use_container_width=True)
    row1_c3.button('🏗️ Projeto', on_click=toggle_view, args=('menu_projetos',), use_container_width=True)
    
    row2_c1.button('📅 Reunião', on_click=toggle_view, args=('menu_reuniao',), use_container_width=True)
    row2_c2.button('🍽️ Almoço', on_click=update_status, args=('Almoço', True,), use_container_width=True)
    row2_c3.button('🎙️ Sessão', on_click=toggle_view, args=('menu_sessao',), use_container_width=True)
    row2_c4.button('🚶 Saída', on_click=update_status, args=('Saída rápida', True,), use_container_width=True)
    row2_c5.button('👤 Ausente', on_click=update_status, args=('Ausente', True,), use_container_width=True)
    
    # Menus contextuais
    if st.session_state.active_view == 'menu_atividades':
        with st.container(border=True):
            st.markdown("### Selecione a Atividade")
            c_a1, c_a2 = st.columns([1, 1], vertical_alignment="bottom")
            with c_a1:
                atividades_escolhidas = st.multiselect("Tipo:", OPCOES_ATIVIDADES_STATUS)
            with c_a2:
                texto_extra = st.text_input("Detalhe:", placeholder="Ex: Assunto específico...")
            
            col_confirm_1, col_confirm_2 = st.columns(2)
            with col_confirm_1:
                if st.button("Confirmar Atividade", type="primary", use_container_width=True):
                    if atividades_escolhidas:
                        str_atividades = ", ".join(atividades_escolhidas)
                        status_final = f"Atividade: {str_atividades}"
                        if texto_extra:
                            status_final += f" - {texto_extra}"
                        update_status(status_final)
                        st.session_state.active_view = None
                        st.rerun()
                    else:
                        st.warning("Selecione pelo menos uma atividade.")
            with col_confirm_2:
                if st.button("Cancelar", use_container_width=True, key='cancel_act'):
                    st.session_state.active_view = None
                    st.rerun()
    
    if st.session_state.active_view == 'menu_projetos':
        with st.container(border=True):
            st.markdown("### Selecione o Projeto")
            projeto_escolhido = st.selectbox("Projeto:", OPCOES_PROJETOS)
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                if st.button("Confirmar Projeto", type="primary", use_container_width=True):
                    status_final = f"Projeto: {projeto_escolhido}"
                    update_status(status_final)
                    st.session_state.active_view = None
                    st.rerun()
            with col_p2:
                if st.button("Cancelar", use_container_width=True, key='cancel_proj'):
                    st.session_state.active_view = None
                    st.rerun()
    
    if st.session_state.active_view == 'menu_reuniao':
        with st.container(border=True):
            st.markdown("### Detalhes da Reunião")
            reuniao_desc = st.text_input("Qual reunião?", placeholder="Ex: Alinhamento equipe...")
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                if st.button("Confirmar Reunião", type="primary", use_container_width=True):
                    if reuniao_desc:
                        status_final = f"Reunião: {reuniao_desc}"
                        update_status(status_final)
                        st.session_state.active_view = None
                        st.rerun()
                    else:
                        st.warning("Digite o nome da reunião.")
            with col_r2:
                if st.button("Cancelar", use_container_width=True, key='cancel_reuniao'):
                    st.session_state.active_view = None
                    st.rerun()
    
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
    c_tool1, c_tool2, c_tool3, c_tool4 = st.columns(4)
    c_tool5, c_tool6, c_tool7 = st.columns(3)
    
    c_tool1.button("📑 Checklist", help="Gerador de Checklist Eproc", use_container_width=True, on_click=toggle_view, args=("checklist",))
    c_tool2.button("🆘 Chamados", help="Guia de Abertura de Chamados", use_container_width=True, on_click=toggle_view, args=("chamados",))
    c_tool3.button("📝 Atendimento", help="Registrar Atendimento (Local)", use_container_width=True, on_click=toggle_view, args=("atendimentos",))
    c_tool4.button("⏰ H. Extras", help="Registrar Horas Extras (Local)", use_container_width=True, on_click=toggle_view, args=("hextras",))
    
    c_tool5.button("🧠 Descanso", help="Jogo e Ranking", use_container_width=True, on_click=toggle_view, args=("descanso",))
    c_tool6.button("🐛 Erro/Novidade", help="Relatar Erro (Local)", use_container_width=True, on_click=toggle_view, args=("erro_novidade",))
    c_tool7.button("📊 Relatórios", help="Ver Registros Salvos", use_container_width=True, on_click=toggle_view, args=("relatorios",))
    
    # Views das ferramentas
    if st.session_state.active_view == "checklist":
        with st.container(border=True):
            st.header("Gerador de Checklist (Sessão Eproc)")
            st.markdown("### Gerar HTML")
            data_eproc = st.date_input("Data da Sessão:", format="DD/MM/YYYY", key='sessao_data_input')
            camara_eproc = st.selectbox("Selecione a Câmara:", CAMARAS_OPCOES, index=None, key='sessao_camara_select')
            
            if st.button("Gerar HTML", type="primary", use_container_width=True):
                consultor = st.session_state.consultor_selectbox
                if consultor and consultor != 'Selecione um nome' and camara_eproc:
                    data_formatada = data_eproc.strftime("%d/%m/%Y")
                    html_content = gerar_html_checklist(consultor, camara_eproc, data_formatada)
                    filename = f"Checklist_{data_eproc.strftime('%d-%m-%Y')}.html"
                    st.success("HTML gerado com sucesso!")
                    st.download_button(
                        label=f"⬇️ Baixar {filename}",
                        data=html_content,
                        file_name=filename,
                        mime="text/html"
                    )
                else:
                    st.warning("Preencha todos os campos.")
    
    elif st.session_state.active_view == "chamados":
        with st.container(border=True):
            st.header("Padrão abertura de chamados / jiras")
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
            at_jira = st.text_input("Número do Jira:", value=st.session_state.get('last_jira_number', ""), placeholder="Ex: 1234", key="at_jira_input")
            
            if st.button("Salvar Registro Localmente", type="primary", use_container_width=True):
                consultor = st.session_state.consultor_selectbox
                if consultor and consultor != "Selecione um nome":
                    st.session_state['last_jira_number'] = at_jira
                    st.success("✅ Atendimento registrado localmente!")
                    log_entry = {
                        'timestamp': datetime.now(),
                        'consultor': consultor,
                        'data': at_data,
                        'usuario': at_usuario,
                        'setor': at_nome_setor,
                        'sistema': at_sistema,
                        'descricao': at_descricao,
                        'canal': at_canal,
                        'desfecho': at_desfecho,
                        'jira': at_jira
                    }
                    st.session_state.daily_logs.append(log_entry)
                else:
                    st.error("Selecione um consultor.")
    
    elif st.session_state.active_view == "hextras":
        with st.container(border=True):
            st.markdown("### Registro de Horas Extras (Local)")
            he_data = st.date_input("Data:", value=date.today(), format="DD/MM/YYYY")
            he_inicio = st.time_input("Horário de Início:", value=dt_time(18, 0))
            he_tempo = st.text_input("Tempo Total (ex: 2h30):")
            he_motivo = st.text_input("Motivo da Hora Extra:")
            
            if st.button("Salvar HE Localmente", type="primary", use_container_width=True):
                consultor = st.session_state.consultor_selectbox
                if consultor and consultor != "Selecione um nome":
                    st.success("✅ Horas extras registradas localmente!")
                    he_entry = {
                        'timestamp': datetime.now(),
                        'consultor': consultor,
                        'data': he_data,
                        'inicio': he_inicio,
                        'tempo': he_tempo,
                        'motivo': he_motivo
                    }
                    st.session_state.daily_logs.append(he_entry)
                else:
                    st.error("Selecione um consultor.")
    
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
                consultor = st.session_state.consultor_selectbox
                if consultor and consultor != "Selecione um nome":
                    st.success("✅ Relato salvo localmente!")
                    erro_entry = {
                        'timestamp': datetime.now(),
                        'consultor': consultor,
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
                    st.error("Selecione um consultor.")
    
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
                    consultores_nos_logs = list(set([log.get('consultor', 'N/A') for log in logs]))
                    consultor_filtro = st.selectbox(
                        "Consultor:",
                        ["Todos"] + sorted(consultores_nos_logs)
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
                
                if consultor_filtro != "Todos":
                    logs_filtrados = [l for l in logs_filtrados if l.get('consultor') == consultor_filtro]
                
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
                    consultor = log.get('consultor', 'N/A')
                    
                    # Identifica tipo de registro
                    if 'usuario' in log:
                        # Atendimento
                        with st.expander(f"📝 #{idx} - Atendimento - {consultor} - {data_hora}"):
                            st.markdown(f"**👤 Consultor:** {consultor}")
                            st.markdown(f"**📅 Data:** {log.get('data', 'N/A')}")
                            st.markdown(f"**👥 Usuário:** {log.get('usuario', 'N/A')}")
                            st.markdown(f"**🏢 Setor:** {log.get('setor', 'N/A')}")
                            st.markdown(f"**💻 Sistema:** {log.get('sistema', 'N/A')}")
                            st.markdown(f"**📝 Descrição:** {log.get('descricao', 'N/A')}")
                            st.markdown(f"**📞 Canal:** {log.get('canal', 'N/A')}")
                            st.markdown(f"**✅ Desfecho:** {log.get('desfecho', 'N/A')}")
                            if log.get('jira'):
                                st.markdown(f"**🔢 Jira:** CESUPE-{log.get('jira')}")
                    
                    elif 'inicio' in log and 'tempo' in log:
                        # Horas Extras
                        with st.expander(f"⏰ #{idx} - Horas Extras - {consultor} - {data_hora}"):
                            st.markdown(f"**👤 Consultor:** {consultor}")
                            st.markdown(f"**📅 Data:** {log.get('data', 'N/A')}")
                            st.markdown(f"**🕐 Início:** {log.get('inicio', 'N/A')}")
                            st.markdown(f"**⏱️ Tempo Total:** {log.get('tempo', 'N/A')}")
                            st.markdown(f"**📝 Motivo:** {log.get('motivo', 'N/A')}")
                    
                    elif 'titulo' in log and 'relato' in log:
                        # Erro/Novidade
                        with st.expander(f"🐛 #{idx} - Erro/Novidade - {consultor} - {data_hora}"):
                            st.markdown(f"**👤 Autor:** {consultor}")
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
                    # Exportar para texto
                    if st.button("📥 Exportar como TXT", use_container_width=True):
                        export_text = "=== RELATÓRIO DE REGISTROS ===\n\n"
                        export_text += f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
                        export_text += f"Total de registros: {len(logs_filtrados)}\n\n"
                        export_text += "="*50 + "\n\n"
                        
                        for idx, log in enumerate(logs_filtrados, 1):
                            timestamp = log.get('timestamp', datetime.now())
                            if isinstance(timestamp, str):
                                try:
                                    timestamp = datetime.fromisoformat(timestamp)
                                except:
                                    timestamp = datetime.now()
                            
                            export_text += f"REGISTRO #{idx}\n"
                            export_text += f"Data/Hora: {timestamp.strftime('%d/%m/%Y %H:%M:%S')}\n"
                            export_text += f"Consultor: {log.get('consultor', 'N/A')}\n"
                            
                            if 'usuario' in log:
                                export_text += "Tipo: ATENDIMENTO\n"
                                export_text += f"Usuário: {log.get('usuario', 'N/A')}\n"
                                export_text += f"Sistema: {log.get('sistema', 'N/A')}\n"
                                export_text += f"Descrição: {log.get('descricao', 'N/A')}\n"
                            elif 'inicio' in log:
                                export_text += "Tipo: HORAS EXTRAS\n"
                                export_text += f"Tempo: {log.get('tempo', 'N/A')}\n"
                                export_text += f"Motivo: {log.get('motivo', 'N/A')}\n"
                            elif 'titulo' in log:
                                export_text += "Tipo: ERRO/NOVIDADE\n"
                                export_text += f"Título: {log.get('titulo', 'N/A')}\n"
                            
                            export_text += "\n" + "-"*50 + "\n\n"
                        
                        st.download_button(
                            label="⬇️ Baixar Relatório",
                            data=export_text,
                            file_name=f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain"
                        )

# Coluna lateral (Disponibilidade)
with col_disponibilidade:
    st.markdown("###")
    st.toggle("Auxílio HP/Emails/Whatsapp", key='auxilio_ativo', on_change=on_auxilio_change)
    if st.session_state.get('auxilio_ativo'):
        st.warning("HP/Emails/Whatsapp irão para bastão")
        st.image(GIF_URL_NEDRY, width=300)
    st.markdown("---")
    st.header('Status dos(as) Consultores(as)')
    
    # Listas de status
    import re
    ui_lists = {
        'fila': [],
        'almoco': [],
        'saida': [],
        'ausente': [],
        'atividade_especifica': [],
        'sessao_especifica': [],
        'projeto_especifico': [],
        'reuniao_especifica': [],
        'indisponivel': []
    }
    
    for nome in CONSULTORES:
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
        
        if 'Reunião:' in status:
            match = re.search(r'Reunião: (.*)', status)
            if match:
                ui_lists['reuniao_especifica'].append((nome, match.group(1).split('|')[0].strip()))
        
        if 'Projeto:' in status:
            match = re.search(r'Projeto: (.*)', status)
            if match:
                ui_lists['projeto_especifico'].append((nome, match.group(1).split('|')[0].strip()))
        
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
            if "Projeto" in status_atual:
                extra_info += " 🏗️"
            
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
    render_section_detalhada('Projetos', '🏗️', ui_lists['projeto_especifico'], 'blue', 'Projeto')
    render_section_detalhada('Reuniões', '📅', ui_lists['reuniao_especifica'], 'violet', 'Reunião')
    render_section_simples('Almoço', '🍽️', ui_lists['almoco'], 'red')
    render_section_detalhada('Sessão', '🎙️', ui_lists['sessao_especifica'], 'green', 'Sessão')
    render_section_simples('Saída rápida', '🚶', ui_lists['saida'], 'red')
    render_section_simples('Ausente', '👤', ui_lists['ausente'], 'violet')
    render_section_simples('Indisponível', '❌', ui_lists['indisponivel'], 'grey')

# Footer
st.markdown("---")
st.caption("Sistema de Controle de Bastão - INFORMÁTICA 2026 - Versão Local ")
