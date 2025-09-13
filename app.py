import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)
# CSS customizado para cores azuis e branco
st.markdown("""
<style>

    /* Fundo geral */
    .stApp {
        background-color: #f0f4f8;
    }

    /* Container azul para títulos */
    .blue-header {
        background-color: #1e3a8a;
        color: white;
        padding: 15px;
        border-radius: 10px 10px 10px 10px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
    }

    /* Estilo para os blocos */
    .block-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);

    }

    /* Métricas customizadas */
    div[data-testid="metric-container"] {
        background-color: #e0f2fe;
        border: 1px solid #3b82f6;
        padding: 10px;
        border-radius: 5px;
        margin: 5px;

    }

    div[data-testid="metric-container"] > div {
        color: #1e40af;
    }
    /* Shadow box para containers específicos */
    .shadow-box > div {
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.9);
        border-radius: 8px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# Função para criar dados de exemplo
def gerar_dados_exemplo():
    np.random.seed(42)
    return {
        'categorias': ['A', 'B', 'C', 'D', 'E'],
        'valores': np.random.randint(10, 100, 5),
        'meses': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai'],
        'vendas': np.random.randint(50, 200, 5),
        'lucro': np.random.randint(20, 80, 5)
    }


# Função para criar gráfico de velocímetro
def criar_velocimetro(valor, titulo):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=valor,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': titulo, 'font': {'color': '#1e3a8a'}},
        gauge={
            'axis': {'range': [None, 100], 'tickcolor': '#1e3a8a'},
            'bar': {'color': '#3b82f6'},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#1e3a8a",
            'steps': [
                {'range': [0, 50], 'color': '#dbeafe'},
                {'range': [50, 80], 'color': '#93c5fd'},
                {'range': [80, 100], 'color': '#60a5fa'}
            ],
            'threshold': {
                'line': {'color': "#1e40af", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        autosize=True,  # Permite redimensionamento automático
    )
    return fig


# Função para criar gráficos de barras
def criar_grafico_barras(dados, x, y, titulo, orientacao='v'):
    cores = ['#1e3a8a', '#2563eb', '#3b82f6', '#60a5fa', '#93c5fd']

    if orientacao == 'v':
        fig = px.bar(
            x=dados[x],
            y=dados[y],
            title=titulo,
            color_discrete_sequence=cores
        )
    else:
        fig = px.bar(
            x=dados[y],
            y=dados[x],
            orientation='h',
            title=titulo,
            color_discrete_sequence=cores
        )

    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color='#1e3a8a',
        title_font_size=16,
        showlegend=False,
        height=300
    )
    fig.update_xaxes(gridcolor='#e0f2fe')
    fig.update_yaxes(gridcolor='#e0f2fe')

    return fig


# Função para criar gráfico de linhas
def criar_grafico_linhas(dados, x, y, titulo):
    fig = px.line(
        x=dados[x],
        y=dados[y],
        title=titulo,
        markers=True
    )
    fig.update_traces(
        line_color='#3b82f6',
        line_width=3,
        marker=dict(size=8, color='#1e3a8a')
    )
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color='#1e3a8a',
        title_font_size=16,
        height=300
    )
    fig.update_xaxes(gridcolor='#e0f2fe')
    fig.update_yaxes(gridcolor='#e0f2fe')

    return fig


# Dados de exemplo
dados = gerar_dados_exemplo()

# Bloco de Filtros
with st.container(border=True, height="content"):
    col1, = st.columns(1)
    with col1:
        st.markdown('<div class="blue-header">Dashboard Hospitalar</div>', unsafe_allow_html=True)

        with st.container(border=True):
            # Criar colunas para o filtro de data
            col_data1, col_data2, col_espaco, col_botao = st.columns([2, 2, 3, 1])

            with col_data1:
                st.markdown("**📅 Data Inicial**")
                data_inicio = st.date_input(
                    "De",
                    value=pd.to_datetime("2024-01-01"),
                    format="DD/MM/YYYY",
                    label_visibility="collapsed"
                )

            with col_data2:
                st.markdown("**📅 Data Final**")
                data_fim = st.date_input(
                    "Até",
                    value=pd.to_datetime("2024-12-31"),
                    format="DD/MM/YYYY",
                    label_visibility="collapsed"
                )

            with col_espaco:
                # Espaço vazio para melhor layout
                st.empty()

            with col_botao:
                st.markdown("<br>", unsafe_allow_html=True)  # Alinha o botão
                if st.button("🔍 Aplicar", type="secondary", use_container_width=True):
                    pass


# Criar layout de 2x2

col1, col2 = st.columns(2)
# PRIMEIRO BLOCO
with col1:
    with st.container(border=True, height='content'):

        st.markdown('<div class="blue-header">Atendimento Hospitalar</div>', unsafe_allow_html=True)
        #st.markdown("<br>", unsafe_allow_html=True)

        # Métricas
        m1, m2, m3 = st.columns(3)
        with m1:
            with st.container(border=True, height="content"):
                st.metric("Total de Internações", "3.450", "+8%")
        with m2:
            with st.container(border=True, height="content"):
                st.metric("Pacientes Novos", "892", "+12%")
        with m3:
            with st.container(border=True, height="content"):
                st.metric("Tempo Médio (dias)", "4.2", "-0.3")

        # Gráficos lado a lado
        g1, g2 = st.columns(2)
        with g1:
            with st.container(border=True, height="content"):
                fig_bar1 = criar_grafico_barras(dados, 'categorias', 'valores', 'Internações por Especialidade')
                st.plotly_chart(fig_bar1, use_container_width=True)
        with g2:
            with st.container(border=True, height="content"):
                fig_velocimetro = criar_velocimetro(75, "Taxa de Ocupação (%)")
                st.plotly_chart(fig_velocimetro, use_container_width=True)

with col2:
    with st.container(border=True, height="content"):

        st.markdown('<div class="blue-header">Convênios Hospitalares</div>', unsafe_allow_html=True)

        # Métricas
        m1, m2, m3 = st.columns(3)
        with m1:
            with st.container(border=True, height="content"):
                st.metric("Faturamento Mensal", "R$ 2.850.000", "+18%")
        with m2:
            with st.container(border=True, height="content"):
                st.metric("Convênios Ativos", "47", "+2")
        with m3:
            with st.container(border=True, height="content"):
                st.metric("Taxa Aprovação", "92%", "+4%")

        # Gráficos lado a lado
        g1, g2 = st.columns(2)
        with g1:
            with st.container(border=True, height="content"):
                fig_bar2 = criar_grafico_barras(dados, 'meses', 'vendas', 'Faturamento por Convênio')
                st.plotly_chart(fig_bar2, use_container_width=True)
        with g2:
            with st.container(border=True, height="content"):
                fig_linha1 = criar_grafico_linhas(dados, 'meses', 'lucro', 'Evolução dos Repasses')
                st.plotly_chart(fig_linha1, use_container_width=True)

# TERCEIRO BLOCO
with col1:
    with st.container(border=True, height="content"):
        st.markdown('<div class="blue-header">Análise de Glosas</div>', unsafe_allow_html=True)

        # Métricas
        m1, m2, m3 = st.columns(3)
        with m1:
            with st.container(border=True, height="content"):
                st.metric("Glosas Totais", "1.247", "+15%")
        with m2:
            with st.container(border=True, height="content"):
                st.metric("Valor Glosado", "R$ 342.500", "+8%")
        with m3:
            with st.container(border=True, height="content"):
                st.metric("Taxa de Glosa", "12.8%", "-2.1%")

        # Dois gráficos de barras
        g1, g2 = st.columns(2)
        with g1:
            # Dados diferentes para variar
            dados2 = {
                'produtos': ['Consultas', 'Exames', 'Cirurgias', 'Internações'],
                'quantidade': [315, 428, 189, 315]
            }
            with st.container(border=True, height="content"):
                fig_bar3 = criar_grafico_barras(dados2, 'produtos', 'quantidade', 'Glosas por Tipo de Procedimento')
                st.plotly_chart(fig_bar3, use_container_width=True)
        with g2:
            # Gráfico de barras horizontal
            dados3 = {
                'regioes': ['Unimed', 'Bradesco Saúde', 'SulAmérica', 'Amil'],
                'vendas': [287, 195, 341, 424]
            }
            with st.container(border=True, height="content"):
                fig_bar4 = criar_grafico_barras(dados3, 'regioes', 'vendas', 'Glosas por Operadora', 'h')
                st.plotly_chart(fig_bar4, use_container_width=True)

# QUARTO BLOCO
with col2:
    with st.container(border=True, height="content"):
        st.markdown('<div class="blue-header">Fluxo de Caixa</div>', unsafe_allow_html=True)

        # Métricas
        m1, m2, m3 = st.columns(3)
        with m1:
            with st.container(border=True, height="content"):
                st.metric("FCL Mensal", "R$ 1.2M", "+18%")
        with m2:
            with st.container(border=True, height="content"):
                st.metric("Margem FCL", "15.3%", "+2.1%")
        with m3:
            with st.container(border=True, height="content"):
                st.metric("Liquidez", "2.4x", "+0.3x")

        # Gráficos lado a lado
        g1, g2 = st.columns(2)
        with g1:
            # Dados para o último gráfico de barras
            dados4 = {
                'equipes': ['Recebimentos', 'Pagamentos', 'Investimentos', 'Financiamentos'],
                'performance': [2850, -1950, -450, 320]
            }
            with st.container(border=True, height="content"):
                fig_bar5 = criar_grafico_barras(dados4, 'equipes', 'performance',
                                                'Componentes do FCL (R$ mil)', 'v')
                st.plotly_chart(fig_bar5, use_container_width=True)
        with g2:
            # Dados para o último gráfico de linhas
            dados5 = {
                'dias': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai'],
                'acessos': [980, 1150, 1320, 1280, 1450]
            }
            with st.container(border=True, height="content"):
                fig_linha2 = criar_grafico_linhas(dados5, 'dias', 'acessos', 'Evolução FCL Mensal (R$ mil)')
                st.plotly_chart(fig_linha2, use_container_width=True)

# Rodapé opcional
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #1e3a8a;'>
        Dashboard desenvolvido com Streamlit | 2025
    </div>
    """,
    unsafe_allow_html=True
)

