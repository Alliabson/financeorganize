import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.ticker as mticker
import calendar # Para obter o nome do mês
import numpy as np # Adicionado para operações numéricas

# --- Configuração da Página ---
st.set_page_config(layout="wide", page_title="Painel Financeiro Granazen-like")

# --- Funções Auxiliares de Estilo ---
def apply_custom_css():
    st.markdown("""
    <style>
    /* Estilo geral do aplicativo */
    .stApp {
        background-color: #f0f2f6; /* Cor de fundo clara */
        color: #333; /* Cor do texto padrão */
        font-family: "Inter", sans-serif; /* Fonte Inter para um visual moderno */
    }

    /* Títulos principais */
    h1, h2, h3, h4, h5, h6 {
        color: #333;
    }

    /* Estilo para os cards de métricas (Receitas, Despesas, Saldo) */
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px; /* Cantos arredondados */
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.08); /* Sombra suave e discreta */
        text-align: left;
        height: 100%; /* Garante que os cards tenham a mesma altura */
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        border: 1px solid #e0e0e0; /* Borda sutil */
    }
    .metric-card h3 {
        margin-top: 0;
        color: #666; /* Título da métrica mais suave */
        font-size: 1em;
        font-weight: normal;
    }
    .metric-card .stMetric {
        padding: 0;
    }
    .metric-card .stMetric > div:first-child { /* Título da métrica */
        color: #666;
        font-size: 0.9em;
    }
    .metric-card .stMetric > div:nth-child(2) { /* Valor da métrica */
        font-size: 1.6em; /* Um pouco menor para caber melhor */
        font-weight: bold;
        color: #333;
    }
    .metric-card .stMetric > div:nth-child(3) { /* Delta da métrica */
        font-size: 0.8em;
        color: #888;
    }

    /* Estilo para as seções de conteúdo (tabelas, gráficos, formulários) */
    .content-section {
        background-color: white;
        padding: 25px; /* Mais padding para espaçamento interno */
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); /* Sombra um pouco mais visível para seções */
        margin-bottom: 20px;
        border: 1px solid #e0e0e0; /* Borda sutil */
    }

    /* Estilo para campos de input (texto, número) */
    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input {
        border-radius: 8px; /* Cantos arredondados */
        border: 1px solid #d0d0d0; /* Borda cinza suave */
        padding: 10px 12px;
        background-color: #ffffff; /* Fundo branco puro */
        box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.03); /* Sombra interna mais sutil */
        transition: all 0.2s ease-in-out; /* Transição suave para o foco */
    }
    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stNumberInput"] input:focus {
        border-color: #28a745; /* Borda verde no foco */
        box-shadow: 0 0 0 2px rgba(40, 167, 69, 0.15); /* Sombra de foco verde mais suave */
        outline: none; /* Remove outline padrão do navegador */
    }

    /* Estilo para st.date_input */
    div[data-testid="stDateInput"] .stDateInput input {
        border-radius: 8px;
        border: 1px solid #d0d0d0;
        padding: 10px 12px;
        background-color: #ffffff;
        box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.03);
        transition: all 0.2s ease-in-out;
    }
    div[data-testid="stDateInput"] .stDateInput input:focus {
        border-color: #28a745;
        box-shadow: 0 0 0 2px rgba(40, 167, 69, 0.15);
        outline: none;
    }

    /* Estilo para st.selectbox */
    div[data-testid="stSelectbox"] button {
        border-radius: 8px;
        border: 1px solid #d0d0d0;
        padding: 10px 12px;
        background-color: #ffffff;
        box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.03);
        transition: all 0.2s ease-in-out;
    }
    div[data-testid="stSelectbox"] button:focus {
        border-color: #28a745;
        box-shadow: 0 0 0 2px rgba(40, 167, 69, 0.15);
        outline: none;
    }

    /* Estilo específico para o campo de pesquisa (mais arredondado) */
    div[data-testid="stTextInput"] input[type="text"][placeholder*="Pesquisar"] {
        border-radius: 20px; /* Mais arredondado para pesquisa */
        padding-left: 20px; /* Espaçamento para ícone de pesquisa (se houver) */
    }

    /* Estilo para botões gerais (ex: "Adicionar Lançamento") */
    div[data-testid="stFormSubmitButton"] button {
        border-radius: 8px;
        border: none; /* Remove a borda padrão */
        background-color: #28a745; /* Fundo verde principal */
        color: white;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.2s ease-in-out; /* Transição suave */
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* Sombra mais sutil */
    }
    div[data-testid="stFormSubmitButton"] button:hover {
        background-color: #218838; /* Verde mais escuro no hover */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15); /* Sombra maior no hover */
    }
    div[data-testid="stFormSubmitButton"] button:focus {
        box-shadow: 0 0 0 0.2rem rgba(40, 167, 69, 0.4); /* Sombra de foco verde */
        outline: none;
    }

    /* Estilo para botões secundários (ex: "Essa semana", "Esse mês", "Hoje", "Limpar") */
    div[data-testid^="stButton"] button { /* Seleciona todos os botões e depois refina */
        background-color: #f8f9fa; /* Cinza muito claro */
        color: #495057; /* Texto cinza escuro */
        border: 1px solid #e0e0e0; /* Borda cinza */
        box-shadow: none; /* Remove sombra */
        padding: 8px 15px; /* Padding menor */
        font-weight: normal;
        border-radius: 8px; /* Cantos arredondados */
        transition: all 0.2s ease-in-out;
    }
    div[data-testid^="stButton"] button:hover {
        background-color: #e2e6ea; /* Cinza um pouco mais escuro no hover */
        border-color: #d0d0d0;
        color: #333;
    }

    /* Estilo para as abas (tabs) */
    div[data-testid="stTab"] {
        background-color: #f0f2f6;
        border-radius: 8px 8px 0 0;
        padding: 10px 15px;
        margin-right: 5px;
        font-weight: bold;
        color: #666;
        transition: all 0.2s ease-in-out;
    }
    div[data-testid="stTab"]:hover {
        background-color: #e0e2e6;
    }
    div[data-testid="stTab"][aria-selected="true"] {
        background-color: white;
        border-bottom: 3px solid #28a745; /* Linha verde na aba selecionada */
        color: #28a745;
    }
    div[data-testid="stTabs"] {
        background-color: transparent; /* Remove fundo da barra de abas */
    }
    div[data-testid="stTabContent"] {
        background-color: white; /* Fundo do conteúdo da aba */
        padding: 20px;
        border-radius: 0 0 10px 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    /* Estilo para o container dos botões de período */
    .period-buttons-container {
        display: flex;
        gap: 10px; /* Espaçamento entre os botões */
        align-items: center;
        flex-wrap: wrap; /* Permite quebrar linha em telas menores */
    }

    /* Ajuste para o st.dataframe */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden; /* Garante que o conteúdo não vaze das bordas arredondadas */
    }
    .stDataFrame table {
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 8px;
    }
    .stDataFrame thead th {
        background-color: #f8f9fa; /* Fundo do cabeçalho da tabela */
        color: #495057;
        font-weight: bold;
        padding: 12px 15px;
        border-bottom: 1px solid #e0e0e0;
    }
    .stDataFrame tbody tr {
        border-bottom: 1px solid #e0e0e0;
    }
    .stDataFrame tbody tr:last-child {
        border-bottom: none;
    }
    .stDataFrame tbody td {
        padding: 10px 15px;
    }
    .stDataFrame tbody tr:hover {
        background-color: #f2f2f2; /* Efeito hover nas linhas da tabela */
    }
    </style>
    """, unsafe_allow_html=True)

