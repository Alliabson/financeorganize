import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.ticker as mticker
import calendar # Para obter o nome do mês
import numpy as np # Adicionado para operações numéricas, se necessário

# --- Configuração da Página ---
st.set_page_config(layout="wide", page_title="Painel Financeiro Granazen-like")

# --- Funções Auxiliares de Estilo (para simular o visual do Granazen) ---
def apply_custom_css():
    st.markdown("""
    <style>
    /* Estilo geral do aplicativo */
    .stApp {
        background-color: #f0f2f6; /* Cor de fundo clara */
        color: #333; /* Cor do texto padrão */
        font-family: "Inter", sans-serif; /* Fonte Inter para um visual moderno */
    }

    /* Estilo para os cards de métricas (Receitas, Despesas, Saldo) */
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px; /* Cantos arredondados */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Sombra suave para profundidade */
        text-align: left;
        height: 100%; /* Garante que os cards tenham a mesma altura */
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .metric-card h3 {
        margin-top: 0;
        color: #333;
        font-size: 1.1em;
    }
    .metric-card .stMetric {
        padding: 0;
    }
    .metric-card .stMetric > div:first-child { /* Título da métrica */
        color: #666;
        font-size: 0.9em;
    }
    .metric-card .stMetric > div:nth-child(2) { /* Valor da métrica */
        font-size: 1.8em;
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
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }

    /* Estilo para campos de input (texto, número, data) e selectbox */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input,
    .stSelectbox > div > div > div > div {
        border-radius: 8px; /* Cantos arredondados */
        border: 1px solid #d0d0d0; /* Borda cinza suave */
        padding: 10px 12px;
        background-color: #ffffff; /* Fundo branco puro */
        box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.05); /* Sombra interna sutil */
        transition: all 0.2s ease-in-out; /* Transição suave para o foco */
    }

    /* Estilo de foco para campos de input e selectbox */
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stDateInput > div > div > input:focus,
    .stSelectbox > div > div > div > div:focus {
        border-color: #28a745; /* Borda verde no foco */
        box-shadow: 0 0 0 2px rgba(40, 167, 69, 0.2); /* Sombra de foco verde suave */
        outline: none; /* Remove outline padrão do navegador */
    }

    /* Estilo específico para o campo de pesquisa (mais arredondado) */
    .stTextInput[data-testid="stTextInput"] > div > div > input {
        border-radius: 20px; /* Mais arredondado para pesquisa */
        padding-left: 20px; /* Espaçamento para ícone de pesquisa (se houver) */
    }

    /* Estilo para botões gerais (ex: "Adicionar Lançamento") */
    .stButton > button {
        border-radius: 8px;
        border: none; /* Remove a borda padrão */
        background-color: #28a745; /* Fundo verde principal */
        color: white;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.2s ease-in-out; /* Transição suave */
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15); /* Sombra mais pronunciada */
    }
    .stButton > button:hover {
        background-color: #218838; /* Verde mais escuro no hover */
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* Sombra maior no hover */
    }
    .stButton > button:focus {
        box-shadow: 0 0 0 0.2rem rgba(40, 167, 69, 0.5); /* Sombra de foco verde */
        outline: none;
    }

    /* Estilo para botões secundários (ex: "Essa semana", "Esse mês", "Hoje", "Limpar") */
    .stButton > button[data-testid*="stButton-secondary"] {
        background-color: #e9ecef; /* Cinza claro */
        color: #495057; /* Texto cinza escuro */
        border: 1px solid #ced4da; /* Borda cinza */
        box-shadow: none; /* Remove sombra */
    }
    .stButton > button[data-testid*="stButton-secondary"]:hover {
        background-color: #dee2e6; /* Cinza um pouco mais escuro no hover */
        border-color: #adb5bd;
        color: #333;
    }

    /* Estilo para as abas (tabs) */
    .stTabs [data-testid="stTab"] {
        background-color: #f0f2f6;
        border-radius: 8px 8px 0 0;
        padding: 10px 15px;
        margin-right: 5px;
        font-weight: bold;
        color: #666;
        transition: all 0.2s ease-in-out;
    }
    .stTabs [data-testid="stTab"]:hover {
        background-color: #e0e2e6;
    }
    .stTabs [data-testid="stTab"][aria-selected="true"] {
        background-color: white;
        border-bottom: 3px solid #28a745; /* Linha verde na aba selecionada */
        color: #28a745;
    }
    .stTabs [data-testid="stTabs"] {
        background-color: transparent; /* Remove fundo da barra de abas */
    }
    .stTabs [data-testid="stTabContent"] {
        background-color: white; /* Fundo do conteúdo da aba */
        padding: 20px;
        border-radius: 0 0 10px 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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
            'Data': [datetime(2024, 1, 10), datetime(2024, 1, 15), datetime(2024, 2, 5), datetime(2024, 2, 12), datetime(2024, 2, 20), datetime(2024, 3, 1), datetime(2024, 3, 10)],
            'Descrição': ['Salário', 'Aluguel', 'Supermercado', 'Transporte', 'Restaurante', 'Bônus', 'Conta de Luz'],
            'Valor': [3000.00, 1500.00, 450.00, 120.00, 80.00, 500.00, 200.00],
            'Tipo': ['Receita', 'Despesa', 'Despesa', 'Despesa', 'Despesa', 'Receita', 'Despesa'],
            'Categoria': ['Salário', 'Moradia', 'Alimentação', 'Transporte', 'Lazer', 'Bônus', 'Moradia']
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
            st.dataframe(temp_df.head())
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

# --- Seleção de Período ---
st.markdown("<div class='content-section'>", unsafe_allow_html=True)
st.subheader("Seleção de Período")

col_nav_month, col_period_buttons, col_date_range, col_clear = st.columns([1, 2, 3, 1])

with col_nav_month:
    current_month_name = calendar.month_name[datetime.now().month]
    st.markdown(f"### ← {current_month_name} →") # Simulação de navegação por mês

with col_period_buttons:
    if st.button("Essa semana"):
        today = datetime.now().date()
        start_date = today - timedelta(days=today.weekday()) # Segunda-feira
        end_date = start_date + timedelta(days=6) # Domingo
        st.session_state.start_date = start_date
        st.session_state.end_date = end_date
        st.rerun()
    if st.button("Esse mês"):
        today = datetime.now().date()
        start_date = today.replace(day=1)
        end_date = (today.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1) # Último dia do mês
        st.session_state.start_date = start_date
        st.session_state.end_date = end_date
        st.rerun()
    if st.button("Hoje"):
        today = datetime.now().date()
        st.session_state.start_date = today
        st.session_state.end_date = today
        st.rerun()

with col_date_range:
    # Define o período padrão como o mês atual se não houver seleção prévia
    if 'start_date' not in st.session_state or 'end_date' not in st.session_state:
        today = datetime.now().date()
        st.session_state.start_date = today.replace(day=1)
        st.session_state.end_date = (today.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)

    selected_date_range = st.date_input(
        "Período Personalizado",
        value=(st.session_state.start_date, st.session_state.end_date),
        key="date_range_picker"
    )
    if len(selected_date_range) == 2:
        st.session_state.start_date = selected_date_range[0]
        st.session_state.end_date = selected_date_range[1]
    elif len(selected_date_range) == 1: # Caso o usuário selecione apenas uma data
        st.session_state.start_date = selected_date_range[0]
        st.session_state.end_date = selected_date_range[0]


with col_clear:
    if st.button("Limpar"):
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

# --- Cards de Métricas ---
st.markdown("<div class='content-section'>", unsafe_allow_html=True)
st.subheader("Resumo Financeiro")
col1, col2, col3, col4 = st.columns(4)

if not df.empty and not df_filtered.empty:
    total_receitas, total_despesas, saldo_atual, prev_month_saldo = calculate_metrics(
        df_filtered, st.session_state.start_date, st.session_state.end_date, first_day_prev_month, last_day_prev_month
    )

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Mês Anterior ({calendar.month_name[first_day_prev_month.month].capitalize()})</h3>
            <div style="font-size: 1.8em; font-weight: bold; color: #333;">R$ {prev_month_saldo:,.2f}</div>
            <div style="font-size: 0.8em; color: #888;">1 {calendar.month_abbr[first_day_prev_month.month]}. até {last_day_prev_month.day} {calendar.month_abbr[last_day_prev_month.month]}.</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Receitas</h3>
            <div style="font-size: 1.8em; font-weight: bold; color: #28a745;">R$ {total_receitas:,.2f}</div>
            <div style="font-size: 0.8em; color: #888;">{st.session_state.start_date.day} {calendar.month_abbr[st.session_state.start_date.month]}. até {st.session_state.end_date.day} {calendar.month_abbr[st.session_state.end_date.month]}.</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Despesas</h3>
            <div style="font-size: 1.8em; font-weight: bold; color: #dc3545;">R$ {total_despesas:,.2f}</div>
            <div style="font-size: 0.8em; color: #888;">{st.session_state.start_date.day} {calendar.month_abbr[st.session_state.start_date.month]}. até {st.session_state.end_date.day} {calendar.month_abbr[st.session_state.end_date.month]}.</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Saldo Atual</h3>
            <div style="font-size: 1.8em; font-weight: bold; color: {'#28a745' if saldo_atual >= 0 else '#dc3545'};">R$ {saldo_atual:,.2f}</div>
            <div style="font-size: 0.8em; color: #888;">{st.session_state.start_date.day} {calendar.month_abbr[st.session_state.start_date.month]}. até {st.session_state.end_date.day} {calendar.month_abbr[st.session_state.end_date.month]}.</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Carregue dados ou adicione lançamentos para ver as métricas.")

st.markdown("</div>", unsafe_allow_html=True) # Fecha content-section para métricas


# --- Layout principal: Últimas Transações e Categorias/Gráfico ---
main_col1, main_col2 = st.columns([2, 1])

with main_col1:
    st.markdown("<div class='content-section'>", unsafe_allow_html=True)
    st.subheader("Últimas Transações")
    st.markdown("Verifique as últimas transações")

    # Tabs para filtrar transações
    tab_all, tab_expenses, tab_income = st.tabs(["Todas", "Despesas", "Receitas"])

    search_query = st.text_input("Pesquisar receitas ou gastos", "")

    df_display = df_filtered.copy() # Usar uma cópia para a exibição

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

    st.markdown("</div>", unsafe_allow_html=True) # Fecha content-section para transações

with main_col2:
    st.markdown("<div class='content-section'>", unsafe_allow_html=True)
    st.subheader("Categorias")

    tab_cat_despesas, tab_cat_receitas = st.tabs(["Despesas", "Receitas"])

    with tab_cat_despesas:
        st.markdown(f"Gráfico por categoria ({st.session_state.start_date.day} {calendar.month_abbr[st.session_state.start_date.month]}. - {st.session_state.end_date.day} {calendar.month_abbr[st.session_state.end_date.month]}. )")
        df_despesas_filtered = df_filtered[df_filtered['Tipo'] == 'Despesa']
        if not df_despesas_filtered.empty:
            despesas_por_categoria = df_despesas_filtered.groupby('Categoria')['Valor'].sum()
            fig_despesas_cat, ax_despesas_cat = plt.subplots(figsize=(6, 6)) # Tamanho ajustado para coluna
            ax_despesas_cat.pie(despesas_por_categoria, labels=despesas_por_categoria.index,
                                autopct='%1.1f%%', startangle=90, wedgeprops={'width': 0.4})
            ax_despesas_cat.set_title('Distribuição das Despesas por Categoria')
            ax_despesas_cat.axis('equal')
            st.pyplot(fig_despesas_cat)
            plt.close(fig_despesas_cat)
        else:
            st.info("Nenhuma despesa encontrada para gerar o gráfico de pizza neste período.")

    with tab_cat_receitas:
        st.markdown(f"Gráfico por categoria ({st.session_state.start_date.day} {calendar.month_abbr[st.session_state.start_date.month]}. - {st.session_state.end_date.day} {calendar.month_abbr[st.session_state.end_date.month]}. )")
        df_receitas_filtered = df_filtered[df_filtered['Tipo'] == 'Receita']
        if not df_receitas_filtered.empty:
            receitas_por_categoria = df_receitas_filtered.groupby('Categoria')['Valor'].sum()
            fig_receitas_cat, ax_receitas_cat = plt.subplots(figsize=(6, 6)) # Tamanho ajustado para coluna
            ax_receitas_cat.pie(receitas_por_categoria, labels=receitas_por_categoria.index,
                                autopct='%1.1f%%', startangle=90, wedgeprops={'width': 0.4})
            ax_receitas_cat.set_title('Distribuição das Receitas por Categoria')
            ax_receitas_cat.axis('equal')
            st.pyplot(fig_receitas_cat)
            plt.close(fig_receitas_cat)
        else:
            st.info("Nenhuma receita encontrada para gerar o gráfico de pizza neste período.")

    # --- Top Categorias de Despesas ---
    st.subheader("Top 5 Categorias de Despesas")
    if not df_despesas_filtered.empty:
        top_despesas = df_despesas_filtered.groupby('Categoria')['Valor'].sum().nlargest(5)
        if not top_despesas.empty:
            for categoria, valor in top_despesas.items():
                st.markdown(f"- **{categoria}**: R$ {valor:,.2f}")
        else:
            st.info("Não há despesas suficientes para listar as top categorias.")
    else:
        st.info("Nenhuma despesa para analisar as top categorias.")

    st.markdown("</div>", unsafe_allow_html=True) # Fecha content-section para categorias/gráfico

# --- Gráfico de Saldo Acumulado (Mantido, mas fora do layout principal para melhor visualização) ---
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


# --- Novo Gráfico: Saldo Mensal (Receitas - Despesas) ---
st.markdown("<div class='content-section'>", unsafe_allow_html=True)
st.subheader("Saldo Mensal (Receitas - Despesas)")
if not df_filtered.empty:
    # Garante que 'AnoMes' e 'Valor_Ajustado' estejam disponíveis
    df_filtered['AnoMes'] = df_filtered['Data'].dt.to_period('M').astype(str)
    monthly_net_balance = df_filtered.groupby('AnoMes')['Valor_Ajustado'].sum().reset_index()
    monthly_net_balance.columns = ['AnoMes', 'Saldo_Mensal']
    
    # Ordena por data para garantir a correta visualização da série temporal
    monthly_net_balance['AnoMes_Sort'] = pd.to_datetime(monthly_net_balance['AnoMes'])
    monthly_net_balance = monthly_net_balance.sort_values(by='AnoMes_Sort')

    fig_net_balance, ax_net_balance = plt.subplots(figsize=(12, 6))
    ax_net_balance.bar(monthly_net_balance['AnoMes'], monthly_net_balance['Saldo_Mensal'],
                       color=['g' if x >= 0 else 'r' for x in monthly_net_balance['Saldo_Mensal']],
                       edgecolor='grey')
    ax_net_balance.set_title('Saldo Mensal (Receitas - Despesas)')
    ax_net_balance.set_xlabel('Mês/Ano')
    ax_net_balance.set_ylabel('Saldo (R$)')
    ax_net_balance.grid(axis='y', linestyle='--', alpha=0.7)
    formatter = mticker.FormatStrFormatter('R$ %.2f')
    ax_net_balance.yaxis.set_major_formatter(formatter)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig_net_balance)
    plt.close(fig_net_balance)
else:
    st.info("Nenhum dado disponível para o período selecionado para gerar o gráfico de saldo mensal.")
st.markdown("</div>", unsafe_allow_html=True)


# --- Gráfico de Barras Mensal/Anual de Receitas e Despesas (Mantido) ---
st.markdown("<div class='content-section'>", unsafe_allow_html=True)
st.subheader("Receitas e Despesas Mensais Detalhadas")
if not df_filtered.empty:
    df_filtered['AnoMes'] = df_filtered['Data'].dt.to_period('M').astype(str)
    df_grouped = df_filtered.groupby(['AnoMes', 'Tipo'])['Valor'].sum().unstack(fill_value=0).reset_index()
    df_grouped.columns.name = None
    
    if 'Receita' not in df_grouped.columns:
        df_grouped['Receita'] = 0
    if 'Despesa' not in df_grouped.columns:
        df_grouped['Despesa'] = 0

    df_grouped['AnoMes_Sort'] = pd.to_datetime(df_grouped['AnoMes'])
    df_grouped = df_grouped.sort_values(by='AnoMes_Sort')

    fig_bar, ax_bar = plt.subplots(figsize=(12, 6))
    
    bar_width = 0.35
    r1 = range(len(df_grouped['AnoMes']))
    r2 = [x + bar_width for x in r1]

    ax_bar.bar(r1, df_grouped['Receita'], color='g', width=bar_width, edgecolor='grey', label='Receita')
    ax_bar.bar(r2, df_grouped['Despesa'], color='r', width=bar_width, edgecolor='grey', label='Despesa')

    ax_bar.set_xlabel('Mês/Ano', fontweight='bold')
    ax_bar.set_ylabel('Valor (R$)', fontweight='bold')
    ax_bar.set_title('Receitas e Despesas Mensais Detalhadas')
    ax_bar.set_xticks([r + bar_width/2 for r in range(len(df_grouped['AnoMes']))])
    ax_bar.set_xticklabels(df_grouped['AnoMes'], rotation=45, ha='right')
    ax_bar.legend()
    ax_bar.grid(axis='y', linestyle='--', alpha=0.7)
    formatter = mticker.FormatStrFormatter('R$ %.2f')
    ax_bar.yaxis.set_major_formatter(formatter)
    plt.tight_layout()
    st.pyplot(fig_bar)
    plt.close(fig_bar)
else:
    st.info("Nenhum dado disponível para o período selecionado para gerar o gráfico de barras.")
st.markdown("</div>", unsafe_allow_html=True)


# --- Estratégias para Melhorar o Rendimento Mensal ---
st.markdown("<div class='content-section'>", unsafe_allow_html=True)
st.header("6. Estratégias para Melhorar o Rendimento Mensal")
if not df_filtered.empty:
    if saldo_atual < 0:
        st.markdown(f"**Seu saldo atual é negativo (R$ {saldo_atual:,.2f}) neste período.** É crucial analisar onde o dinheiro está indo.")
        st.markdown("### Foco Principal: Redução de Despesas")
        st.markdown("- **Revise suas Top Despesas:** As categorias que mais consomem seu dinheiro são:")
        if 'top_despesas' in locals() and not top_despesas.empty:
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
        if 'top_despesas' in locals() and not top_despesas.empty:
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
        st.markdown("- **Invista seu dinheiro:** Com um saldo positivo, é o momento de fazer seu dinheiro trabalhar para você. Pesquise opções de investimento (renda fixa, fundos, ações) que se alinhem aos seus objetivos.")
        st.markdown("- **Educação financeira:** Continue aprendendo sobre finanças pessoais e investimentos para tomar decisões mais informadas.")

    st.markdown("---")
    st.markdown("Lembre-se: A chave para um bom rendimento mensal é o **controle contínuo** e a **adaptação** às suas necessidades financeiras.")
else:
    st.info("Carregue dados ou adicione lançamentos para receber estratégias personalizadas.")

st.markdown("</div>", unsafe_allow_html=True)


st.markdown("---")
st.markdown("Desenvolvido com Streamlit e Matplotlib para uma experiência de análise financeira intuitiva.")
