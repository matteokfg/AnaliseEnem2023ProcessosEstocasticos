import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile
import os

# -----------------------------------------------
# Configuração inicial
# -----------------------------------------------
st.set_page_config(page_title="Análise ENEM 2023 - Completa", layout="wide")
st.title("📚 Análise Detalhada do ENEM 2023")

st.markdown("""
Bem-vindo(a) à análise dos dados do ENEM 2023!
Aqui você poderá explorar o perfil dos candidatos, suas condições socioeconômicas e o desempenho geral.
Também apresentamos uma análise estatística inicial para melhor compreensão dos dados.
""")

with zipfile.ZipFile('microdados_limpos_enem_2023.zip', 'r') as zip_ref:
    zip_ref.extractall(os.getcwd())

# -----------------------------------------------
# Carregar Dados
# -----------------------------------------------
@st.cache_data

def carregar_dados():
    return pd.read_parquet("microdados_limpos_enem_2023.parquet")

df = carregar_dados()

# Criar coluna de REGIAO
regioes = {
    'Norte': ['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO'],
    'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
    'Centro-Oeste': ['DF', 'GO', 'MT', 'MS'],
    'Sudeste': ['ES', 'MG', 'RJ', 'SP'],
    'Sul': ['PR', 'RS', 'SC']
}

def estado_para_regiao(uf):
    for regiao, estados in regioes.items():
        if uf in estados:
            return regiao
    return 'Não informado'

df['REGIAO'] = df['SG_UF_ESC'].map(estado_para_regiao)

# Cálculo do Desempenho Geral
df['MEDIA_GERAL'] = df[['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']].mean(axis=1)


melhores = st.selectbox("Tipo de inscrito a ser analisado: ", ("Geral", "Melhores", "Piores"))

if melhores == "Melhores":
    df = df.sort_values(by='MEDIA_GERAL', ascending=False)
    st.markdown(f"Selecione qual porcentagem de inscritos deve ser analisada:")
    num_percent = st.slider("Porcentagem:", 1, 40, 25)/100
    df = df.head(round(num_percent*len(df))+1)
elif melhores == "Piores":
    df = df.sort_values(by='MEDIA_GERAL', ascending=True)
    st.markdown(f"Selecione qual porcentagem de inscritos deve ser analisada:")
    num_percent = st.slider("Porcentagem:", 1, 40, 25)/100
    df = df.head(round(num_percent*len(df))+1)
else:
    num_percent = 1

# -----------------------------------------------
# Análise Exploratória dos Dados (Primeira Parte)
# -----------------------------------------------

st.header("📘 Análise Exploratória dos Dados")

colunas_numericas = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']

st.subheader("📐 Medidas Estatísticas e Distribuição")
for coluna in colunas_numericas:
    col1, col2 = st.columns([1, 2])
    with col1:
        medidas = {
            'Média': df[coluna].mean(),
            'Mediana': df[coluna].median(),
            'Moda': df[coluna].mode()[0],
            'Desvio Padrão': df[coluna].std(),
            'Variância': df[coluna].var(),
            'Mínimo': df[coluna].min(),
            'Máximo': df[coluna].max(),
            '1º Quartil': df[coluna].quantile(0.25),
            '3º Quartil': df[coluna].quantile(0.75),
            'Amplitude': df[coluna].max() - df[coluna].min(),
            'Assimetria': df[coluna].skew(),
            'Curtose': df[coluna].kurtosis(),
            'Coef. Pearson': 3 * (df[coluna].mean() - df[coluna].median()) / df[coluna].std()
        }
        st.dataframe(pd.DataFrame(medidas, index=["Valor"]).T.round(2))
    with col2:
        fig, ax = plt.subplots()
        sns.histplot(df[coluna], bins=30, kde=True, ax=ax)
        ax.set_title(f'Distribuição: {coluna}')
        st.pyplot(fig)

st.subheader("📦 Boxplot com Médias")
fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(data=df[colunas_numericas], showmeans=True)
ax.set_title("Distribuição das Notas com Médias")
st.pyplot(fig)

