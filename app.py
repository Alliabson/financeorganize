import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import calendar
import numpy as np

# --- Configuração da Página ---
st.set_page_config(
    layout="wide",
    page_title="Granazen Finance",
    page_icon="💰",
    initial_sidebar_state="collapsed"
)

# --- CSS Personalizado ---
def apply_custom_css():
    st.markdown("""
    <style>
    :root {
        --primary: #4e73df;
        --primary-light: #7a9ef5;
        --primary-dark: #2c56c8;
        --success: #1cc88a;
        --success-light: #4adfa7;
        --danger: #e74a3b;
        --danger-light: #ff6b5b;
        --warning: #f6c23e;
        --info: #36b9cc;
        --dark: #5a5c69;
        --gray: #858796;
        --light: #f8f9fc;
        --lighter: #fff;
    }
    
    /* Estilo geral */
    .stApp {
        background-color: var(--light);
        font-family: 'Nunito', sans-serif;
        line-height: 1.5;
    }
    
    /* Títulos */
    h1 {
        color: var(--dark);
        font-weight: 700;
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        color: var(--dark);
        font-weight: 600;
        font-size: 1.5rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        color: var(--dark);
        font-weight: 600;
        font-size: 1.2rem;
    }
    
    /* Cards de métricas */
    .metric-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    @media (max-width: 1200px) {
        .metric-container {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    
    @media (max-width: 768px) {
        .metric-container {
            grid-template-columns: 1fr;
        }
    }
    
    .metric-card {
        background: var(--lighter);
        border-radius: 0.5rem;
        padding: 1.5rem;
        box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.1);
        position: relative;
        overflow: hidden;
        border-left: 0.4rem solid;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 0.5rem 2rem 0 rgba(58, 59, 69, 0.2);
    }
    
    .metric-card.primary { border-left-color: var(--primary); }
    .metric-card.success { border-left-color: var(--success); }
    .metric-card.danger { border-left-color: var(--danger); }
    .metric-card.info { border-left-color: var(--info); }
    
    .metric-value {
        font-size: 1.75rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-primary { color: var(--primary); }
    .metric-success { color: var(--success); }
    .metric-danger { color: var(--danger); }
    .metric-info { color: var(--info); }
    
    .metric-title {
        font-size: 0.85rem;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
        color: var(--gray);
        margin-bottom: 0.25rem;
    }
    
    .metric-period {
        font-size: 0.75rem;
        color: var(--gray);
        display: flex;
        align-items: center;
    }
    
    .metric-period i {
        margin-right: 0.3rem;
        font-size: 0.9rem;
    }
    
    /* Formulários */
    .stTextInput input, 
    .stNumberInput input, 
    .stDateInput input, 
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 0.4rem;
        border: 1px solid #d1d3e2;
        padding: 0.6rem 1rem;
        background-color: var(--lighter);
        font-size: 0.95rem;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }
    
    .stTextInput input:focus, 
    .stNumberInput input:focus, 
    .stDateInput input:focus, 
    .stSelectbox div[data-baseweb="select"]:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 0.2rem rgba(78, 115, 223, 0.25);
        outline: none;
    }
    
    .stButton button {
        border-radius: 0.4rem;
        font-weight: 600;
        padding: 0.65rem 1.5rem;
        transition: all 0.3s ease;
        font-size: 0.95rem;
    }
    
    .stButton button.primary {
        background-color: var(--primary);
        border-color: var(--primary);
    }
    
    .stButton button.primary:hover {
        background-color: var(--primary-dark);
        border-color: var(--primary-dark);
        transform: translateY(-2px);
        box-shadow: 0 0.5rem 1rem rgba(78, 115, 223, 0.3);
    }
    
    /* Tabs */
    .stTabs [role="tablist"] {
        border-bottom: 1px solid #e3e6f0;
        margin-bottom: 1.5rem;
    }
    
    .stTabs [role="tab"] {
        padding: 0.75rem 1.25rem;
        color: var(--gray);
        font-weight: 600;
        margin-right: 0.5rem;
        border-radius: 0.4rem 0.4rem 0 0;
        transition: all 0.3s ease;
    }
    
    .stTabs [role="tab"]:hover {
        color: var(--primary);
        background-color: rgba(78, 115, 223, 0.05);
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--primary);
        border-bottom: 3px solid var(--primary);
        background-color: transparent;
    }
    
    /* Dataframe */
    .stDataFrame {
        border-radius: 0.5rem;
        box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.1);
        border: none;
    }
    
    /* Tooltips */
    .stTooltip {
        font-family: 'Nunito', sans-serif;
        border-radius: 0.3rem;
        padding: 0.5rem 1rem;
        box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
    }
    
    /* Seções */
    .section {
        background-color: var(--lighter);
        border-radius: 0.5rem;
        padding: 1.5rem;
        box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.1);
        margin-bottom: 1.5rem;
    }
    
    /* Radio buttons */
    .stRadio [role="radiogroup"] {
        gap: 1rem;
    }
    
    .stRadio [role="radio"] {
        padding: 0.5rem 1rem;
        border-radius: 0.4rem;
        border: 1px solid #d1d3e2;
        transition: all 0.3s ease;
    }
    
    .stRadio [role="radio"][aria-checked="true"] {
        background-color: var(--primary);
        color: white;
        border-color: var(--primary);
    }
    
    /* Ajustes para mobile */
    @media (max-width: 768px) {
        .stRadio [role="radiogroup"] {
            flex-direction: column;
            align-items: flex-start;
        }
    }
    
    /* Ícones */
    .icon {
        margin-right: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

apply_custom_css()

# --- Funções Auxiliares ---
def format_currency(value):
    return f"R$ {value:,.2f}"

def calculate_metrics(df_filtered_current_period, start_date, end_date, prev_month_start, prev_month_end):
    # Métricas para o período atual
    total_receitas = df_filtered_current_period[df_filtered_current_period['Tipo'] == 'Receita']['Valor'].sum() if not df_filtered_current_period.empty else 0
    total_despesas = df_filtered_current_period[df_filtered_current_period['Tipo'] == 'Despesa']['Valor'].sum() if not df_filtered_current_period.empty else 0
    saldo_atual = total_receitas - total_despesas

    prev_month_receitas = 0
    prev_month_despesas = 0
    
    if not st.session_state.df.empty:
        # Garante que a coluna 'Data' do st.session_state.df seja datetime para o cálculo do mês anterior
        df_full_data_copy = st.session_state.df.copy()
        df_full_data_copy['Data'] = pd.to_datetime(df_full_data_copy['Data'], errors='coerce')
        df_full_data_copy = df_full_data_copy.dropna(subset=['Data'])
        
        if not df_full_data_copy.empty:
            df_prev_month_data = df_full_data_copy[
                (df_full_data_copy['Data'].dt.date >= prev_month_start) & 
                (df_full_data_copy['Data'].dt.date <= prev_month_end)
            ]
            prev_month_receitas = df_prev_month_data[df_prev_month_data['Tipo'] == 'Receita']['Valor'].sum() if not df_prev_month_data.empty else 0
            prev_month_despesas = df_prev_month_data[df_prev_month_data['Tipo'] == 'Despesa']['Valor'].sum() if not df_prev_month_data.empty else 0

    prev_month_saldo = prev_month_receitas - prev_month_despesas
    return total_receitas, total_despesas, saldo_atual, prev_month_saldo

def create_monthly_flow_chart(df):
    if df.empty:
        return None
        
    df_monthly = df.copy()
    df_monthly['Mês'] = df_monthly['Data'].dt.to_period('M').astype(str)
    monthly_summary = df_monthly.groupby(['Mês', 'Tipo'])['Valor'].sum().unstack().fillna(0)
    
    # Garante que as colunas 'Receita' e 'Despesa' existam
    for tipo in ['Receita', 'Despesa']:
        if tipo not in monthly_summary.columns:
            monthly_summary[tipo] = 0
    
    # Ordena os meses para garantir a sequência correta no gráfico
    monthly_summary.index = pd.PeriodIndex(monthly_summary.index, freq='M')
    monthly_summary = monthly_summary.sort_index()
    monthly_summary.index = monthly_summary.index.astype(str) # Converte de volta para string para Plotly

    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=monthly_summary.index,
        y=monthly_summary['Receita'],
        name='Receitas',
        marker_color='#1cc88a',
        hovertemplate='<b>%{x}</b><br>Receitas: R$ %{y:,.2f}<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        x=monthly_summary.index,
        y=-monthly_summary['Despesa'],
        name='Despesas',
        marker_color='#e74a3b',
        hovertemplate='<b>%{x}</b><br>Despesas: R$ %{y:,.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Fluxo Mensal de Receitas e Despesas',
        barmode='relative',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified',
        height=450,
        margin=dict(t=50, b=50, l=50, r=50),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(
            showgrid=False,
            tickangle=-45
        ),
        yaxis=dict(
            gridcolor='#e3e6f0',
            tickprefix="R$ "
        )
    )
    
    return fig

def create_expense_pie_chart(df):
    df_despesas = df[df['Tipo'] == 'Despesa']
    if df_despesas.empty:
        return None
    
    expense_by_category = df_despesas.groupby('Categoria')['Valor'].sum().reset_index()
    
    fig = px.pie(
        expense_by_category,
        values='Valor',
        names='Categoria',
        title='Distribuição das Despesas por Categoria',
        hole=0.5,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Valor: R$ %{value:,.2f}<br>Percentual: %{percent}<extra></extra>',
        marker=dict(line=dict(color='#fff', width=1))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=450,
        showlegend=False,
        margin=dict(t=50, b=50, l=50, r=50),
        uniformtext_minsize=12,
        uniformtext_mode='hide'
    )
    
    return fig

def create_balance_chart(df):
    if df.empty:
        return None
        
    df_saldo = df.copy()
    df_saldo = df_saldo.sort_values('Data')
    df_saldo['Valor_Ajustado'] = df_saldo.apply(
        lambda x: x['Valor'] if x['Tipo'] == 'Receita' else -x['Valor'], axis=1
    )
    df_saldo['Saldo_Acumulado'] = df_saldo['Valor_Ajustado'].cumsum()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_saldo['Data'],
        y=df_saldo['Saldo_Acumulado'],
        mode='lines+markers',
        name='Saldo Acumulado',
        line=dict(color='#4e73df', width=3),
        marker=dict(size=8, color='#4e73df'),
        hovertemplate='<b>%{x|%d/%m/%Y}</b><br>Saldo: R$ %{y:,.2f}<extra></extra>',
        fill='tozeroy',
        fillcolor='rgba(78, 115, 223, 0.1)'
    ))
    
    fig.update_layout(
        title='Evolução do Saldo Acumulado',
        xaxis_title='Data',
        yaxis_title='Saldo (R$)',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=450,
        hovermode='x unified',
        margin=dict(t=50, b=50, l=50, r=50),
        xaxis=dict(
            showgrid=False,
            tickformat='%d/%m'
        ),
        yaxis=dict(
            gridcolor='#e3e6f0',
            tickprefix="R$ "
        )
    )
    
    return fig

# --- Inicialização de Dados ---
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['Data', 'Descrição', 'Valor', 'Tipo', 'Categoria'])
    
    # Dados de exemplo
    example_data = {
        'Data': [
            datetime(2024, 1, 10), datetime(2024, 1, 15), datetime(2024, 1, 20),
            datetime(2024, 2, 5), datetime(2024, 2, 12), datetime(2024, 2, 20),
            datetime(2024, 3, 1), datetime(2024, 3, 10), datetime(2024, 3, 15),
            datetime(2024, 3, 25), datetime(2024, 4, 5), datetime(2024, 4, 15)
        ],
        'Descrição': [
            'Salário', 'Aluguel', 'Supermercado',
            'Freelance', 'Transporte', 'Restaurante',
            'Bônus', 'Conta de Luz', 'Internet',
            'Presente', 'Salário', 'Academia'
        ],
        'Valor': [
            3000.00, 1500.00, 450.00,
            1200.00, 120.00, 80.00,
            500.00, 200.00, 90.00,
            150.00, 3000.00, 120.00
        ],
        'Tipo': [
            'Receita', 'Despesa', 'Despesa',
            'Receita', 'Despesa', 'Despesa',
            'Receita', 'Despesa', 'Despesa',
            'Despesa', 'Receita', 'Despesa'
        ],
        'Categoria': [
            'Salário', 'Moradia', 'Alimentação',
            'Freelance', 'Transporte', 'Lazer',
            'Bônus', 'Moradia', 'Moradia',
            'Lazer', 'Salário', 'Saúde'
        ]
    }
    st.session_state.df = pd.DataFrame(example_data)
    st.session_state.df['Data'] = pd.to_datetime(st.session_state.df['Data'])

# --- Header ---
col1, col2 = st.columns([1, 3])
with col1:
    st.image("https://placehold.co/150x50/4e73df/ffffff?text=Granazen", width=150) # Placeholder com cor primária
with col2:
    st.title("Dashboard Financeiro")

st.markdown("Visualize e analise suas finanças pessoais com insights poderosos")

# --- Seção 1: Gerenciar Lançamentos ---
st.header("📝 Gerenciar Lançamentos")
tab1, tab2 = st.tabs(["📤 Carregar CSV", "✏️ Inserir Manualmente"])

with tab1:
    st.subheader("Carregar Extrato Bancário")
    uploaded_file = st.file_uploader(
        "Selecione seu arquivo CSV",
        type="csv",
        help="O arquivo deve conter colunas: Data, Descrição, Valor, Tipo, Categoria",
        key="file_uploader"
    )
    
    if uploaded_file is not None:
        try:
            temp_df = pd.read_csv(uploaded_file)
            required_cols = ['Data', 'Descrição', 'Valor', 'Tipo', 'Categoria']
            if all(col in temp_df.columns for col in required_cols):
                st.session_state.df = temp_df
                # Garante que a coluna 'Data' seja datetime após o upload
                st.session_state.df['Data'] = pd.to_datetime(st.session_state.df['Data'], errors='coerce')
                st.session_state.df = st.session_state.df.dropna(subset=['Data'])
                st.success("Dados carregados com sucesso!")
                
                with st.expander("Visualizar dados carregados"):
                    st.dataframe(st.session_state.df.head(), use_container_width=True)
                st.rerun() # Recarrega para aplicar os novos dados
            else:
                missing_cols = [col for col in required_cols if col not in temp_df.columns]
                st.error(f"O arquivo não contém todas as colunas necessárias. Faltando: {', '.join(missing_cols)}")
        except Exception as e:
            st.error(f"Erro ao processar arquivo: {str(e)}")

with tab2:
    st.subheader("Adicionar Transação Manual")
    with st.form("transaction_form", clear_on_submit=True):
        cols = st.columns([1, 1, 1])
        
        with cols[0]:
            data = st.date_input("Data*", value=datetime.now())
            tipo = st.selectbox("Tipo*", ["Receita", "Despesa"])
        
        with cols[1]:
            valor = st.number_input("Valor (R$)*", min_value=0.01, format="%.2f", step=0.01)
            categoria = st.selectbox(
                "Categoria*",
                ["Moradia", "Alimentação", "Transporte", "Lazer", "Saúde", "Educação", "Outros", "Salário", "Freelance", "Bônus"] # Adicionado categorias de exemplo
            )
        
        with cols[2]:
            descricao = st.text_input("Descrição*")
            st.markdown("<div style='height: 27px;'></div>", unsafe_allow_html=True) # Espaçamento para alinhar o botão
            submitted = st.form_submit_button("💾 Salvar Transação", type="primary")
        
        if submitted:
            if descricao and valor:
                new_entry = pd.DataFrame([{
                    'Data': data,
                    'Descrição': descricao,
                    'Valor': valor,
                    'Tipo': tipo,
                    'Categoria': categoria
                }])
                st.session_state.df = pd.concat([st.session_state.df, new_entry], ignore_index=True)
                # Garante que a coluna 'Data' seja datetime após adicionar nova entrada
                st.session_state.df['Data'] = pd.to_datetime(st.session_state.df['Data'], errors='coerce')
                st.success("Transação adicionada com sucesso!")
                st.rerun()
            else:
                st.warning("Preencha todos os campos obrigatórios (*)")

# --- Filtro de Período ---
st.header("🔍 Filtros de Período")
col1, col2, col3 = st.columns([2, 3, 1])

with col1:
    period = st.radio(
        "Período",
        ["Hoje", "Esta Semana", "Este Mês", "Personalizado"],
        horizontal=True,
        key="period_radio"
    )

with col2:
    # Define valores padrão para o date_input para evitar erro de valor vazio
    default_start_date = datetime.now().date().replace(day=1)
    default_end_date = (datetime.now().date().replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)

    if period == "Personalizado":
        date_range = st.date_input(
            "Selecione o período",
            value=[default_start_date, default_end_date], # Define um valor padrão
            label_visibility="collapsed",
            key="date_range_picker"
        )
        if len(date_range) == 2:
            start_date, end_date = date_range
        elif len(date_range) == 1: # Se apenas uma data for selecionada, considera como período de um dia
            start_date = end_date = date_range[0]
        else: # Se nada for selecionado, usa o padrão
            start_date = default_start_date
            end_date = default_end_date
    else:
        today = datetime.now().date()
        if period == "Hoje":
            start_date = end_date = today
        elif period == "Esta Semana":
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)
        else:  # Este Mês
            start_date = today.replace(day=1)
            end_date = (today.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)

with col3:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    if st.button("🔄 Limpar Filtros", key="clear_filters"):
        # Reseta para o período "Este Mês" ao limpar
        period = "Este Mês"
        start_date = datetime.now().date().replace(day=1)
        end_date = (datetime.now().date().replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
        st.session_state.period_radio = "Este Mês" # Atualiza o estado do radio button
        st.rerun()

# Filtra os dados
df_filtered = pd.DataFrame() # Inicializa como DataFrame vazio
if not st.session_state.df.empty:
    # Garante que a coluna 'Data' seja datetime antes de filtrar
    df_temp = st.session_state.df.copy()
    df_temp['Data'] = pd.to_datetime(df_temp['Data'], errors='coerce')
    df_temp = df_temp.dropna(subset=['Data']) # Remove linhas com datas inválidas
    
    df_filtered = df_temp[
        (df_temp['Data'].dt.date >= start_date) & 
        (df_temp['Data'].dt.date <= end_date)
    ].copy()


# --- Cards de Métricas ---
st.header("📊 Visão Geral")

if not df_filtered.empty:
    # Calcula o período do mês anterior para a métrica de variação
    # O mês anterior é calculado em relação ao início do 'start_date' do filtro atual.
    # Ex: se o filtro atual é Fev 2024, o mês anterior é Jan 2024.
    first_day_current_filter_month = start_date.replace(day=1)
    last_day_prev_filter_month = first_day_current_filter_month - timedelta(days=1)
    first_day_prev_filter_month = last_day_prev_filter_month.replace(day=1)

    total_receitas, total_despesas, saldo_atual, prev_month_saldo = calculate_metrics(
        df_filtered, start_date, end_date,
        first_day_prev_filter_month, last_day_prev_filter_month
    )
    
    # Calcula variação em relação ao mês anterior
    if prev_month_saldo != 0:
        saldo_variation = ((saldo_atual - prev_month_saldo) / abs(prev_month_saldo)) * 100
    else:
        saldo_variation = 0 # Ou np.nan se preferir não mostrar %
    
    cols = st.columns(4)
    with cols[0]:
        st.markdown(f"""
        <div class="metric-card primary">
            <div class="metric-title">Saldo Total</div>
            <div class="metric-value metric-primary">{format_currency(saldo_atual)}</div>
            <div class="metric-period">
                <i>📅</i> {start_date.strftime('%d/%m')} - {end_date.strftime('%d/%m/%Y')}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown(f"""
        <div class="metric-card success">
            <div class="metric-title">Receitas</div>
            <div class="metric-value metric-success">{format_currency(total_receitas)}</div>
            <div class="metric-period">
                <i>📈</i> {len(df_filtered[df_filtered['Tipo'] == 'Receita'])} transações
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[2]:
        st.markdown(f"""
        <div class="metric-card danger">
            <div class="metric-title">Despesas</div>
            <div class="metric-value metric-danger">{format_currency(total_despesas)}</div>
            <div class="metric-period">
                <i>📉</i> {len(df_filtered[df_filtered['Tipo'] == 'Despesa'])} transações
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[3]:
        variation_icon = "🟢" if saldo_variation >= 0 else "🔴"
        variation_text = f"{variation_icon} {abs(saldo_variation):.1f}% vs mês anterior"
        
        st.markdown(f"""
        <div class="metric-card info">
            <div class="metric-title">Variação do Saldo</div>
            <div class="metric-value metric-info">{variation_text}</div>
            <div class="metric-period">
                <i>🔄</i> Mês anterior: {format_currency(prev_month_saldo)}
            </div>
        </div>
        """, unsafe_allow_html=True)

else:
    st.info("Nenhuma transação encontrada para o período selecionado. Carregue dados ou adicione transações para ver as métricas.")

# --- Gráficos Principais ---
st.header("📈 Análise Detalhada")

if not df_filtered.empty:
    tab1, tab2, tab3 = st.tabs(["Fluxo Mensal", "Distribuição de Despesas", "Evolução do Saldo"])
    
    with tab1:
        fig1 = create_monthly_flow_chart(df_filtered)
        if fig1:
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.warning("Não há dados suficientes para exibir o gráfico de fluxo mensal.")
    
    with tab2:
        fig2 = create_expense_pie_chart(df_filtered)
        if fig2:
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("Nenhuma despesa encontrada no período selecionado para o gráfico de pizza.")
    
    with tab3:
        fig3 = create_balance_chart(df_filtered)
        if fig3:
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.warning("Não há dados suficientes para exibir o gráfico de evolução do saldo.")

# --- Tabela de Transações ---
st.header("🧾 Últimas Transações")
if not df_filtered.empty:
    search_query = st.text_input("🔍 Pesquisar transações", key="search_transactions")
    
    if search_query:
        df_display = df_filtered[
            df_filtered['Descrição'].str.contains(search_query, case=False, na=False) |
            df_filtered['Categoria'].str.contains(search_query, case=False, na=False)
        ]
    else:
        df_display = df_filtered
    
    st.dataframe(
        df_display.sort_values('Data', ascending=False)[['Data', 'Descrição', 'Valor', 'Tipo', 'Categoria']],
        column_config={
            "Data": st.column_config.DateColumn("Data", format="DD/MM/YYYY"),
            "Valor": st.column_config.NumberColumn("Valor (R$)", format="%.2f"),
            "Tipo": st.column_config.TextColumn("Tipo"),
            "Categoria": st.column_config.TextColumn("Categoria")
        },
        use_container_width=True,
        hide_index=True,
        height=400
    )
else:
    st.info("Nenhuma transação encontrada para o período selecionado")

# --- Rodapé ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: var(--gray); font-size: 0.9rem;">
    <p><strong>Granazen Finance Dashboard</strong> · Desenvolvido com Streamlit · Estilo inspirado no Granazen</p>
    <p>© 2024 Todos os direitos reservados</p>
</div>
""", unsafe_allow_html=True)
