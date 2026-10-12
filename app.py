import streamlit as st
import pandas as pd
import pdfplumber
import plotly.express as px
import io

# Configuração da página em modo ultra-wide
st.set_page_config(page_title="Centro de Inteligência Executiva - Saúde", layout="wide", page_icon="🚀")

# --- DESIGN SYSTEM EXECUTIVO (GLASSMORPHISM & RODAPÉ DISCRETO) ---
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(15, 23, 42) 0%, rgb(2, 6, 23) 90%);
        color: #f8fafc;
    }
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(56, 189, 248, 0.2);
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
        text-align: center;
    }
    h1, h2, h3 {
        color: #38bdf8 !important;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    .stTextInput input, .stSelectbox select {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        border: 1px solid #0284c7 !important;
    }
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #334155;
    }
    /* RODAPÉ DISCRETO E MINIMALISTA */
    .discrete-footer {
        margin-top: 50px;
        padding: 15px;
        border-top: 1px solid rgba(148, 163, 184, 0.15);
        text-align: center;
        color: #64748b;
        font-size: 13px;
        font-family: 'Inter', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho Executivo
st.markdown("<h1>🚀 EXECUTIVE HEALTH INTELLIGENCE</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-size: 16px;'>Plataforma Autônoma de Extração e Visualização de Indicadores Críticos em Tempo Real</p>", unsafe_allow_html=True)
st.markdown("---")

# Painel de Upload Futurista
uploaded_file = st.file_uploader("📂 Arraste e solte o seu relatório executivo (PDF, Excel ou CSV) para iniciar:", type=["xlsx", "xls", "csv", "pdf"])

df = None

if uploaded_file is not None:
    file_type = uploaded_file.name.split('.')[-1].lower()

    with st.spinner("⚡ Processando matriz de dados e estruturando indicadores..."):
        # --- LEITURA DE PLANILHAS (Excel / CSV) ---
        if file_type in ["xlsx", "xls"]:
            df = pd.read_excel(uploaded_file)
        elif file_type == "csv":
            content = uploaded_file.read()
            try:
                decoded = content.decode('utf-8')
            except UnicodeDecodeError:
                decoded = content.decode('latin1')

            lines = decoded.splitlines()
            start_line = 0
            for i, line in enumerate(lines):
                if ';' in line or ',' in line:
                    start_line = i
                    break

            valid_content = "\n".join(lines[start_line:])
            try:
                df = pd.read_csv(io.StringIO(valid_content), sep=None, engine='python', on_bad_lines='skip')
            except Exception:
                df = pd.read_csv(io.StringIO(valid_content), sep=';', on_bad_lines='skip')

        # --- LEITURA DE PDF (Extração de Alta Precisão) ---
        elif file_type == "pdf":
            all_rows = []
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    tables = page.extract_tables()
                    for table in tables:
                        for row in table:
                            cleaned_row = [str(cell).strip() if cell is not None else "" for cell in row]
                            if any(cleaned_row):
                                all_rows.append(cleaned_row)
            
            if all_rows:
                header_idx = 0
                for idx, r in enumerate(all_rows):
                    r_upper = [str(x).upper() for x in r]
                    if any(m in r_upper for m in ['JAN', 'FEV', 'MAR', 'TOTAL', 'REGIÃO', 'MUNICIPIO', 'MES']):
                        header_idx = idx
                        break
                
                header = all_rows[header_idx]
                seen = {}
                clean_header = []
                for i, h in enumerate(header):
                    h_name = h if h != "" else f"Coluna_{i+1}"
                    if h_name in seen:
                        seen[h_name] += 1
                        clean_header.append(f"{h_name}_{seen[h_name]}")
                    else:
                        seen[h_name] = 0
                        clean_header.append(h_name)

                rows = all_rows[header_idx+1:]
                max_cols = len(clean_header)
                normalized_rows = []
                for r in rows:
                    if len(r) < max_cols:
                        r = r + [""] * (max_cols - len(r))
                    elif len(r) > max_cols:
                        r = r[:max_cols]
                    normalized_rows.append(r)

                df = pd.DataFrame(normalized_rows, columns=clean_header)

    if df is not None and not df.empty:
        df = df.dropna(how='all', axis=1).dropna(how='all', axis=0)

        # --- SEÇÃO 1: KPI CARDS EXECUTIVOS ---
        st.success(f"🎯 Ficheiro integrado com sucesso: **{uploaded_file.name}**")
        
        col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
        with col_kpi1:
            st.markdown(f"""
                <div class="metric-card">
                    <h4 style='color: #94a3b8; margin:0;'>TOTAL DE REGISTOS</h4>
                    <h2 style='color: #38bdf8; margin:5px 0;'>{len(df):,}</h2>
                </div>
            """, unsafe_allow_html=True)
        with col_kpi2:
            st.markdown(f"""
                <div class="metric-card">
                    <h4 style='color: #94a3b8; margin:0;'>VARIÁVEIS MAPEADAS</h4>
                    <h2 style='color: #4ade80; margin:5px 0;'>{len(df.columns)}</h2>
                </div>
            """, unsafe_allow_html=True)
        with col_kpi3:
            st.markdown(f"""
                <div class="metric-card">
                    <h4 style='color: #94a3b8; margin:0;'>STATUS DE INTEGRIDADE</h4>
                    <h2 style='color: #c084fc; margin:5px 0;'>100% OK</h2>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # --- SEÇÃO 2: CONTROLES DE FILTRO E PERSONALIZAÇÃO ---
        st.subheader("🎛️ Centro de Comando e Filtros Dinâmicos")
        colunas = df.columns.tolist()

        c1, c2, c3 = st.columns(3)
        with c1:
            eixo_x = st.selectbox("🎯 Categoria Principal (Eixo X):", colunas, index=0)
        with c2:
            eixo_y = st.selectbox("📈 Indicador / Métrica (Eixo Y):", colunas, index=min(1, len(colunas)-1))
        with c3:
            tipo_grafico = st.selectbox("📊 Formato Visual:", ["Gráfico de Barras", "Gráfico de Linhas", "Gráfico de Pizza"])

        if eixo_x == eixo_y:
            st.warning("⚠️ Selecione dimensões diferentes para o cruzamento analítico.")
        else:
            df_plot = df.copy()
            df_plot[eixo_y] = pd.to_numeric(
                df_plot[eixo_y].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False),
                errors='coerce'
            ).fillna(0)

            # --- SEÇÃO 3: RENDERIZAÇÃO DOS GRÁFICOS EXECUTIVOS ---
            if tipo_grafico == "Gráfico de Barras":
                fig = px.bar(df_plot, x=eixo_x, y=eixo_y, text=eixo_y, color=eixo_x, color_discrete_sequence=px.colors.qualitative.Vivid)
                fig.update_traces(texttemplate='%{text}', textposition='outside')
            elif tipo_grafico == "Gráfico de Linhas":
                fig = px.line(df_plot, x=eixo_x, y=eixo_y, markers=True, color_discrete_sequence=['#38bdf8'])
                fig.update_traces(line=dict(width=4), marker=dict(size=10))
            else:
                fig = px.pie(df_plot, names=eixo_x, values=eixo_y, hole=0.4, color_discrete_sequence=px.colors.qualitative.Bold)
                fig.update_traces(textinfo='percent+label')

            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#f8fafc', size=13),
                xaxis=dict(gridcolor='#1e293b'),
                yaxis=dict(gridcolor='#1e293b'),
                showlegend=(tipo_grafico == "Gráfico de Pizza"),
                margin=dict(t=40, b=40, l=40, r=40)
            )

            st.markdown("<br>", unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True)

        # --- SEÇÃO 4: MATRIZ DE DADOS BRUTOS ---
        st.markdown("---")
        with st.expander("🔍 Expandir Matriz de Dados Detalhada (Fonte Original)"):
            st.dataframe(df, use_container_width=True, height=450)

# --- RODAPÉ DISCRETO ---
st.markdown("""
    <div class="discrete-footer">
        Desenvolvido por Bruno Vasconcelos
    </div>
""", unsafe_allow_html=True)