st.subheader("📊 Correlação entre Notas")
correlacoes = df[colunas_numericas].corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlacoes, annot=True, cmap="coolwarm", center=0, linewidths=0.5, fmt=".2f")
ax.set_title("Mapa de Calor - Correlação entre Áreas")
st.pyplot(fig)

# Criar coluna de REGIAO
regioes = {
    'Norte': ['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO'],
    'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
    'Centro-Oeste': ['DF', 'GO', 'MT', 'MS'],
    'Sudeste': ['ES', 'MG', 'RJ', 'SP'],
    'Sul': ['PR', 'RS', 'SC']
}

def estado_para_regiao(uf):
    for regiao, estados in regioes.items():
        if uf in estados:
            return regiao
    return 'Não informado'




df['REGIAO'] = df['SG_UF_ESC'].map(estado_para_regiao)

# Cálculo do Desempenho Geral
colunas_notas = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']
df['DESEMPENHO_GERAL'] = df[colunas_notas].mean(axis=1)







# -----------------------------------------------
# Legendas das Variáveis (Etapa 1 e Etapa 2)
# (vou colar as legendas já já — continuo na próxima mensagem para não cortar)
# -----------------------------------------------

# -----------------------------------------------
# Definição das Legendas
# -----------------------------------------------
legendas_etapa1 = {
    "TP_SEXO": {"M": "Masculino", "F": "Feminino"},
    "TP_ESTADO_CIVIL": {0: "Não informado", 1: "Solteiro(a)", 2: "Casado(a)/Companheiro(a)", 3: "Divorciado(a)/Separado(a)", 4: "Viúvo(a)"},
    "TP_COR_RACA": {0: "Não declarado", 1: "Branca", 2: "Preta", 3: "Parda", 4: "Amarela", 5: "Indígena", 6: "Não dispõe da informação"},
    "TP_FAIXA_ETARIA": {
        1: "Menor de 17", 2: "17 anos", 3: "18 anos", 4: "19 anos", 5: "20 anos", 6: "21 anos", 7: "22 anos", 8: "23 anos", 9: "24 anos",
        10: "25 anos", 11: "26-30 anos", 12: "31-35 anos", 13: "36-40 anos", 14: "41-45 anos", 15: "46-50 anos", 16: "51-55 anos",
        17: "56-60 anos", 18: "61-65 anos", 19: "66-70 anos", 20: "Mais de 70"
    },
    "TP_ST_CONCLUSAO": {1: "Concluiu Ensino Médio", 2: "Cursando e conclui em 2023", 3: "Cursando e conclui após 2023", 4: "Não concluiu e não cursa"},
    "TP_ESCOLA": {1: "Não respondeu", 2: "Pública", 3: "Privada"},
    "TP_ENSINO": {1: "Ensino Regular", 2: "Educação Especial - Modalidade Substitutiva"},
    "TP_DEPENDENCIA_ADM_ESC": {1: "Federal", 2: "Estadual", 3: "Municipal", 4: "Privada"}
}