apply_custom_css()

# --- Funções de Ajuda ---
def calculate_metrics(df_filtered, start_date, end_date, prev_month_start, prev_month_end):
    # Métricas para o período atual
    total_receitas = df_filtered[df_filtered['Tipo'] == 'Receita']['Valor'].sum()
    total_despesas = df_filtered[df_filtered['Tipo'] == 'Despesa']['Valor'].sum()
    saldo_atual = total_receitas - total_despesas

    # Métricas para o mês anterior
    df_prev_month = st.session_state.df[
        (st.session_state.df['Data'] >= prev_month_start) & 
        (st.session_state.df['Data'] <= prev_month_end)
    ]
    prev_month_receitas = df_prev_month[df_prev_month['Tipo'] == 'Receita']['Valor'].sum()
    prev_month_despesas = df_prev_month[df_prev_month['Tipo'] == 'Despesa']['Valor'].sum()
    prev_month_saldo = prev_month_receitas - prev_month_despesas

    return total_receitas, total_despesas, saldo_atual, prev_month_saldo

# --- Título Principal e Subtítulo ---
st.title("💰 Dashboard de Análise Financeira")
st.markdown("Este aplicativo simula a perspectiva analítica do Granazen, permitindo que você carregue seus dados financeiros ou insira novos lançamentos manualmente.")
st.markdown("Para uma melhor experiência, seu arquivo CSV deve conter as seguintes colunas (nomes exatos): `Data`, `Descrição`, `Valor`, `Tipo` (com 'Receita' ou 'Despesa'), e `Categoria`.")


