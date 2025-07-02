import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.ticker as mticker
import calendar
import numpy as np

# --- Configuração da Página ---
st.set_page_config(layout="wide", page_title="Painel Financeiro Granazen-like")

# --- Funções Auxiliares de Estilo ---
def apply_custom_css():
    st.markdown("""
    <style>
    /* Estilo geral do aplicativo */
    .stApp {
        background-color: #f0f2f6;
        color: #333;
        font-family: "Inter", sans-serif;
    }

    /* Títulos principais */
    h1, h2, h3, h4, h5, h6 {
        color: #333;
    }

    /* Estilo para os cards de métricas */
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.08);
        text-align: left;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        border: 1px solid #e0e0e0;
    }
    .metric-card h3 {
        margin-top: 0;
        color: #666;
        font-size: 1em;
        font-weight: normal;
    }
    .metric-card .stMetric {
        padding: 0;
    }
    .metric-card .stMetric > div:first-child {
        color: #666;
        font-size: 0.9em;
    }
    .metric-card .stMetric > div:nth-child(2) {
        font-size: 1.6em;
        font-weight: bold;
        color: #333;
    }
    .metric-card .stMetric > div:nth-child(3) {
        font-size: 0.8em;
        color: #888;
    }

    /* Estilo para as seções de conteúdo */
    .content-section {
        background-color: white;
        padding: 25px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        margin-bottom: 20px;
        border: 1px solid #e0e0e0;
    }

    /* Outros estilos... */
    </style>
    """, unsafe_allow_html=True)

apply_custom_css()

# --- Funções de Ajuda ---
def calculate_metrics(df_filtered, start_date, end_date, prev_month_start, prev_month_end):
    # Métricas para o período atual
    total_receitas = df_filtered[df_filtered['Tipo'] == 'Receita']['Valor'].sum() if not df_filtered.empty else 0
    total_despesas = df_filtered[df_filtered['Tipo'] == 'Despesa']['Valor'].sum() if not df_filtered.empty else 0
    saldo_atual = total_receitas - total_despesas

    # Métricas para o mês anterior
    prev_month_receitas = 0
    prev_month_despesas = 0
    
    if not st.session_state.df.empty and 'Data' in st.session_state.df.columns:
        df_prev = st.session_state.df.copy()
        df_prev['Data'] = pd.to_datetime(df_prev['Data'], errors='coerce')
        df_prev = df_prev.dropna(subset=['Data'])
        
        if not df_prev.empty:
            df_prev_month = df_prev[
                (df_prev['Data'].dt.date >= prev_month_start) & 
                (df_prev['Data'].dt.date <= prev_month_end)
            ]
            prev_month_receitas = df_prev_month[df_prev_month['Tipo'] == 'Receita']['Valor'].sum() if not df_prev_month.empty else 0
            prev_month_despesas = df_prev_month[df_prev_month['Tipo'] == 'Despesa']['Valor'].sum() if not df_prev_month.empty else 0

    prev_month_saldo = prev_month_receitas - prev_month_despesas

    return total_receitas, total_despesas, saldo_atual, prev_month_saldo

# --- Título Principal ---
st.title("💰 Dashboard de Análise Financeira")
st.markdown("Este aplicativo simula a perspectiva analítica do Granazen, permitindo que você carregue seus dados financeiros ou insira novos lançamentos manualmente.")

# --- Inicialização de Dados ---
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['Data', 'Descrição', 'Valor', 'Tipo', 'Categoria'])
    if st.session_state.df.empty:
        example_data = {
            'Data': [datetime(2024, 1, 10), datetime(2024, 1, 15), datetime(2024, 2, 5), 
                    datetime(2024, 2, 12), datetime(2024, 2, 20), datetime(2024, 3, 1), 
                    datetime(2024, 3, 10), datetime(2024, 3, 15)],
            'Descrição': ['Salário', 'Aluguel', 'Supermercado', 'Transporte', 'Restaurante', 
                         'Bônus', 'Conta de Luz', 'Internet'],
            'Valor': [3000.00, 1500.00, 450.00, 120.00, 80.00, 500.00, 200.00, 90.00],
            'Tipo': ['Receita', 'Despesa', 'Despesa', 'Despesa', 'Despesa', 'Receita', 'Despesa', 'Despesa'],
            'Categoria': ['Salário', 'Moradia', 'Alimentação', 'Transporte', 'Lazer', 'Bônus', 'Moradia', 'Moradia']
        }
        st.session_state.df = pd.DataFrame(example_data)
        st.session_state.df['Data'] = pd.to_datetime(st.session_state.df['Data'])