legendas_etapa2 = {
    "Q001": {"A": "Nunca estudou", "B": "Até 4ª série", "C": "Até 8ª série", "D": "Ensino Fundamental completo", "E": "Ensino Médio incompleto", "F": "Faculdade incompleta", "G": "Pós-graduação", "H": "Não sei"},
    "Q002": {"A": "Nunca estudou", "B": "Até 4ª série", "C": "Até 8ª série", "D": "Ensino Fundamental completo", "E": "Ensino Médio incompleto", "F": "Faculdade incompleta", "G": "Pós-graduação", "H": "Não sei"},
    "Q003": {
        "A": "Grupo 1: Trabalhador rural, pescador, criador de animais, extrativista.",
        "B": "Grupo 2: Empresário agrícola, grande produtor.",
        "C": "Grupo 3: Operário, vendedor, trabalhador de serviços gerais.",
        "D": "Grupo 4: Técnico, policial militar, bombeiro, enfermeiro técnico.",
        "E": "Grupo 5: Médico, engenheiro, advogado, professor universitário, pesquisador científico.",
        "F": "Não sei"
    },
    "Q004": {
        "A": "Grupo 1: Trabalhadora rural, pescadora, criadora de animais, extrativista.",
        "B": "Grupo 2: Empresária agrícola, grande produtora.",
        "C": "Grupo 3: Operária, vendedora, trabalhadora de serviços gerais.",
        "D": "Grupo 4: Técnica de laboratório, policial militar, bombeira, enfermeira técnica.",
        "E": "Grupo 5: Médica, engenheira, advogada, professora universitária, pesquisadora científica.",
        "F": "Não sei"
    },
    "Q005": {str(i): str(i) for i in range(1, 21)},
    "Q006": {
        "A": "Nenhuma", "B": "≤ R$1.320", "C": "R$1.320–1.980", "D": "R$1.980–2.640", "E": "R$2.640–3.300", "F": "R$3.300–3.960",
        "G": "R$3.960–5.280", "H": "R$5.280–6.600", "I": "R$6.600–7.920", "J": "R$7.920–9.240", "K": "R$9.240–10.560",
        "L": "R$10.560–11.880", "M": "R$11.880–13.200", "N": "R$13.200–15.840", "O": "R$15.840–19.800",
        "P": "R$19.800–26.400", "Q": "> R$26.400"
    },
    "Q024": {"A": "Não tem", "B": "1 computador", "C": "2 computadores", "D": "3 computadores", "E": "4 ou mais computadores"},
    "Q025": {"A": "Não", "B": "Sim"}
}

# -------------------------------------------------------------------------------------
# Funções Auxiliares
# -------------------------------------------------------------------------------------

# Função para mostrar legenda suspensa
def mostrar_legenda(coluna, etapa):
    legenda = legendas_etapa1.get(coluna) if etapa == 1 else legendas_etapa2.get(coluna)
    if legenda:
        with st.expander("📜 Legenda da Variável"):
            legenda_df = pd.DataFrame(list(legenda.items()), columns=["Código", "Descrição"])
            st.table(legenda_df)

# Função para aplicar filtros dinâmicos
def aplicar_filtros(df_base, filtros, etapa):
    df_filtrado = df_base.copy()

    for coluna, titulo, descricao in filtros:
        st.markdown(f"### 🔎 Filtro: {titulo}")
        st.markdown(f"**Descrição:** {descricao}")
        mostrar_legenda(coluna, etapa)

        opcoes = sorted(df_filtrado[coluna].dropna().unique())
        selecionados = st.multiselect(f"Selecione {titulo}:", opcoes, default=opcoes)
        if selecionados:
            df_filtrado = df_filtrado[df_filtrado[coluna].isin(selecionados)]

    return df_filtrado

# Função para gráfico de Barras (Inscritos)
def plot_grafico(df_dados, coluna, titulo, descricao, eixo_x, etapa):
    st.markdown(f"## {titulo}")
    st.markdown(f"#### Sobre este gráfico:")
    st.markdown(descricao)

    mostrar_legenda(coluna, etapa)

    contagem = df_dados[coluna].value_counts(dropna=False)
    contagem = contagem[contagem > 0].sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(contagem.index.astype(str), contagem.values, edgecolor='black')

    ax.set_xlabel(eixo_x, fontsize=14)
    ax.set_ylabel("Número de Inscritos", fontsize=14)
    ax.tick_params(axis='x', rotation=45)
    ax.set_ylim(0, contagem.values.max() * 1.20)

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + (contagem.values.max() * 0.02),
                f'{int(yval)}', ha='center', va='bottom', fontsize=8, rotation=90)

    st.pyplot(fig)