# --- Inicialização de Dados (se não houver arquivo carregado) ---
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['Data', 'Descrição', 'Valor', 'Tipo', 'Categoria'])
    # Adiciona alguns dados de exemplo se o DataFrame estiver vazio
    if st.session_state.df.empty:
        example_data = {
            'Data': [datetime(2024, 1, 10), datetime(2024, 1, 15), datetime(2024, 2, 5), datetime(2024, 2, 12), datetime(2024, 2, 20), datetime(2024, 3, 1), datetime(2024, 3, 10), datetime(2024, 3, 15)],
            'Descrição': ['Salário', 'Aluguel', 'Supermercado', 'Transporte', 'Restaurante', 'Bônus', 'Conta de Luz', 'Internet'],
            'Valor': [3000.00, 1500.00, 450.00, 120.00, 80.00, 500.00, 200.00, 90.00],
            'Tipo': ['Receita', 'Despesa', 'Despesa', 'Despesa', 'Despesa', 'Receita', 'Despesa', 'Despesa'],
            'Categoria': ['Salário', 'Moradia', 'Alimentação', 'Transporte', 'Lazer', 'Bônus', 'Moradia', 'Moradia']
        }
        st.session_state.df = pd.DataFrame(example_data)
        st.session_state.df['Data'] = pd.to_datetime(st.session_state.df['Data']) # Garante que a coluna Data seja datetime

# --- 1. Gerenciar Lançamentos ---
st.header("1. Gerenciar Lançamentos")

tab1, tab2 = st.tabs(["Carregar CSV", "Inserir Lançamento Manual"])

with tab1:
    st.subheader("Carregar Arquivo CSV")
    uploaded_file = st.file_uploader("Escolha um arquivo CSV com seus lançamentos financeiros", type="csv")

    if uploaded_file is not None:
        try:
            temp_df = pd.read_csv(uploaded_file)
            st.success("Arquivo CSV carregado com sucesso!")
            st.write("Prévia dos dados carregados:")
            st.dataframe(temp_df.head(), use_container_width=True)
            st.session_state.df = temp_df # Atualiza o DataFrame na sessão
            st.rerun() # Recarrega para aplicar os novos dados
        except Exception as e:
            st.error(f"Ocorreu um erro ao processar o arquivo: {e}")
            st.info("Por favor, certifique-se de que o arquivo é um CSV válido e bem formatado.")