# --- 1. Gerenciar Lançamentos ---
st.header("1. Gerenciar Lançamentos")
tab1, tab2 = st.tabs(["Carregar CSV", "Inserir Lançamento Manual"])

with tab1:
    st.subheader("Carregar Arquivo CSV")
    uploaded_file = st.file_uploader("Escolha um arquivo CSV com seus lançamentos financeiros", type="csv")

    if uploaded_file is not None:
        try:
            temp_df = pd.read_csv(uploaded_file)
            st.session_state.df = temp_df
            st.session_state.df['Data'] = pd.to_datetime(st.session_state.df['Data'], errors='coerce')
            st.session_state.df = st.session_state.df.dropna(subset=['Data'])
            st.success("Arquivo CSV carregado com sucesso!")
        except Exception as e:
            st.error(f"Ocorreu um erro ao processar o arquivo: {e}")

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
            else:
                st.warning("Por favor, preencha todos os campos.")

# --- Validação de Dados ---
df = st.session_state.df.copy()
if not df.empty:
    required_cols = ['Data', 'Descrição', 'Valor', 'Tipo', 'Categoria']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        st.error(f"Faltam colunas essenciais: {', '.join(missing_cols)}")
    else:
        df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
        df = df.dropna(subset=['Data'])
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
        df = df.dropna(subset=['Valor'])
        df = df[df['Tipo'].isin(['Receita', 'Despesa'])]

# --- Seleção de Período ---
st.markdown("<div class='content-section'>", unsafe_allow_html=True)
col_month_nav, col_period_selection = st.columns([1, 3])

with col_month_nav:
    st.markdown("### ← Fevereiro →")