# Função para gráfico de Boxplot (Desempenho Geral)
def plot_boxplot(df_dados, coluna, titulo, descricao, eixo_x, etapa):
    st.markdown(f"## {titulo}")
    st.markdown(f"#### Sobre este gráfico:")
    st.markdown(descricao)

    mostrar_legenda(coluna, etapa)

    df_plot = df_dados[[coluna, 'DESEMPENHO_GERAL']].dropna()

    # Ordenação decrescente da média
    medias = df_plot.groupby(coluna)['DESEMPENHO_GERAL'].mean().sort_values(ascending=False)
    categorias_ordenadas = medias.index.tolist()
    df_plot[coluna] = pd.Categorical(df_plot[coluna], categories=categorias_ordenadas, ordered=True)

    fig, ax = plt.subplots(figsize=(12, 6))
    df_plot.boxplot(by=coluna, column='DESEMPENHO_GERAL', grid=False, ax=ax)

    ax.set_xlabel(eixo_x, fontsize=14)
    ax.set_ylabel(f"Desempenho {num_percent*100}% {melhores} (Média das Notas)", fontsize=14)
    plt.suptitle("")
    ax.set_title("")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

    # Análise de Resultados
    analise = df_plot.groupby(coluna)['DESEMPENHO_GERAL'].agg(['mean', 'min', 'max', 'var']).sort_values(by='mean', ascending=False)

    melhor_categoria = analise.index[0]
    pior_categoria = analise.index[-1]

    st.markdown(f"#### 📊 Análise de Resultados:")
    st.markdown(f"- **Melhor desempenho médio**: `{melhor_categoria}` (**{analise.iloc[0]['mean']:.2f} pontos**).")
    st.markdown(f"- **Pior desempenho médio**: `{pior_categoria}` (**{analise.iloc[-1]['mean']:.2f} pontos**).")
    st.markdown(f"- **Maior nota registrada**: **{df_plot['DESEMPENHO_GERAL'].max():.2f} pontos**.")
    st.markdown(f"- **Menor nota registrada**: **{df_plot['DESEMPENHO_GERAL'].min():.2f} pontos**.")
    st.markdown(f"- Categorias com maior variância indicam maior dispersão no desempenho dos participantes.")

# -------------------------------------------------------------------------------------
# ETAPA 1: Perfil Demográfico dos Inscritos
# -------------------------------------------------------------------------------------
st.header("📊 Etapa 1: Perfil Demográfico dos Inscritos")
st.markdown("Análise do perfil de idade, sexo, raça, tipo de escola e outras características dos participantes do ENEM 2023.")

# Filtros da Etapa 1
filtros_etapa1 = [
    ('TP_SEXO', 'Sexo', 'Gênero informado pelo participante.'),
    ('TP_FAIXA_ETARIA', 'Faixa Etária', 'Faixa de idade do participante.'),
    ('TP_ESTADO_CIVIL', 'Estado Civil', 'Estado civil informado.'),
    ('TP_COR_RACA', 'Cor/Raça', 'Autoidentificação racial.'),
    ('TP_ST_CONCLUSAO', 'Conclusão do Ensino Médio', 'Status de conclusão do Ensino Médio.'),
    ('TP_ESCOLA', 'Tipo de Escola', 'Rede de ensino frequentada no Ensino Médio.'),
    ('TP_ENSINO', 'Tipo de Ensino Médio', 'Modalidade cursada.'),
    ('TP_DEPENDENCIA_ADM_ESC', 'Dependência Administrativa da Escola', 'Administração da escola (federal, estadual, etc.).'),
    ('REGIAO', 'Região do Brasil', 'Região associada ao estado da escola.')
]



# Aplicar filtros e gerar dados filtrados
df_etapa1 = aplicar_filtros(df, filtros_etapa1, etapa=1)

# Gráfico Principal: Total de Inscritos por Estado
plot_grafico(df_etapa1, 'SG_UF_ESC', "Distribuição de Inscritos por Estado - Etapa 1",
             "Visualização do total de participantes inscritos em cada estado, considerando os filtros aplicados.", "Estado", etapa=1)

# Gráfico Principal: Boxplot de Desempenho por Estado
plot_boxplot(df_etapa1, 'SG_UF_ESC', f"Desempenho {num_percent*100}% {melhores} dos Inscritos por Estado - Etapa 1",
             "Análise do desempenho médio dos participantes em cada estado, considerando os filtros aplicados.", "Estado", etapa=1)

