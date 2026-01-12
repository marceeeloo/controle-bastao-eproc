import streamlit as st
import time
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# ============================================
# CONFIGURAÇÕES E CONSTANTES
# ============================================

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

OPCOES_STATUS = [
    "HP", "E-mail", "WhatsApp", 
    "Treinamento", "Reunião",
    "Almoço", "Ausente", "Saída rápida", 
]

GIF_BASTAO = "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExa3Uwazd5cnNra2oxdDkydjZkcHdqcWN2cng0Y2N0cmNmN21vYXVzMiZlcD12MV9pbnRlcm5uYWxfZ2lmX2J5X2lkJmN0PWc/3rXs5J0hZkXwTZjuvM/giphy.gif"
GIF_ROTATION = "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExdmx4azVxbGt4Mnk1cjMzZm5sMmp1YThteGJsMzcyYmhsdmFoczV0aSZlcD12MV9pbnRlcm5uYWxfZ2lmX2J5X2lkJmN0PWc/JpkZEKWY0s9QI4DGvF/giphy.gif"
GIF_WARNING = "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExY2pjMDN0NGlvdXp1aHZ1ejJqMnY5MG1yZmN0d3NqcDl1bTU1dDJrciZlcD12MV9pbnRlcm5uYWxfZ2lmX2J5X2lkJmN0PWc/fXnRObM8Q0RkOmR5nf/giphy.gif"

# ============================================
# FUNÇÕES AUXILIARES
# ============================================

def format_time_duration(duration):
    """Formata timedelta para HH:MM:SS"""
    if not isinstance(duration, timedelta):
        return '--:--:--'
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
    }
    
    for key, default in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default
    
    # Inicializa checkboxes
    for nome in CONSULTORES:
        if f'check_{nome}' not in st.session_state:
            st.session_state[f'check_{nome}'] = False

def find_next_holder_index(current_index, queue):
    """Encontra o próximo consultor elegível na fila"""
    if not queue:
        return -1
    
    num_consultores = len(queue)
    if num_consultores == 0:
        return -1
        
    next_idx = (current_index + 1) % num_consultores
    attempts = 0
    
    while attempts < num_consultores:
        consultor = queue[next_idx]
        if st.session_state.get(f'check_{consultor}'):
            return next_idx
        next_idx = (next_idx + 1) % num_consultores
        attempts += 1
    
    return -1

def check_and_assume_baton():
    """Verifica e atribui o bastão automaticamente"""
    queue = st.session_state.bastao_queue
    current_holder = next((c for c, s in st.session_state.status_texto.items() 
                          if 'Bastão' in s), None)
    
    is_current_valid = (current_holder and current_holder in queue and 
                       st.session_state.get(f'check_{current_holder}'))
    
    first_eligible_index = find_next_holder_index(-1, queue)
    first_eligible_holder = queue[first_eligible_index] if first_eligible_index != -1 else None
    
    should_have_baton = None
    if is_current_valid:
        should_have_baton = current_holder
    elif first_eligible_holder:
        should_have_baton = first_eligible_holder

    changed = False

    # Remove bastão de quem não deveria ter
    for c in CONSULTORES:
        s_text = st.session_state.status_texto.get(c, '')
        if c != should_have_baton and 'Bastão' in s_text:
            st.session_state.status_texto[c] = 'Indisponível'
            changed = True

    # Dá bastão para quem deveria ter
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
    """Adiciona ou remove consultor da fila"""
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
    """Passa o bastão para o próximo consultor"""
    selected = st.session_state.consultor_selectbox
    st.session_state.gif_warning = False
    st.session_state.rotation_gif_start_time = None
    
    if not selected or selected == 'Selecione um nome':
        st.warning('Selecione um(a) consultor(a).')
        return
    
    queue = st.session_state.bastao_queue
    current_holder = next((c for c, s in st.session_state.status_texto.items() 
                          if 'Bastão' in s), None)
    
    # Validação: só pode passar se for o atual detentor
    if selected != current_holder:
        st.session_state.gif_warning = True
        return

    try:
        current_index = queue.index(current_holder)
    except ValueError:
        check_and_assume_baton()
        return

    # Encontra o próximo elegível
    next_idx = find_next_holder_index(current_index, queue)
    
    if next_idx != -1:
        next_holder = queue[next_idx]
        
        # Remove bastão do atual
        old_h_status = st.session_state.status_texto[current_holder]
        new_h_status = old_h_status.replace('Bastão | ', '').replace('Bastão', '').strip()
        if not new_h_status:
            new_h_status = ''
        st.session_state.status_texto[current_holder] = new_h_status
        
        # Dá bastão ao próximo
        old_n_status = st.session_state.status_texto.get(next_holder, '')
        new_n_status = f"Bastão | {old_n_status}" if old_n_status else "Bastão"
        st.session_state.status_texto[next_holder] = new_n_status
        st.session_state.bastao_start_time = datetime.now()
        
        # Incrementa contador
        st.session_state.bastao_counts[current_holder] = st.session_state.bastao_counts.get(current_holder, 0) + 1
        
        # Efeitos visuais
        st.session_state.rotation_gif_start_time = datetime.now()
        st.success(f"🎉 Bastão passou de **{current_holder}** para **{next_holder}**!")
    else:
        st.warning('Não há próximo(a) consultor(a) elegível na fila no momento.')
        check_and_assume_baton()