with tab2:
    st.subheader("Inserir Novo Lançamento")
    with st.form("new_transaction_form"):
        col_date, col_type = st.columns(2)
        with col_date:
            new_data = st.date_input("Data", value=datetime.now())
        with col_type:
            new_tipo = st.selectbox("Tipo", ["Receita", "Despesa"])
        
        new_valor = st.number_input("Valor", min_value=0.01, format="%.2f")
        new_descricao = st.text_input("Descrição")
        new_categoria = st.text_input("Categoria")

        submitted = st.form_submit_button("Adicionar Lançamento")
        if submitted:
            if new_descricao and new_valor and new_categoria:
                new_entry = pd.DataFrame([{
                    'Data': new_data,
                    'Descrição': new_descricao,
                    'Valor': new_valor,
                    'Tipo': new_tipo,
                    'Categoria': new_categoria
                }])
                st.session_state.df = pd.concat([st.session_state.df, new_entry], ignore_index=True)
                st.success("Lançamento adicionado com sucesso!")
                st.rerun()
            else:
                st.warning("Por favor, preencha todos os campos (Descrição, Valor, Categoria).")

df = st.session_state.df.copy() # Usa uma cópia para evitar SettingWithCopyWarning

# --- Validação e Preparação de Dados Financeiros ---
if not df.empty:
    required_cols = ['Data', 'Descrição', 'Valor', 'Tipo', 'Categoria']
    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        st.error(f"Seu DataFrame está faltando as seguintes colunas essenciais: {', '.join(missing_cols)}. Por favor, verifique o formato.")
        df = pd.DataFrame(columns=required_cols) # Cria um DF vazio para evitar erros
    else:
        df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
        df.dropna(subset=['Data'], inplace=True)

        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
        df.dropna(subset=['Valor'], inplace=True)

        df = df[df['Tipo'].isin(['Receita', 'Despesa'])]
        df = df.sort_values(by='Data').reset_index(drop=True)

# --- Seleção de Período (Ajustado para o layout da imagem) ---
st.markdown("<div class='content-section'>", unsafe_allow_html=True)
col_month_nav, col_period_selection = st.columns([1, 3])

with col_month_nav:
    # Simulação de navegação por mês (setas)
    st.markdown("### ← Fevereiro →") # Hardcoded para simular, precisaria de lógica real

with col_period_selection:
    col_buttons, col_date_picker, col_clear_button = st.columns([2, 3, 1])
    with col_buttons:
        st.markdown("<div class='period-buttons-container'>", unsafe_allow_html=True)
        if st.button("Essa semana", key="btn_semana"):
            today = datetime.now().date()
            start_date = today - timedelta(days=today.weekday()) # Segunda-feira
            end_date = start_date + timedelta(days=6) # Domingo
            st.session_state.start_date = start_date
            st.session_state.end_date = end_date
            st.rerun()
        if st.button("Esse mês", key="btn_mes"):
            today = datetime.now().date()
            start_date = today.replace(day=1)
            end_date = (today.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1) # Último dia do mês
            st.session_state.start_date = start_date
            st.session_state.end_date = end_date
            st.rerun()
        if st.button("Hoje", key="btn_hoje"):
            today = datetime.now().date()
            st.session_state.start_date = today
            st.session_state.end_date = today
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_date_picker:
        # Define o período padrão como o mês atual se não houver seleção prévia
        if 'start_date' not in st.session_state or 'end_date' not in st.session_state:
            today = datetime.now().date()
            st.session_state.start_date = today.replace(day=1)
            st.session_state.end_date = (today.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)

        selected_date_range = st.date_input(
            "Período Personalizado",
            value=(st.session_state.start_date, st.session_state.end_date),
            key="date_range_picker",
            label_visibility="collapsed" # Esconde o label para um visual mais limpo
        )
        if len(selected_date_range) == 2:
            st.session_state.start_date = selected_date_range[0]
            st.session_state.end_date = selected_date_range[1]
        elif len(selected_date_range) == 1:
            st.session_state.start_date = selected_date_range[0]
            st.session_state.end_date = selected_date_range[0]

    with col_clear_button:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True) # Espaçamento para alinhar o botão
        if st.button("Limpar", key="btn_limpar"):
            if 'start_date' in st.session_state:
                del st.session_state.start_date
            if 'end_date' in st.session_state:
                del st.session_state.end_date
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True) # Fecha content-section para seleção de período