# Gráficos Adicionais (barras + boxplot) para outras variáveis
variaveis_etapa1 = [
    ('TP_SEXO', "Sexo"),
    ('TP_FAIXA_ETARIA', "Faixa Etária"),
    ('TP_ESTADO_CIVIL', "Estado Civil"),
    ('TP_COR_RACA', "Cor/Raça"),
    ('TP_ST_CONCLUSAO', "Conclusão do Ensino Médio"),
    ('TP_ESCOLA', "Tipo de Escola"),
    ('TP_ENSINO', "Tipo de Ensino Médio"),
    ('TP_DEPENDENCIA_ADM_ESC', "Dependência Administrativa da Escola")
]

for coluna, titulo in variaveis_etapa1:
    plot_grafico(df_etapa1, coluna, f"Distribuição dos Inscritos por {titulo} - Etapa 1",
                 f"Distribuição dos candidatos em relação a {titulo.lower()}.", eixo_x=titulo, etapa=1)
    
    plot_boxplot(df_etapa1, coluna, f"Desempenho {num_percent*100}% {melhores} dos Inscritos por {titulo} - Etapa 1",
                 f"Analisamos como o desempenho geral varia conforme {titulo.lower()}.", eixo_x=titulo, etapa=1)

# -------------------------------------------------------------------------------------
# ETAPA 2: Perfil Socioeconômico dos Inscritos
# -------------------------------------------------------------------------------------
st.header("📊 Etapa 2: Perfil Socioeconômico dos Inscritos")
st.markdown("Análise do contexto socioeconômico dos participantes do ENEM 2023.")

# Filtros da Etapa 2
filtros_etapa2 = [
    ('Q001', 'Escolaridade do Pai', 'Maior nível de escolaridade alcançado pelo pai.'),
    ('Q002', 'Escolaridade da Mãe', 'Maior nível de escolaridade alcançado pela mãe.'),
    ('Q003', 'Ocupação do Pai', 'Principal ocupação exercida pelo pai.'),
    ('Q004', 'Ocupação da Mãe', 'Principal ocupação exercida pela mãe.'),
    ('Q005', 'Número de Pessoas na Residência', 'Número de moradores na casa.'),
    ('Q006', 'Renda Familiar', 'Faixa de renda mensal da família.'),
    ('Q024', 'Quantidade de Computadores', 'Número de computadores disponíveis na residência.'),
    ('Q025', 'Acesso à Internet', 'Possui acesso à internet na residência?')
]

# Aplicar filtros
df_etapa2 = aplicar_filtros(df, filtros_etapa2, etapa=2)

# Gráfico Principal: Total de Inscritos por Estado
plot_grafico(df_etapa2, 'SG_UF_ESC', "Distribuição de Inscritos por Estado - Etapa 2",
             "Visualização do total de participantes inscritos em cada estado, considerando o perfil socioeconômico.", "Estado", etapa=2)

# Gráfico Principal: Boxplot de Desempenho por Estado
plot_boxplot(df_etapa2, 'SG_UF_ESC', f"Desempenho {num_percent*100}% {melhores} dos Inscritos por Estado - Etapa 2",
             "Análise do desempenho médio dos participantes em cada estado, com filtros socioeconômicos aplicados.", "Estado", etapa=2)

# Gráficos Adicionais (barras + boxplot) para outras variáveis
variaveis_etapa2 = [
    ('Q002', "Escolaridade da Mãe"),
    ('Q001', "Escolaridade do Pai"),
    ('Q004', "Ocupação da Mãe"),
    ('Q003', "Ocupação do Pai"),
    ('Q005', "Número de Pessoas na Residência"),
    ('Q006', "Renda Familiar"),
    ('Q024', "Quantidade de Computadores"),
    ('Q025', "Acesso à Internet")
]

for coluna, titulo in variaveis_etapa2:
    plot_grafico(df_etapa2, coluna, f"Distribuição dos Inscritos por {titulo} - Etapa 2",
                 f"Distribuição dos candidatos em relação a {titulo.lower()}.", eixo_x=titulo, etapa=2)
    
    plot_boxplot(df_etapa2, coluna, f"Desempenho {num_percent*100}% {melhores} dos Inscritos por {titulo} - Etapa 2",
                 f"Analisamos como o desempenho geral varia conforme {titulo.lower()}.", eixo_x=titulo, etapa=2)