def update_status(new_status):
    """Atualiza o status do consultor selecionado"""
    selected = st.session_state.consultor_selectbox
    st.session_state.gif_warning = False
    st.session_state.rotation_gif_start_time = None
    
    if not selected or selected == 'Selecione um nome':
        st.warning('Selecione um(a) consultor(a).')
        return

    blocking_statuses = ['Almoço', 'Ausente', 'Saída rápida']
    should_exit_queue = new_status in blocking_statuses
    
    if should_exit_queue:
        st.session_state[f'check_{selected}'] = False
        if selected in st.session_state.bastao_queue:
            st.session_state.bastao_queue.remove(selected)
        final_status = new_status
    else:
        current = st.session_state.status_texto.get(selected, '')
        parts = [p.strip() for p in current.split('|') if p.strip()]
        
        cleaned_parts = []
        for p in parts:
            if p == 'Indisponível':
                continue
            cleaned_parts.append(p)
        
        cleaned_parts.append(new_status)
        cleaned_parts.sort(key=lambda x: 0 if 'Bastão' in x else 1)
        final_status = " | ".join(cleaned_parts)
    
    was_holder = next((True for c, s in st.session_state.status_texto.items() 
                      if 'Bastão' in s and c == selected), False)
    
    if was_holder and not should_exit_queue:
        if 'Bastão' not in final_status:
            final_status = f"Bastão | {final_status}"
    
    st.session_state.status_texto[selected] = final_status
    
    if was_holder and should_exit_queue:
        check_and_assume_baton()

def enter_from_indisponivel(consultor):
    """Coloca consultor indisponível na fila"""
    st.session_state.gif_warning = False
    if consultor not in st.session_state.bastao_queue:
        st.session_state.bastao_queue.append(consultor)
    st.session_state[f'check_{consultor}'] = True
    st.session_state.status_texto[consultor] = ''
    check_and_assume_baton()

def leave_status(consultor, status_to_remove):
    """Remove um status específico do consultor"""
    st.session_state.gif_warning = False
    old_status = st.session_state.status_texto.get(consultor, '')
    
    parts = [p.strip() for p in old_status.split('|')]
    new_parts = [p for p in parts if status_to_remove not in p and p]
    
    new_status = " | ".join(new_parts)
    if not new_status and consultor not in st.session_state.bastao_queue:
        new_status = 'Indisponível'
    
    st.session_state.status_texto[consultor] = new_status
    check_and_assume_baton()

# ============================================
# INTERFACE PRINCIPAL
# ============================================

st.set_page_config(
    page_title="Controle de Bastão - CESUPE",
    layout="wide",
    page_icon="🥂"
)

init_session_state()

# Auto-refresh a cada 5 segundos
gif_start_time = st.session_state.get('rotation_gif_start_time')
show_gif = False
refresh_interval = 5000