# Filtra o DataFrame com base no período selecionado
if not df.empty and 'start_date' in st.session_state and 'end_date' in st.session_state:
    df_filtered = df[
        (df['Data'].dt.date >= st.session_state.start_date) &
        (df['Data'].dt.date <= st.session_state.end_date)
    ]
else:
    df_filtered = pd.DataFrame(columns=required_cols) # DataFrame vazio se não houver dados ou seleção

# Calcula o período do mês anterior para a métrica
today = datetime.now().date()
first_day_current_month = today.replace(day=1)
last_day_prev_month = first_day_current_month - timedelta(days=1)
first_day_prev_month = last_day_prev_month.replace(day=1)

# --- Cards de Métricas (Ajustado para o layout da imagem) ---
st.markdown("<div class='content-section'>", unsafe_allow_html=True)
col_saldo, col_receitas, col_despesas, col_investimentos = st.columns(4) # Adicionado col_investimentos para layout

if not df.empty and not df_filtered.empty:
    total_receitas, total_despesas, saldo_atual, prev_month_saldo = calculate_metrics(
        df_filtered, st.session_state.start_date, st.session_state.end_date, first_day_prev_month, last_day_prev_month
    )

    with col_saldo:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Saldo</h3>
            <div style="font-size: 1.8em; font-weight: bold; color: {'#28a745' if saldo_atual >= 0 else '#dc3545'};">R$ {saldo_atual:,.2f}</div>
            <div style="font-size: 0.8em; color: #888;">{st.session_state.start_date.day} {calendar.month_abbr[st.session_state.start_date.month]}. até {st.session_state.end_date.day} {calendar.month_abbr[st.session_state.end_date.month]}.</div>
        </div>
        """, unsafe_allow_html=True)

    with col_receitas:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Receitas</h3>
            <div style="font-size: 1.8em; font-weight: bold; color: #28a745;">R$ {total_receitas:,.2f}</div>
            <div style="font-size: 0.8em; color: #888;">{st.session_state.start_date.day} {calendar.month_abbr[st.session_state.start_date.month]}. até {st.session_state.end_date.day} {calendar.month_abbr[st.session_state.end_date.month]}.</div>
        </div>
        """, unsafe_allow_html=True)

    with col_despesas:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Despesas</h3>
            <div style="font-size: 1.8em; font-weight: bold; color: #dc3545;">R$ {total_despesas:,.2f}</div>
            <div style="font-size: 0.8em; color: #888;">{st.session_state.start_date.day} {calendar.month_abbr[st.session_state.start_date.month]}. até {st.session_state.end_date.day} {calendar.month_abbr[st.session_state.end_date.month]}.</div>
        </div>
        """, unsafe_allow_html=True)

    with col_investimentos:
        # Este card é um placeholder, pois não temos dados de investimento.
        st.markdown(f"""
        <div class="metric-card">
            <h3>Investimentos</h3>
            <div style="font-size: 1.8em; font-weight: bold; color: #007bff;">R$ 0,00</div>
            <div style="font-size: 0.8em; color: #888;">(Dados não disponíveis)</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Carregue dados ou adicione lançamentos para ver as métricas.")

st.markdown("</div>", unsafe_allow_html=True) # Fecha content-section para métricas


# --- Layout principal: Entradas/Saídas Mensal e Resumo das Despesas ---
st.markdown("<div class='content-section'>", unsafe_allow_html=True)
col_monthly_chart, col_expense_summary = st.columns([2, 1])