with col_period_selection:
    col_buttons, col_date_picker, col_clear_button = st.columns([2, 3, 1])
    
    with col_buttons:
        st.markdown("<div class='period-buttons-container'>", unsafe_allow_html=True)
        if st.button("Essa semana"):
            today = datetime.now().date()
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)
            st.session_state.start_date = start_date
            st.session_state.end_date = end_date
        if st.button("Esse mês"):
            today = datetime.now().date()
            start_date = today.replace(day=1)
            end_date = (today.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
            st.session_state.start_date = start_date
            st.session_state.end_date = end_date
        if st.button("Hoje"):
            today = datetime.now().date()
            st.session_state.start_date = today
            st.session_state.end_date = today
        st.markdown("</div>", unsafe_allow_html=True)

    with col_date_picker:
        if 'start_date' not in st.session_state or 'end_date' not in st.session_state:
            today = datetime.now().date()
            st.session_state.start_date = today.replace(day=1)
            st.session_state.end_date = (today.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)

        selected_date_range = st.date_input(
            "Período Personalizado",
            value=(st.session_state.start_date, st.session_state.end_date),
            key="date_range_picker",
            label_visibility="collapsed"
        )
        
        if len(selected_date_range) == 2:
            st.session_state.start_date, st.session_state.end_date = selected_date_range

    with col_clear_button:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("Limpar"):
            st.session_state.start_date = None
            st.session_state.end_date = None

st.markdown("</div>", unsafe_allow_html=True)

# --- Filtro de Dados ---
if not df.empty and 'start_date' in st.session_state and 'end_date' in st.session_state:
    df_filtered = df[
        (df['Data'].dt.date >= st.session_state.start_date) &
        (df['Data'].dt.date <= st.session_state.end_date)
    ].copy()
else:
    df_filtered = pd.DataFrame(columns=df.columns)

# Calcula período do mês anterior
today = datetime.now().date()
first_day_current_month = today.replace(day=1)
last_day_prev_month = first_day_current_month - timedelta(days=1)
first_day_prev_month = last_day_prev_month.replace(day=1)

# --- Cards de Métricas ---
st.markdown("<div class='content-section'>", unsafe_allow_html=True)
col_saldo, col_receitas, col_despesas, col_investimentos = st.columns(4)

if not df.empty and not df_filtered.empty:
    total_receitas, total_despesas, saldo_atual, prev_month_saldo = calculate_metrics(
        df_filtered, st.session_state.start_date, st.session_state.end_date, 
        first_day_prev_month, last_day_prev_month
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
        st.markdown(f"""
        <div class="metric-card">
            <h3>Investimentos</h3>
            <div style="font-size: 1.8em; font-weight: bold; color: #007bff;">R$ 0,00</div>
            <div style="font-size: 0.8em; color: #888;">(Dados não disponíveis)</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Carregue dados ou adicione lançamentos para ver as métricas.")

st.markdown("</div>", unsafe_allow_html=True)

# --- Gráficos e Tabelas ---
st.markdown("<div class='content-section'>", unsafe_allow_html=True)
col_monthly_chart, col_expense_summary = st.columns([2, 1])

with col_monthly_chart:
    st.subheader("Entradas e Saídas Mensal")
    if not df_filtered.empty:
        df_filtered['AnoMes'] = df_filtered['Data'].dt.to_period('M').astype(str)
        df_monthly_summary = df_filtered.groupby(['AnoMes', 'Tipo'])['Valor'].sum().unstack(fill_value=0).reset_index()
        
        if 'Receita' not in df_monthly_summary.columns:
            df_monthly_summary['Receita'] = 0
        if 'Despesa' not in df_monthly_summary.columns:
            df_monthly_summary['Despesa'] = 0

        df_monthly_summary['AnoMes_Sort'] = pd.to_datetime(df_monthly_summary['AnoMes'])
        df_monthly_summary = df_monthly_summary.sort_values('AnoMes_Sort')

        fig_monthly_flow, ax_monthly_flow = plt.subplots(figsize=(10, 5))
        bar_width = 0.35
        r_index = np.arange(len(df_monthly_summary['AnoMes']))
        
        ax_monthly_flow.bar(r_index - bar_width/2, df_monthly_summary['Receita'], color='#28a745', width=bar_width, label='Receita')
        ax_monthly_flow.bar(r_index + bar_width/2, df_monthly_summary['Despesa'], color='#dc3545', width=bar_width, label='Despesa')

        ax_monthly_flow.set_xlabel('Mês/Ano')
        ax_monthly_flow.set_ylabel('Valor (R$)')
        ax_monthly_flow.set_xticks(r_index)
        ax_monthly_flow.set_xticklabels(df_monthly_summary['AnoMes'], rotation=45, ha='right')
        ax_monthly_flow.legend()
        ax_monthly_flow.grid(axis='y', linestyle='--', alpha=0.7)
        ax_monthly_flow.yaxis.set_major_formatter(mticker.FormatStrFormatter('R$ %.2f'))
        plt.tight_layout()
        st.pyplot(fig_monthly_flow)
        plt.close(fig_monthly_flow)
    else:
        st.info("Nenhum dado disponível para o período selecionado.")

with col_expense_summary:
    st.subheader("Resumo das Despesas")
    if not df_filtered.empty:
        df_despesas_summary = df_filtered[df_filtered['Tipo'] == 'Despesa'].copy()
        if not df_despesas_summary.empty:
            expense_summary = df_despesas_summary.groupby('Categoria')['Valor'].sum().reset_index()
            expense_summary.columns = ['Categoria', 'Gastos']
            expense_summary = expense_summary.sort_values('Gastos', ascending=False)
            
            total_expenses = expense_summary['Gastos'].sum()
            total_income = df_filtered[df_filtered['Tipo'] == 'Receita']['Valor'].sum()
            
            expense_summary['% das Despesas'] = (expense_summary['Gastos'] / total_expenses * 100).map('{:.2f}%'.format)
            expense_summary['% da Receita'] = (expense_summary['Gastos'] / total_income * 100).map('{:.2f}%'.format) if total_income > 0 else '0.00%'
            
            st.dataframe(expense_summary, use_container_width=True)
        else:
            st.info("Nenhuma despesa no período selecionado.")
    else:
        st.info("Nenhum dado disponível.")

st.markdown("</div>", unsafe_allow_html=True)

# --- Últimas Transações e Gráfico de Pizza ---
st.markdown("<div class='content-section'>", unsafe_allow_html=True)
col_transactions, col_expense_type_chart = st.columns([2, 1])

with col_transactions:
    st.subheader("Últimas Transações")
    search_query = st.text_input("Pesquisar receitas ou gastos", key="search_transactions")

    df_display = df_filtered.copy()
    if search_query:
        df_display = df_display[
            df_display['Descrição'].str.contains(search_query, case=False, na=False) |
            df_display['Categoria'].str.contains(search_query, case=False, na=False)
        ]

    tab_all, tab_expenses, tab_income = st.tabs(["Todas", "Despesas", "Receitas"])
    
    with tab_all:
        st.dataframe(df_display[['Data', 'Descrição', 'Valor', 'Tipo', 'Categoria']].tail(10), use_container_width=True)
    with tab_expenses:
        st.dataframe(df_display[df_display['Tipo'] == 'Despesa'][['Data', 'Descrição', 'Valor', 'Categoria']].tail(10), use_container_width=True)
    with tab_income:
        st.dataframe(df_display[df_display['Tipo'] == 'Receita'][['Data', 'Descrição', 'Valor', 'Categoria']].tail(10), use_container_width=True)

with col_expense_type_chart:
    st.subheader("Gastos por Tipo de Despesa")
    if not df_filtered.empty:
        df_despesas_type = df_filtered[df_filtered['Tipo'] == 'Despesa'].copy()
        
        if not df_despesas_type.empty:
            fixed_categories = ['Moradia', 'Internet', 'Seguros', 'Assinaturas']
            df_despesas_type['Tipo_Gasto'] = df_despesas_type['Categoria'].apply(
                lambda x: 'Fixa' if x in fixed_categories else 'Variável'
            )

            gastos_por_tipo = df_despesas_type.groupby('Tipo_Gasto')['Valor'].sum()
            
            fig_expense_type, ax_expense_type = plt.subplots(figsize=(6, 6))
            ax_expense_type.pie(gastos_por_tipo, labels=gastos_por_tipo.index,
                              autopct='%1.1f%%', startangle=90, wedgeprops={'width': 0.4})
            ax_expense_type.set_title('Distribuição de Gastos')
            ax_expense_type.axis('equal')
            st.pyplot(fig_expense_type)
            plt.close(fig_expense_type)
        else:
            st.info("Nenhuma despesa no período.")
    else:
        st.info("Nenhum dado disponível.")

st.markdown("</div>", unsafe_allow_html=True)

# --- Saldo Acumulado ---
st.markdown("<div class='content-section'>", unsafe_allow_html=True)
st.subheader("Evolução do Saldo Acumulado")
if not df_filtered.empty:
    df_saldo = df_filtered.copy()
    df_saldo = df_saldo.sort_values('Data')
    df_saldo['Valor_Ajustado'] = df_saldo.apply(
        lambda x: x['Valor'] if x['Tipo'] == 'Receita' else -x['Valor'], axis=1
    )
    df_saldo['Saldo_Acumulado'] = df_saldo['Valor_Ajustado'].cumsum()

    fig_saldo, ax_saldo = plt.subplots(figsize=(12, 6))
    ax_saldo.plot(df_saldo['Data'], df_saldo['Saldo_Acumulado'], marker='o', linestyle='-', color='#007bff')
    ax_saldo.set_title('Saldo Acumulado')
    ax_saldo.set_xlabel('Data')
    ax_saldo.set_ylabel('Saldo (R$)')
    ax_saldo.grid(True)
    ax_saldo.yaxis.set_major_formatter(mticker.FormatStrFormatter('R$ %.2f'))
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig_saldo)
    plt.close(fig_saldo)
else:
    st.info("Nenhum dado disponível para o período selecionado.")

st.markdown("</div>", unsafe_allow_html=True)

# --- Estratégias ---
st.markdown("<div class='content-section'>", unsafe_allow_html=True)
st.header("Estratégias para Melhorar o Rendimento Mensal")
if not df_filtered.empty and 'saldo_atual' in locals():
    df_despesas_filtered = df_filtered[df_filtered['Tipo'] == 'Despesa']
    top_despesas = pd.Series()
    if not df_despesas_filtered.empty:
        top_despesas = df_despesas_filtered.groupby('Categoria')['Valor'].sum().nlargest(5)

    if saldo_atual < 0:
        st.markdown(f"**Seu saldo atual é negativo (R$ {saldo_atual:,.2f}).** Foque em reduzir despesas.")
        if not top_despesas.empty:
            st.markdown("**Principais categorias de gastos:**")
            for categoria, valor in top_despesas.items():
                st.markdown(f"- **{categoria}**: R$ {valor:,.2f}")
    elif saldo_atual >= 0 and total_despesas > (total_receitas * 0.7):
        st.markdown(f"**Seu saldo é positivo (R$ {saldo_atual:,.2f}), mas suas despesas são altas.** Otimize seus gastos.")
    else:
        st.markdown(f"**Parabéns! Seu saldo é saudável (R$ {saldo_atual:,.2f}).** Considere investir o excedente.")
else:
    st.info("Carregue dados para receber estratégias personalizadas.")

st.markdown("</div>", unsafe_allow_html=True)

# --- Rodapé ---
st.markdown("---")
st.markdown("Desenvolvido com Streamlit e Matplotlib para uma experiência de análise financeira intuitiva.")

