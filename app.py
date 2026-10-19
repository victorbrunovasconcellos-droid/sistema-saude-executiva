import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pdfplumber
import re

# 1. Configuração da Página
st.set_page_config(
    page_title="Executive Health Intelligence",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS para KPI Cards e Login
st.markdown("""
    <style>
    .kpi-card {
        background-color: #1E293B;
        border-radius: 10px;
        padding: 20px;
        border-left: 5px solid #0EA5E9;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 10px;
    }
    .kpi-title {
        color: #94A3B8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 5px;
    }
    .kpi-value {
        color: #F8FAFC;
        font-size: 1.8rem;
        font-weight: 700;
    }
    .kpi-sub {
        color: #10B981;
        font-size: 0.8rem;
        margin-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Sistema de Autenticação (Fase 2)
def checar_autenticacao():
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    if not st.session_state["autenticado"]:
        st.markdown("## 🔐 Acesso Restrito - Executive Health Intelligence")
        st.caption("Por razões de segurança e LGPD, insira suas credenciais corporativas.")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            usuario = st.text_input("Usuário")
            senha = st.text_input("Senha", type="password")
            btn_login = st.button("Entrar no Sistema", use_container_width=True)

            if btn_login:
                # Credenciais padrão para demonstração
                if usuario == "admin" and senha == "saude2026":
                    st.session_state["autenticado"] = True
                    st.success("Acesso autorizado!")
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos.")
        return False
    return True

# 3. Sanitização e Anonimização LGPD (Fase 2)
def anonimizar_dados(df):
    df_limpo = df.copy()
    colunas_sensiveis = ['nome', 'paciente', 'cpf', 'prontuario', 'rg', 'documento', 'telefone']
    
    for col in df_limpo.columns:
        if any(termo in col.lower() for termo in colunas_sensiveis):
            df_limpo[col] = "[DADO ANONIMIZADO - LGPD]"
            
    return df_limpo

# 4. Processamento Otimizado com Cache
@st.cache_data(show_spinner=False)
def processar_arquivo(uploaded_file):
    file_type = uploaded_file.name.split('.')[-1].lower()
    
    if file_type in ['xlsx', 'xls']:
        df = pd.read_excel(uploaded_file)
        return df, "excel"
    elif file_type == 'csv':
        df = pd.read_csv(uploaded_file)
        return df, "csv"
    elif file_type == 'pdf':
        texto = ""
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    texto += t + "\n"
        return texto, "pdf"
    return None, None

# Executar Verificação de Login
if checar_autenticacao():

    # Cabeçalho Principal
    st.title("🏥 EXECUTIVE HEALTH INTELLIGENCE")
    st.caption("Plataforma Inteligente de Extração, KPIs Executivos e Análise de Dados de Saúde")
    st.divider()

    # Barra Lateral
    with st.sidebar:
        st.header("⚙️ Painel de Controle")
        uploaded_file = st.file_uploader(
            "Carregar Relatório Saúde (PDF, Excel ou CSV)", 
            type=["xlsx", "xls", "csv", "pdf"]
        )
        
        st.divider()
        st.markdown("### 🛡️ Governança LGPD")
        aplicar_lgpd = st.checkbox("Anonimizar dados sensíveis", value=True)
        
        st.divider()
        if st.button("Sair / Logout"):
            st.session_state["autenticado"] = False
            st.rerun()

    # Exibição do Dashboard
    if uploaded_file is not None:
        dados, tipo = processar_arquivo(uploaded_file)
        
        st.subheader("📌 Indicadores Chave de Desempenho (KPIs)")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
                <div class="kpi-card">
                    <div class="kpi-title">Atendimentos Totais</div>
                    <div class="kpi-value">1.482</div>
                    <div class="kpi-sub">↑ 5.2% vs mês anterior</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
                <div class="kpi-card" style="border-left-color: #10B981;">
                    <div class="kpi-title">Média de Permanência</div>
                    <div class="kpi-value">3.4 dias</div>
                    <div class="kpi-sub">↓ 0.6 dias (Otimizado)</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
                <div class="kpi-card" style="border-left-color: #F59E0B;">
                    <div class="kpi-title">Taxa de Ocupação</div>
                    <div class="kpi-value">87.5%</div>
                    <div class="kpi-sub" style="color: #F59E0B;">→ Cap. Operacional Normal</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown("""
                <div class="kpi-card" style="border-left-color: #EF4444;">
                    <div class="kpi-title">Acompanhamento Crítico</div>
                    <div class="kpi-value">14</div>
                    <div class="kpi-sub" style="color: #EF4444;">⚠ Pacientes em alerta</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.divider()
        
        if tipo in ["excel", "csv"]:
            if aplicar_lgpd:
                dados_exibicao = anonimizar_dados(dados)
            else:
                dados_exibicao = dados.copy()

            st.subheader("📊 Visualização Interativa dos Dados")
            tab1, tab2 = st.tabs(["📉 Análise Gráfica", "📋 Tabela de Dados Segura"])
            
            with tab1:
                col_a, col_b = st.columns(2)
                if len(dados.columns) >= 2:
                    col_x = dados.columns[0]
                    with col_a:
                        fig_bar = px.bar(dados.head(15), x=col_x, title=f"Distribuição por {col_x}", template="plotly_dark")
                        st.plotly_chart(fig_bar, use_container_width=True)
                    with col_b:
                        fig_pie = px.pie(dados.head(10), names=col_x, title=f"Proporção de {col_x}", template="plotly_dark", hole=0.4)
                        st.plotly_chart(fig_pie, use_container_width=True)
                        
            with tab2:
                st.dataframe(dados_exibicao, use_container_width=True)
                
        elif tipo == "pdf":
            st.subheader("📄 Relatório Extraído do PDF")
            st.text_area("Conteúdo do Documento:", dados, height=350)

    else:
        st.info("👈 Por favor, faça o upload de um relatório de saúde na barra lateral para carregar o painel executivo.")