with col_monthly_chart:
    st.subheader("Entradas e Saídas Mensal")
    if not df_filtered.empty:
        df_filtered['AnoMes'] = df_filtered['Data'].dt.to_period('M').astype(str)
        df_monthly_summary = df_filtered.groupby(['AnoMes', 'Tipo'])['Valor'].sum().unstack(fill_value=0).reset_index()
        df_monthly_summary.columns.name = None # Remove o nome do índice da coluna
        
        if 'Receita' not in df_monthly_summary.columns:
            df_monthly_summary['Receita'] = 0
        if 'Despesa' not in df_monthly_summary.columns:
            df_monthly_summary['Despesa'] = 0

        df_monthly_summary['AnoMes_Sort'] = pd.to_datetime(df_monthly_summary['AnoMes'])
        df_monthly_summary = df_monthly_summary.sort_values(by='AnoMes_Sort')

        fig_monthly_flow, ax_monthly_flow = plt.subplots(figsize=(10, 5)) # Ajuste de tamanho
        
        bar_width = 0.35
        r_index = np.arange(len(df_monthly_summary['AnoMes']))
        
        ax_monthly_flow.bar(r_index - bar_width/2, df_monthly_summary['Receita'], color='#28a745', width=bar_width, label='Receita')
        ax_monthly_flow.bar(r_index + bar_width/2, df_monthly_summary['Despesa'], color='#dc3545', width=bar_width, label='Despesa')

        ax_monthly_flow.set_xlabel('Mês/Ano', fontweight='bold')
        ax_monthly_flow.set_ylabel('Valor (R$)', fontweight='bold')
        ax_monthly_flow.set_title('Entradas e Saídas Mensais')
        ax_monthly_flow.set_xticks(r_index)
        ax_monthly_flow.set_xticklabels(df_monthly_summary['AnoMes'], rotation=45, ha='right')
        ax_monthly_flow.legend()
        ax_monthly_flow.grid(axis='y', linestyle='--', alpha=0.7)
        formatter = mticker.FormatStrFormatter('R$ %.2f')
        ax_monthly_flow.yaxis.set_major_formatter(formatter)
        plt.tight_layout()
        st.pyplot(fig_monthly_flow)
        plt.close(fig_monthly_flow)
    else:
        st.info("Nenhum dado disponível para gerar o gráfico de entradas e saídas mensais.")

with col_expense_summary:
    st.subheader("Resumo das Despesas")
    if not df_filtered.empty:
        df_despesas_summary = df_filtered[df_filtered['Tipo'] == 'Despesa'].copy()
        if not df_despesas_summary.empty:
            expense_summary = df_despesas_summary.groupby('Categoria')['Valor'].sum().reset_index()
            expense_summary.columns = ['Categoria', 'Gastos']
            expense_summary = expense_summary.sort_values(by='Gastos', ascending=False)

            total_expenses_period = expense_summary['Gastos'].sum()
            total_income_period = df_filtered[df_filtered['Tipo'] == 'Receita']['Valor'].sum()

            if total_expenses_period > 0:
                expense_summary['% s Despesas'] = (expense_summary['Gastos'] / total_expenses_period * 100).map('{:.2f}%'.format)
            else:
                expense_summary['% s Despesas'] = '0.00%'

            if total_income_period > 0:
                expense_summary['% s Receita'] = (expense_summary['Gastos'] / total_income_period * 100).map('{:.2f}%'.format)
            else:
                expense_summary['% s Receita'] = '0.00%'

            st.dataframe(expense_summary, use_container_width=True)
        else:
            st.info("Nenhuma despesa para resumir neste período.")
    else:
        st.info("Nenhum dado disponível para gerar o resumo das despesas.")

st.markdown("</div>", unsafe_allow_html=True) # Fecha content-section para Entradas/Saídas e Resumo

# --- Layout: Últimas Transações e Gastos por Tipo de Despesa ---
st.markdown("<div class='content-section'>", unsafe_allow_html=True)
col_transactions, col_expense_type_chart = st.columns([2, 1])

with col_transactions:
    st.subheader("Últimas Transações")
    st.markdown("Verifique as últimas transações")

    tab_all, tab_expenses, tab_income = st.tabs(["Todas", "Despesas", "Receitas"])

    search_query = st.text_input("Pesquisar receitas ou gastos", key="search_transactions")

    df_display = df_filtered.copy()

    if search_query:
        df_display = df_display[
            df_display['Descrição'].str.contains(search_query, case=False, na=False) |
            df_display['Categoria'].str.contains(search_query, case=False, na=False)
        ]

    with tab_all:
        st.dataframe(df_display[['Data', 'Descrição', 'Valor', 'Tipo', 'Categoria']].tail(10), use_container_width=True)
    with tab_expenses:
        st.dataframe(df_display[df_display['Tipo'] == 'Despesa'][['Data', 'Descrição', 'Valor', 'Categoria']].tail(10), use_container_width=True)
    with tab_income:
        st.dataframe(df_display[df_display['Tipo'] == 'Receita'][['Data', 'Descrição', 'Valor', 'Categoria']].tail(10), use_container_width=True)

