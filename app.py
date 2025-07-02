import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.ticker as mticker
import calendar # Para obter o nome do mês

# --- Configuração da Página ---
st.set_page_config(layout="wide", page_title="Painel Financeiro Granazen-like")

# --- Funções Auxiliares de Estilo (para simular o visual do Granazen) ---
def apply_custom_css():
    st.markdown("""
    <style>
    /* Estilo geral */
    .stApp {
        background-color: #f0f2f6; /* Cor de fundo clara */
        color: #333; /* Cor do texto padrão */
        font-family: "Inter", sans-serif; /* Fonte Inter */
    }

    /* Header/Navegação (REMOVIDO) */
    /* .header-container {
        background-color: #28a745; /* Verde do Granazen */
        padding: 10px 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .header-item {
        color: white;
        font-weight: bold;
        padding: 5px 10px;
        cursor: pointer;
        border-radius: 5px; /* Arredondar itens do cabeçalho */
    }
    .header-item:hover {
        background-color: #218838;
    }
    .header-logo {
        font-size: 24px;
        font-weight: bold;
        color: white;
    }
    .header-right {
        display: flex;
        gap: 15px;
    } */

    /* Cards de Métricas */
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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

    /* Seções de Conteúdo (Tabela, Gráficos, Formulários) */
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
        border-radius: 8px;
        border: 1px solid #e0e0e0; /* Borda suave */
        padding: 10px 12px;
        background-color: #fcfcfc; /* Fundo levemente diferente */
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05); /* Sombra interna sutil */
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stDateInput > div > div > input:focus,
    .stSelectbox > div > div > div > div:focus {
        border-color: #28a745; /* Borda verde no foco */
        box-shadow: 0 0 0 0.2rem rgba(40, 167, 69, 0.25); /* Sombra de foco verde */
        outline: none; /* Remove outline padrão do navegador */
    }

    /* Estilo para o campo de pesquisa */
    .stTextInput[data-testid="stTextInput"] > div > div > input {
        border-radius: 20px; /* Mais arredondado para pesquisa */
        padding-left: 20px; /* Espaçamento para ícone de pesquisa (se houver) */
    }

    /* Estilo para botões gerais */
    .stButton > button {
        border-radius: 8px;
        border: 1px solid #28a745; /* Borda verde */
        background-color: #28a745; /* Fundo verde */
        color: white;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.2s ease-in-out; /* Transição suave */
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .stButton > button:hover {
        background-color: #218838; /* Verde mais escuro no hover */
        border-color: #218838;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    .stButton > button:focus {
        box-shadow: 0 0 0 0.2rem rgba(40, 167, 69, 0.5);
        outline: none;
    }

    /* Estilo para botões de data (Essa semana, Esse mês, Hoje, Limpar) */
    .stButton > button[data-testid*="stButton-secondary"] { /* Ajuste para botões secundários */
        background-color: #f9f9f9;
        color: #333;
        border: 1px solid #ddd;
        box-shadow: none;
    }
    .stButton > button[data-testid*="stButton-secondary"]:hover {
        background-color: #e9e9e9;
        border-color: #ccc;
        color: #333;
    }
    /* Estilo para o botão "Esse mês" selecionado, se o Streamlit mantiver um estado */
    /* Isso é mais complexo com CSS puro, mas podemos simular um destaque */
    /* Streamlit não adiciona uma classe 'selected' automaticamente para botões */
    /* Apenas para demonstração, o estilo abaixo não será ativado por clique */
    /* .stButton > button[data-testid="stButton-secondary"][aria-pressed="true"] {
        background-color: #28a745;
        color: white;
        border-color: #28a745;
    } */

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

# --- Header/Navegação (REMOVIDO) ---
# st.markdown("""
# <div class="header-container">
#     <div class="header-left">
#         <span class="header-logo">GranaZen</span>
#     </div>
#     <div class="header-right">
#         <span class="header-item">Visão geral</span>
#         <span class="header-item">Planeje sua grana</span>
#         <span class="header-item">Minhas Categorias</span>
#         <span class="header-item">Configurações</span>
#         <span class="header-item">Aparência</span>
#         <span class="header-item">Sair</span>
#     </div>
# </div>
# """, unsafe_allow_html=True)

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

# --- 1. Carregar Dados ou Inserir Manualmente ---
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

    st.markdown("</div>", unsafe_allow_html=True) # Fecha content-section para categorias/gráfico

# --- Gráfico de Saldo Acumulado (Mantido, mas fora do layout principal para melhor visualização) ---
st.markdown("<div class='content-section'>", unsafe_allow_html=True)
st.subheader("Evolução do Saldo ao Longo do Tempo")
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
    st.info("Nenhum dado disponível para o período selecionado para gerar o gráfico de saldo.")
st.markdown("</div>", unsafe_allow_html=True)


# --- Gráfico de Barras Mensal/Anual de Receitas e Despesas (Mantido, mas fora do layout principal) ---
st.markdown("<div class='content-section'>", unsafe_allow_html=True)
st.subheader("Receitas e Despesas por Período")
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
    ax_bar.set_title('Receitas e Despesas Mensais')
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


# --- Filtragem e Exportação de Dados (Mantido) ---
st.markdown("<div class='content-section'>", unsafe_allow_html=True)
st.header("5. Filtragem e Exportação de Dados")
st.write("Filtre seus dados com base nos valores das colunas e exporte o resultado.")

filter_column = st.selectbox("Selecione a coluna para filtrar:", [''] + list(df.columns))

if filter_column:
    unique_values = df[filter_column].unique()

    if pd.api.types.is_numeric_dtype(df[filter_column]):
        min_val, max_val = float(df[filter_column].min()), float(df[filter_column].max())
        selected_range = st.slider(f"Selecione o intervalo para '{filter_column}':",
                                   min_value=min_val,
                                   max_value=max_val,
                                   value=(min_val, max_val))
        filtered_df = df[(df[filter_column] >= selected_range[0]) & (df[filter_column] <= selected_range[1])]
    elif pd.api.types.is_datetime64_any_dtype(df[filter_column]):
        min_date, max_date = df[filter_column].min(), df[filter_column].max()
        selected_dates = st.date_input(f"Selecione o intervalo de datas para '{filter_column}':",
                                       value=(min_date, max_date),
                                       min_value=min_date,
                                       max_value=max_date)
        if len(selected_dates) == 2:
            filtered_df = df[(df[filter_column] >= pd.to_datetime(selected_dates[0])) &
                             (df[filter_column] <= pd.to_datetime(selected_dates[1]))]
        else:
            filtered_df = df
    else: # Categórica ou Texto
        selected_values = st.multiselect(f"Selecione os valores para '{filter_column}':",
                                         options=unique_values,
                                         default=unique_values)
        filtered_df = df[df[filter_column].isin(selected_values)]

    if 'filtered_df' in locals():
        st.write("Dados Filtrados:")
        st.dataframe(filtered_df)
        st.write(f"Linhas após a filtragem: {filtered_df.shape[0]}")
        st.download_button(
            label="Baixar Dados Filtrados (CSV)",
            data=filtered_df.to_csv(index=False).encode('utf-8'),
            file_name="dados_filtrados.csv",
            mime="text/csv",
        )
else:
    st.info("Selecione uma coluna para aplicar filtros.")

st.markdown("</div>", unsafe_allow_html=True)


st.markdown("---")
st.markdown("Desenvolvido com Streamlit e Matplotlib para uma experiência de análise financeira intuitiva.")