if gif_start_time:
    elapsed = (datetime.now() - gif_start_time).total_seconds()
    if elapsed < 10:
        show_gif = True
        refresh_interval = 2000
    else:
        st.session_state.rotation_gif_start_time = None

st_autorefresh(interval=refresh_interval, key='auto_rerun')

# Header
st.markdown("""
<div style="text-align: center; padding: 20px;">
    <h1 style="color: #FFD700; text-shadow: 2px 2px 4px #B8860B;">
        🥂 Controle de Bastão - CESUPE
    </h1>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border: 1px solid #FFD700;'>", unsafe_allow_html=True)

# Avisos visuais
if show_gif:
    st.image(GIF_ROTATION, width=200, caption='Bastão Passado!')

if st.session_state.get('gif_warning', False):
    st.error('🚫 Ação inválida! Apenas quem tem o bastão pode passá-lo.')
    st.image(GIF_WARNING, width=150)

# Layout principal
col_principal, col_lateral = st.columns([1.5, 1])

# Coluna Principal
with col_principal:
    st.header("🎯 Responsável pelo Bastão")
    
    queue = st.session_state.bastao_queue
    responsavel = next((c for c, s in st.session_state.status_texto.items() 
                       if 'Bastão' in s), None)
    
    if responsavel:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FFF8DC 0%, #FFFFFF 100%); 
                    border: 3px solid #FFD700; 
                    padding: 25px; 
                    border-radius: 15px; 
                    text-align: center;
                    box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);">
            <img src="{GIF_BASTAO}" style="width: 90px; height: 90px; border-radius: 50%; margin-bottom: 15px;">
            <h2 style="color: #000080; margin: 0;">{responsavel}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        duration = timedelta()
        if st.session_state.bastao_start_time:
            duration = datetime.now() - st.session_state.bastao_start_time
        st.caption(f"⏱️ Tempo com o bastão: **{format_time_duration(duration)}**")
    else:
        st.info("Ninguém com o bastão no momento")
    
    st.markdown("---")
    
    # Próximos da fila
    st.subheader("📋 Próximos na Fila")
    
    if responsavel and responsavel in queue:
        current_index = queue.index(responsavel)
        proximo_index = find_next_holder_index(current_index, queue)
        
        if proximo_index != -1:
            proximo = queue[proximo_index]
            st.markdown(f"### 1º: **{proximo}**")
            
            # Demais
            restante = []
            next_check = (proximo_index + 1) % len(queue)
            while next_check != current_index:
                c = queue[next_check]
                if c != responsavel and st.session_state.get(f'check_{c}'):
                    restante.append(c)
                next_check = (next_check + 1) % len(queue)
            
            if restante:
                st.markdown(f"**Demais:** {', '.join(restante)}")
        else:
            st.info("Apenas o responsável atual está elegível")
    else:
        if queue:
            st.markdown(f"**Próximo:** {queue[0]}")
            if len(queue) > 1:
                st.markdown(f"**Demais:** {', '.join(queue[1:])}")
        else:
            st.info("Ninguém na fila")
    
    st.markdown("---")
    
    # Ações
    st.subheader("⚙️ Ações")
    st.selectbox(
        'Selecione um consultor:',
        options=['Selecione um nome'] + CONSULTORES,
        key='consultor_selectbox'
    )
    
    st.markdown("####")
    
    # Botão Passar (destacado)
    st.button(
        '🎯 PASSAR BASTÃO',
        on_click=rotate_bastao,
        use_container_width=True,
        type='primary',
        help='Passa o bastão para o próximo da fila'
    )
    
    st.markdown("###")
    
    # Outros botões de status
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button('📋 HP/Email', use_container_width=True):
            update_status('HP/Email')
    
    with col2:
        if st.button('💼 Reunião', use_container_width=True):
            update_status('Reunião')
    
    with col3:
        if st.button('🍽️ Almoço', use_container_width=True):
            update_status('Almoço')
    
    with col4:
        if st.button('🚶 Saída', use_container_width=True):
            update_status('Saída rápida')
    
    st.markdown("---")
    
    # Estatísticas do dia
    st.subheader("📊 Estatísticas do Dia")
    counts_today = st.session_state.bastao_counts
    consultores_ativos = [(nome, count) for nome, count in counts_today.items() if count > 0]
    
    if consultores_ativos:
        consultores_ativos.sort(key=lambda x: x[1], reverse=True)
        for nome, count in consultores_ativos[:5]:
            st.markdown(f"**{nome}**: {count} vez(es) com o bastão")
    else:
        st.info("Nenhuma atividade registrada hoje")

# Coluna Lateral
with col_lateral:
    st.header("👥 Consultores")
    
    # Separar por status
    fila = []
    almoco = []
    ausente = []
    saida = []
    outros = []
    indisponivel = []
    
    for nome in CONSULTORES:
        if nome in st.session_state.bastao_queue:
            fila.append(nome)
        
        status = st.session_state.status_texto.get(nome, 'Indisponível')
        
        if status == 'Almoço':
            almoco.append(nome)
        elif status == 'Ausente':
            ausente.append(nome)
        elif status == 'Saída rápida':
            saida.append(nome)
        elif status == 'Indisponível' and nome not in fila:
            indisponivel.append(nome)
        elif status and status != '' and nome not in fila:
            outros.append(nome)
    
    # Renderizar seções
    st.subheader(f"✅ Na Fila ({len(fila)})")
    if fila:
        for nome in fila:
            col_nome, col_check = st.columns([0.8, 0.2])
            with col_check:
                st.checkbox(
                    ' ',
                    key=f'check_fila_{nome}',
                    value=True,
                    on_change=toggle_queue,
                    args=(nome,),
                    label_visibility='collapsed'
                )
            with col_nome:
                if nome == responsavel:
                    st.markdown(f"🥂 **{nome}**")
                else:
                    st.markdown(f"**{nome}**")
    else:
        st.info("Ninguém na fila")
    
    st.markdown("---")
    
    if almoco:
        st.subheader(f"🍽️ Almoço ({len(almoco)})")
        for nome in almoco:
            col_nome, col_check = st.columns([0.8, 0.2])
            with col_check:
                st.checkbox(
                    ' ',
                    key=f'check_almoco_{nome}',
                    value=True,
                    on_change=leave_status,
                    args=(nome, 'Almoço'),
                    label_visibility='collapsed'
                )
            with col_nome:
                st.markdown(f"**{nome}**")
        st.markdown("---")
    
    if saida:
        st.subheader(f"🚶 Saída Rápida ({len(saida)})")
        for nome in saida:
            col_nome, col_check = st.columns([0.8, 0.2])
            with col_check:
                st.checkbox(
                    ' ',
                    key=f'check_saida_{nome}',
                    value=True,
                    on_change=leave_status,
                    args=(nome, 'Saída rápida'),
                    label_visibility='collapsed'
                )
            with col_nome:
                st.markdown(f"**{nome}**")
        st.markdown("---")
    
    if ausente:
        st.subheader(f"👤 Ausente ({len(ausente)})")
        for nome in ausente:
            col_nome, col_check = st.columns([0.8, 0.2])
            with col_check:
                st.checkbox(
                    ' ',
                    key=f'check_ausente_{nome}',
                    value=True,
                    on_change=leave_status,
                    args=(nome, 'Ausente'),
                    label_visibility='collapsed'
                )
            with col_nome:
                st.markdown(f"**{nome}**")
        st.markdown("---")
    
    if outros:
        st.subheader(f"💼 Em Atividade ({len(outros)})")
        for nome in outros:
            status = st.session_state.status_texto.get(nome, '')
            st.markdown(f"**{nome}**: {status}")
        st.markdown("---")
    
    st.subheader(f"❌ Indisponíveis ({len(indisponivel)})")
    if indisponivel:
        for nome in indisponivel:
            col_nome, col_check = st.columns([0.8, 0.2])
            with col_check:
                st.checkbox(
                    ' ',
                    key=f'check_indis_{nome}',
                    value=False,
                    on_change=enter_from_indisponivel,
                    args=(nome,),
                    label_visibility='collapsed'
                )
            with col_nome:
                st.markdown(f"{nome}")
    else:
        st.info("Todos disponíveis")

# Footer
st.markdown("---")
st.caption("Sistema de Controle de Bastão - Informática 2026")