with col_expense_type_chart:
    st.subheader("Gastos por Tipo de Despesa")
    st.info("Para esta análise, as despesas são categorizadas como 'Fixa' ou 'Variável' com base em algumas categorias de exemplo. Para uma classificação precisa, adicione um campo 'Tipo de Gasto' aos seus dados.")
    
    if not df_filtered.empty:
        df_despesas_type = df_filtered[df_filtered['Tipo'] == 'Despesa'].copy()
        
        # Simulação de classificação Fixa/Variável para demonstração
        # Em um app real, você teria uma coluna 'Tipo de Gasto' no seu CSV/input
        fixed_categories = ['Moradia', 'Internet', 'Seguros', 'Assinaturas']
        df_despesas_type['Tipo_Gasto'] = df_despesas_type['Categoria'].apply(
            lambda x: 'Fixa' if x in fixed_categories else 'Variável'
        )

        if not df_despesas_type.empty:
            gastos_por_tipo = df_despesas_type.groupby('Tipo_Gasto')['Valor'].sum()
            
            if 'Fixa' not in gastos_por_tipo.index:
                gastos_por_tipo['Fixa'] = 0
            if 'Variável' not in gastos_por_tipo.index:
                gastos_por_tipo['Variável'] = 0

            fig_expense_type, ax_expense_type = plt.subplots(figsize=(6, 6))
            ax_expense_type.pie(gastos_por_tipo, labels=gastos_por_tipo.index,
                                autopct='%1.1f%%', startangle=90, wedgeprops={'width': 0.4})
            ax_expense_type.set_title('Distribuição de Gastos (Fixos vs. Variáveis)')
            ax_expense_type.axis('equal')
            st.pyplot(fig_expense_type)
            plt.close(fig_expense_type)
        else:
            st.info("Nenhuma despesa encontrada para gerar o gráfico de tipo de despesa neste período.")
    else:
        st.info("Nenhum dado disponível para gerar o gráfico de tipo de despesa.")

st.markdown("</div>", unsafe_allow_html=True) # Fecha content-section para Transações e Tipo de Despesa


# --- Gráficos de Pizza de Categorias (Movidos para uma seção separada ou combinados) ---
# Os gráficos de pizza de despesas e receitas por categoria já estão na coluna da direita,
# dentro da seção "Categorias". Não é necessário duplicá-los aqui.
# O gráfico de Saldo Acumulado e Receitas/Despesas Mensais Detalhadas
# foram movidos para seções separadas abaixo para melhor organização.

# --- Gráfico de Saldo Acumulado ---
st.markdown("<div class='content-section'>", unsafe_allow_html=True)
st.subheader("Evolução do Saldo Acumulado ao Longo do Tempo")
if not df_filtered.empty:
    fig_saldo, ax_saldo = plt.subplots(figsize=(12, 6))
    ax_saldo.plot(df_filtered['Data'], df_filtered['Saldo_Acumulado'], marker='o', linestyle='-')
    ax_saldo.set_title('Saldo Acumulado ao Longo do Tempo')
    ax_saldo.set_xlabel('Data')
    ax_saldo.set_ylabel('Saldo (R$)')
    ax_saldo.grid(True)
    formatter = mticker.FormatStrFormatter('R$ %.2f')
    ax_saldo.yaxis.set_major_formatter(formatter)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig_saldo)
    plt.close(fig_saldo)
else:
    st.info("Nenhum dado disponível para o período selecionado para gerar o gráfico de saldo acumulado.")
st.markdown("</div>", unsafe_allow_html=True)


