import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuração da Página ---
st.set_page_config(
    page_title="Dashboard de Voos",
    page_icon="✈️",
    layout="wide",
)

# --- Carregamento dos dados ---
df = pd.read_csv("airlines_flights_data.csv")

# --- Barra Lateral (Filtros) ---
st.sidebar.header("🔍 Filtros")

# Companhia aérea
companhias = sorted(df['airline'].unique())
companhias_sel = st.sidebar.multiselect("Companhia Aérea", companhias, default=companhias)

# Cidade de origem
origens = sorted(df['source_city'].unique())
origens_sel = st.sidebar.multiselect("Cidade de Origem", origens, default=origens)

# Cidade de destino
destinos = sorted(df['destination_city'].unique())
destinos_sel = st.sidebar.multiselect("Cidade de Destino", destinos, default=destinos)

# Classe
classes = sorted(df['class'].unique())
classes_sel = st.sidebar.multiselect("Classe", classes, default=classes)

# Paradas
paradas = sorted(df['stops'].unique())
paradas_sel = st.sidebar.multiselect("Paradas", paradas, default=paradas)

# --- Filtragem do DataFrame ---
df_filtrado = df[
    (df['airline'].isin(companhias_sel)) &
    (df['source_city'].isin(origens_sel)) &
    (df['destination_city'].isin(destinos_sel)) &
    (df['class'].isin(classes_sel)) &
    (df['stops'].isin(paradas_sel))
]

# --- Título ---
st.title("📊 Dashboard de Voos")
st.markdown("Explore os preços e características dos voos disponíveis. Use os filtros à esquerda para refinar a análise.")

# --- KPIs ---
st.subheader("Métricas Gerais")
if not df_filtrado.empty:
    preco_medio = df_filtrado['price'].mean()
    preco_max = df_filtrado['price'].max()
    duracao_media = df_filtrado['duration'].mean()
    total_voos = df_filtrado.shape[0]
else:
    preco_medio = preco_max = duracao_media = total_voos = 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Preço médio", f"R${preco_medio:,.2f}")
col2.metric("Preço máximo", f"R${preco_max:,.2f}")
col3.metric("Duração média (h)", f"{duracao_media:.2f}")
col4.metric("Total de voos", f"{total_voos:,}")

st.markdown("---")

# --- Gráficos ---
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        top_aereas = df_filtrado.groupby('airline')['price'].mean().nlargest(10).reset_index()
        fig_top = px.bar(
            top_aereas,
            x='price',
            y='airline',
            orientation='h',
            title="Top 10 companhias por preço médio",
            labels={'price': 'Preço médio (R$)', 'airline': 'Companhia'}
        )
        st.plotly_chart(fig_top, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir.")

with col_graf2:
    if not df_filtrado.empty:
        fig_hist = px.histogram(
            df_filtrado,
            x='price',
            nbins=30,
            title="Distribuição de preços das passagens",
            labels={'price': 'Preço (R$)', 'count': 'Quantidade'}
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir.")

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        classe_counts = df_filtrado['class'].value_counts().reset_index()
        classe_counts.columns = ['classe', 'quantidade']
        fig_pizza = px.pie(
            classe_counts,
            names='classe',
            values='quantidade',
            title="Proporção por classe"
        )
        st.plotly_chart(fig_pizza, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir.")

with col_graf4:
    if not df_filtrado.empty:
        origem_destino = df_filtrado.groupby(['source_city', 'destination_city']).size().reset_index(name='quantidade')
        fig_map = px.scatter_geo(
            origem_destino,
            locations="destination_city",
            locationmode="country names",
            size="quantidade",
            title="Cidades de destino mais frequentes"
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir.")

# --- Tabela ---
st.subheader("Dados Detalhados")
st.dataframe(df_filtrado)