# --- Estratégias para Melhorar o Rendimento Mensal ---
st.markdown("<div class='content-section'>", unsafe_allow_html=True)
st.header("6. Estratégias para Melhorar o Rendimento Mensal")
if not df_filtered.empty:
    # Recalcula top_despesas para garantir que esteja disponível aqui
    df_despesas_filtered = df_filtered[df_filtered['Tipo'] == 'Despesa']
    top_despesas = pd.Series() # Inicializa como série vazia
    if not df_despesas_filtered.empty:
        top_despesas = df_despesas_filtered.groupby('Categoria')['Valor'].sum().nlargest(5)

    if saldo_atual < 0:
        st.markdown(f"**Seu saldo atual é negativo (R$ {saldo_atual:,.2f}) neste período.** É crucial analisar onde o dinheiro está indo.")
        st.markdown("### Foco Principal: Redução de Despesas")
        st.markdown("- **Revise suas Top Despesas:** As categorias que mais consomem seu dinheiro são:")
        if not top_despesas.empty:
            for categoria, valor in top_despesas.items():
                st.markdown(f"  - **{categoria}**: R$ {valor:,.2f}")
            st.markdown(f"Considere onde você pode cortar ou reduzir gastos nessas áreas. Pequenas mudanças diárias podem gerar grandes economias.")
        else:
            st.markdown("  - *Não foi possível identificar top categorias de despesas para este período.* Certifique-se de ter despesas registradas.")
        
        st.markdown("- **Corte gastos discricionários:** Lazer, alimentação fora de casa, compras impulsivas. Estabeleça um limite para esses gastos.")
        st.markdown("- **Negocie contas:** Verifique se é possível renegociar planos de telefone, internet, seguros, etc.")
    elif saldo_atual >= 0 and total_despesas > (total_receitas * 0.7): # Se o saldo é positivo mas as despesas são altas
        st.markdown(f"**Seu saldo atual é positivo (R$ {saldo_atual:,.2f}), o que é ótimo!** No entanto, suas despesas representam uma parcela significativa de suas receitas.")
        st.markdown("### Foco Principal: Otimização de Gastos e Poupança")
        st.markdown("- **Onde você pode otimizar?** As categorias com maior despesa são:")
        if not top_despesas.empty:
            for categoria, valor in top_despesas.items():
                st.markdown(f"  - **{categoria}**: R$ {valor:,.2f}")
            st.markdown(f"Mesmo com saldo positivo, otimizar gastos nessas áreas pode liberar mais dinheiro para poupança e investimentos.")
        else:
            st.markdown("  - *Não foi possível identificar top categorias de despesas para este período.*")
        st.markdown("- **Automatize a poupança:** Transfira um valor fixo para uma conta de poupança assim que receber sua receita.")
        st.markdown("- **Crie um orçamento detalhado:** Saber exatamente para onde seu dinheiro está indo é o primeiro passo para o controle.")
    else:
        st.markdown(f"**Parabéns! Seu saldo atual é saudável (R$ {saldo_atual:,.2f}).** Você está no caminho certo para uma boa saúde financeira.")
        st.markdown("### Foco Principal: Crescimento e Investimento")
        st.markdown("- **Explore novas fontes de receita:** Considere um trabalho extra, venda de itens não utilizados, ou monetize um hobby.")
        st.markdown("- **Invista seu dinheiro:** Com um saldo positivo, é o momento de fazer seu dinheiro trabalhar para você. Pesquise opções de investimento (renda fixa, fundos, ações) que se alinham aos seus objetivos.")
        st.markdown("- **Educação financeira:** Continue aprendendo sobre finanças pessoais e investimentos para tomar decisões mais informadas.")

    st.markdown("---")
    st.markdown("Lembre-se: A chave para um bom rendimento mensal é o **controle contínuo** e a **adaptação** às suas necessidades financeiras.")
else:
    st.info("Carregue dados ou adicione lançamentos para receber estratégias personalizadas.")

st.markdown("</div>", unsafe_allow_html=True)


st.markdown("---")
st.markdown("Desenvolvido com Streamlit e Matplotlib para uma experiência de análise financeira intuitiva.")
