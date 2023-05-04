
# HIDRO_APP V2

import pandas as pd
import streamlit as st
import calendar
import datetime as dt
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="HidroApp")

with st.sidebar:

    st.markdown("""
    # Bem-vindo ao HidroApp!!!
    """)

    st.divider()

    st.markdown("""
    ## Faça o upload de um arquivo HIDROWEB, seja ele de chuva ou de vazão. 
    """)

    st.markdown("""
    ##### IMPORTANTE: o arquivo deve estar no formato csv! 
    """)

    st.markdown("""
    ##### IMPORTANTE: não altere o nome do arquivo após o download! O HidroApp depende disso para identificar o tipo de arquivo. 
    """)

    st.divider()
    
    file = st.file_uploader('UPLOAD DO ARQUIVO:',type=['csv'])

st.markdown("""
# Análise exploratória dos seus dados:
""")

if file:
    # Extraindo as seis primeiras letras do nome do arquivo para verificar o tipo dele (chuvas/vazoes)
    nome_arq = str(file.name)
    tipo = nome_arq[0:6]


    if tipo=='chuvas':
        # Criando o dataframe pandas para arquivos de chuva:
        #   -> delimiter = delimitador da tabela csv
        #   -> enconding = codificação da tabela
        #   -> index_col = primeira coluna não é index da tabela (false)
        #   -> skiprows = pulas as 12 primeiras linhas para formar a tabela
        df = pd.read_csv(file, delimiter=';', encoding='ISO-8859-1', index_col=False, skiprows=12)

        # Alterar o formato do separador decimal para evitar erros mais à frente
        df = df.replace(',', '.', regex=True)

        # Selecionando os dados que queremos
        lista_de_dados = ['Data', 'NivelConsistencia',
                          'Chuva01', 'Chuva02', 'Chuva03', 'Chuva04', 'Chuva05', 'Chuva06', 'Chuva07', 'Chuva08',
                          'Chuva09', 'Chuva10', 'Chuva11', 'Chuva12', 'Chuva13', 'Chuva14', 'Chuva15', 'Chuva16',
                          'Chuva17', 'Chuva18', 'Chuva19', 'Chuva20', 'Chuva21', 'Chuva22', 'Chuva23', 'Chuva24',
                          'Chuva25', 'Chuva26', 'Chuva27', 'Chuva28', 'Chuva29', 'Chuva30', 'Chuva31']

        df = df[lista_de_dados]

        # Redefinir a coluna 'Data', substituindo o formato 'texto' para o formato 'data'
        df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')

        # Criando listas vazias que serão preenchidas depois
        lista_chuva = []
        lista_data = []
        lista_ano = []
        lista_mes = []
        lista_consistencia = []

        # Iteração a partir do comprimento total da tabela
        # Para cada linha da coluna 'Data' obtém-se o ano e o mês
        for n in range(0, len(df)):

            ano = df['Data'][n].year
            mes = df['Data'][n].month
            consist = df['NivelConsistencia'][n]

            # Iteração para extrair o último dia do mês e evitar errar a localização dos valores diários de chuva
            for dia in range(0, calendar.monthrange(ano, mes)[1]):
                chuva = df.iloc[[n]][df.columns[dia + 2]]

                # Criando a data da da observação no formato 'year-month-day'
                data = dt.date(ano, mes, dia + 1)

                # Adicionando os resultados na lista
                lista_chuva.append(float(chuva.values[0]))
                lista_data.append(data)
                lista_ano.append(int(ano))
                lista_mes.append(int(mes))
                lista_consistencia.append(str(consist))

        # Criando a tabela da série histórica
        datas_serie = pd.Series(lista_data)
        datas_pandas = pd.to_datetime(datas_serie)
        tab_serie = pd.DataFrame(datas_pandas, columns=['Data'])
        tab_serie['Chuva'] = lista_chuva

        # Formatando a coluna Consistencia, substituindo os valores numericos por texto
        consistencia = pd.Series(lista_consistencia).map({'1': 'Bruto', '2': 'Consistido'})
        tab_serie['Consistencia'] = consistencia

        # Inserindo as colunas de Ano e Mes na tabela da série histórica para facilitar na geração dos gráficos
        tab_serie['Ano'] = lista_ano
        tab_serie['Mes'] = lista_mes

        # Filtrando os dados da série histórica por sua consistencia para facilitar na geração dos gráficos
        tab_serie_bruto = tab_serie.query('Consistencia == "Bruto"')
        tab_serie_consist = tab_serie.query('Consistencia == "Consistido"')

        # Agrupando e resumindo os dados
        total_consistencia = tab_serie.groupby('Consistencia').count()['Chuva']
        total_chuva_ano_bruto = tab_serie_bruto[['Ano','Chuva']].groupby('Ano').sum()['Chuva']
        total_chuva_ano_consist = tab_serie_consist[['Ano','Chuva']].groupby('Ano').sum()['Chuva']

        # Resumindo os dados brutos por Ano e Mes, e selecionando os meses separadamente para o boxplot
        jan_bruto = tab_serie_bruto[['Ano','Mes','Chuva']].groupby(['Ano', 'Mes']).sum().query('Mes == 1')['Chuva']
        fev_bruto = tab_serie_bruto[['Ano','Mes','Chuva']].groupby(['Ano', 'Mes']).sum().query('Mes == 2')['Chuva']
        mar_bruto = tab_serie_bruto[['Ano','Mes','Chuva']].groupby(['Ano', 'Mes']).sum().query('Mes == 3')['Chuva']
        abr_bruto = tab_serie_bruto[['Ano','Mes','Chuva']].groupby(['Ano', 'Mes']).sum().query('Mes == 4')['Chuva']
        mai_bruto = tab_serie_bruto[['Ano','Mes','Chuva']].groupby(['Ano', 'Mes']).sum().query('Mes == 5')['Chuva']
        jun_bruto = tab_serie_bruto[['Ano','Mes','Chuva']].groupby(['Ano', 'Mes']).sum().query('Mes == 6')['Chuva']
        jul_bruto = tab_serie_bruto[['Ano','Mes','Chuva']].groupby(['Ano', 'Mes']).sum().query('Mes == 7')['Chuva']
        ago_bruto = tab_serie_bruto[['Ano','Mes','Chuva']].groupby(['Ano', 'Mes']).sum().query('Mes == 8')['Chuva']
        sep_bruto = tab_serie_bruto[['Ano','Mes','Chuva']].groupby(['Ano', 'Mes']).sum().query('Mes == 9')['Chuva']
        out_bruto = tab_serie_bruto[['Ano','Mes','Chuva']].groupby(['Ano', 'Mes']).sum().query('Mes == 10')['Chuva']
        nov_bruto = tab_serie_bruto[['Ano','Mes','Chuva']].groupby(['Ano', 'Mes']).sum().query('Mes == 11')['Chuva']
        dez_bruto = tab_serie_bruto[['Ano','Mes','Chuva']].groupby(['Ano', 'Mes']).sum().query('Mes == 12')['Chuva']

        # Resumindo os dados consistidos por Ano e Mes, e selecionando os meses separadamente para o boxplot
        jan_consist = tab_serie_consist[['Ano','Mes','Chuva']].groupby(['Ano', 'Mes']).sum().query('Mes == 1')['Chuva']
        fev_consist = tab_serie_consist[['Ano','Mes','Chuva']].groupby(['Ano', 'Mes']).sum().query('Mes == 2')['Chuva']
        mar_consist = tab_serie_consist[['Ano','Mes','Chuva']].groupby(['Ano', 'Mes']).sum().query('Mes == 3')['Chuva']
        abr_consist = tab_serie_consist[['Ano','Mes','Chuva']].groupby(['Ano', 'Mes']).sum().query('Mes == 4')['Chuva']
        mai_consist = tab_serie_consist[['Ano','Mes','Chuva']].groupby(['Ano', 'Mes']).sum().query('Mes == 5')['Chuva']
        jun_consist = tab_serie_consist[['Ano','Mes','Chuva']].groupby(['Ano', 'Mes']).sum().query('Mes == 6')['Chuva']
        jul_consist = tab_serie_consist[['Ano','Mes','Chuva']].groupby(['Ano', 'Mes']).sum().query('Mes == 7')['Chuva']
        ago_consist = tab_serie_consist[['Ano','Mes','Chuva']].groupby(['Ano', 'Mes']).sum().query('Mes == 8')['Chuva']
        sep_consist = tab_serie_consist[['Ano','Mes','Chuva']].groupby(['Ano', 'Mes']).sum().query('Mes == 9')['Chuva']
        out_consist = tab_serie_consist[['Ano','Mes','Chuva']].groupby(['Ano', 'Mes']).sum().query('Mes == 10')['Chuva']
        nov_consist = tab_serie_consist[['Ano','Mes','Chuva']].groupby(['Ano', 'Mes']).sum().query('Mes == 11')['Chuva']
        dez_consist = tab_serie_consist[['Ano','Mes','Chuva']].groupby(['Ano', 'Mes']).sum().query('Mes == 12')['Chuva']

        # Gerando gráfico de barras
        st.subheader('Contagem de dias com dados brutos e dados consistidos')
        fig1 = px.bar(total_consistencia, y='Chuva', labels={'Consistencia':'Consistência'})
        st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

        # Gerando gráfico de barras
        st.subheader('Acumulado de chuva por ano')
        tab21, tab22 = st.tabs(['Dados Brutos', 'Dados Consistidos'])
        with tab21:
            fig21 = px.bar(total_chuva_ano_bruto, y='Chuva')
            st.plotly_chart(fig21, theme="streamlit", use_container_width=True)
        with tab22:
            fig22 = px.bar(total_chuva_ano_consist, y='Chuva')
            st.plotly_chart(fig22, theme="streamlit", use_container_width=True)

        # Gerando o boxplot por mês
        st.subheader('Boxplot da chuva acumulada mensal')
        tab31, tab32 = st.tabs(['Dados Brutos', 'Dados Consistidos'])
        with tab31:
            fig31 = go.Figure()
            fig31.add_trace(go.Box(y=jan_bruto, name='Jan', showlegend=False, marker_color='royalblue'))
            fig31.add_trace(go.Box(y=fev_bruto, name='Fev', showlegend=False, marker_color='royalblue'))
            fig31.add_trace(go.Box(y=mar_bruto, name='Mar', showlegend=False, marker_color='royalblue'))
            fig31.add_trace(go.Box(y=abr_bruto, name='Abr', showlegend=False, marker_color='royalblue'))
            fig31.add_trace(go.Box(y=mai_bruto, name='Mai', showlegend=False, marker_color='royalblue'))
            fig31.add_trace(go.Box(y=jun_bruto, name='Jun', showlegend=False, marker_color='royalblue'))
            fig31.add_trace(go.Box(y=jul_bruto, name='Jul', showlegend=False, marker_color='royalblue'))
            fig31.add_trace(go.Box(y=ago_bruto, name='Ago', showlegend=False, marker_color='royalblue'))
            fig31.add_trace(go.Box(y=sep_bruto, name='Set', showlegend=False, marker_color='royalblue'))
            fig31.add_trace(go.Box(y=out_bruto, name='Out', showlegend=False, marker_color='royalblue'))
            fig31.add_trace(go.Box(y=nov_bruto, name='Nov', showlegend=False, marker_color='royalblue'))
            fig31.add_trace(go.Box(y=dez_bruto, name='Dez', showlegend=False, marker_color='royalblue'))
            fig31.update_layout(xaxis_title="Meses", yaxis_title="Chuva")
            st.plotly_chart(fig31, theme="streamlit", use_container_width=True)
        with tab32:
            fig32 = go.Figure()
            fig32.add_trace(go.Box(y=jan_consist, name='Jan', showlegend=False, marker_color='royalblue'))
            fig32.add_trace(go.Box(y=fev_consist, name='Fev', showlegend=False, marker_color='royalblue'))
            fig32.add_trace(go.Box(y=mar_consist, name='Mar', showlegend=False, marker_color='royalblue'))
            fig32.add_trace(go.Box(y=abr_consist, name='Abr', showlegend=False, marker_color='royalblue'))
            fig32.add_trace(go.Box(y=mai_consist, name='Mai', showlegend=False, marker_color='royalblue'))
            fig32.add_trace(go.Box(y=jun_consist, name='Jun', showlegend=False, marker_color='royalblue'))
            fig32.add_trace(go.Box(y=jul_consist, name='Jul', showlegend=False, marker_color='royalblue'))
            fig32.add_trace(go.Box(y=ago_consist, name='Ago', showlegend=False, marker_color='royalblue'))
            fig32.add_trace(go.Box(y=sep_consist, name='Set', showlegend=False, marker_color='royalblue'))
            fig32.add_trace(go.Box(y=out_consist, name='Out', showlegend=False, marker_color='royalblue'))
            fig32.add_trace(go.Box(y=nov_consist, name='Nov', showlegend=False, marker_color='royalblue'))
            fig32.add_trace(go.Box(y=dez_consist, name='Dez', showlegend=False, marker_color='royalblue'))
            fig32.update_layout(xaxis_title="Meses", yaxis_title="Chuva")
            st.plotly_chart(fig32, theme="streamlit", use_container_width=True)

        # Transformando a tabela série histórica em um arquivo CSV
        tab_serie_csv = tab_serie[['Data', 'Chuva', 'Consistencia']]
        tab_serie_csv = tab_serie_csv.to_csv(index=False, sep=';').encode('ISO-8859-1')

        # Gerando o botão para download da tabela com a série histórica em um arquivo CSV
        st.subheader('Baixar a série histórica no formato de arquivo csv')
        st.download_button(
            label="Baixar arquivo csv",
            data=tab_serie_csv,
            file_name='chuva.csv',
            mime='csv')

    elif tipo=='vazoes':
        # Extraindo as seis primeiras letras do nome do arquivo para verificar o tipo dele (chuvas/vazoes)
        #   -> delimiter = delimitador da tabela csv
        #   -> enconding = codificação da tabela
        #   -> index_col = primeira coluna não é index da tabela (false)
        #   -> skiprows = pulas as 13 primeiras linhas para formar a tabela
        df = pd.read_csv(file, delimiter=';', encoding='ISO-8859-1', index_col=False, skiprows=13)

        # Alterar o formato do separador decimal para evitar erros mais à frente
        df = df.replace(',', '.', regex=True)

        # Selecionando os dados que queremos
        lista_de_dados = ['Data', 'NivelConsistencia',
                          'Vazao01', 'Vazao02', 'Vazao03', 'Vazao04', 'Vazao05', 'Vazao06', 'Vazao07', 'Vazao08',
                          'Vazao09', 'Vazao10', 'Vazao11', 'Vazao12', 'Vazao13', 'Vazao14', 'Vazao15', 'Vazao16',
                          'Vazao17', 'Vazao18', 'Vazao19', 'Vazao20', 'Vazao21', 'Vazao22', 'Vazao23', 'Vazao24',
                          'Vazao25', 'Vazao26', 'Vazao27', 'Vazao28', 'Vazao29', 'Vazao30', 'Vazao31']

        df = df[lista_de_dados]

        # Redefinir a coluna 'Data', substituindo o formato 'texto' para o formato 'data'
        df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')

        # Criando listas vazias que serão preenchidas depois
        lista_vazao = []
        lista_data = []
        lista_ano = []
        lista_mes = []
        lista_consistencia = []

        # Iteração a partir do comprimento total da tabela
        # Para cada linha da coluna 'Data' obtém-se o ano e o mês
        for n in range(0, len(df)):

            ano = df['Data'][n].year
            mes = df['Data'][n].month
            consist = df['NivelConsistencia'][n]

            # Iteração para extrair o último dia do mês e evitar errar a localização dos valores diários de chuva
            for dia in range(0, calendar.monthrange(ano, mes)[1]):
                vazao = df.iloc[[n]][df.columns[dia + 2]]

                # Criando a data da observação no formato 'year-month-day'
                data = dt.date(ano, mes, dia + 1)

                # Adicionando os resultados na lista
                lista_vazao.append(float(vazao.values[0]))
                lista_data.append(data)
                lista_ano.append(int(ano))
                lista_mes.append(int(mes))
                lista_consistencia.append(str(consist))

        # Criando a tabela da série histórica
        datas_serie = pd.Series(lista_data)
        datas_pandas = pd.to_datetime(datas_serie)
        tab_serie = pd.DataFrame(datas_pandas, columns=['Data'])
        tab_serie['Vazao'] = lista_vazao

        # Formatando a coluna Consistencia, substituindo os valores numericos por texto
        consistencia = pd.Series(lista_consistencia).map({'1': 'Bruto', '2': 'Consistido'})
        tab_serie['Consistencia'] = consistencia

        # Inserindo as colunas de Ano e Mes na tabela da série histórica para facilitar na geração dos gráficos
        tab_serie['Ano'] = lista_ano
        tab_serie['Mes'] = lista_mes

        # Filtrando os dados da série histórica por sua consistencia para facilitar na geração dos gráficos
        tab_serie_bruto = tab_serie.query('Consistencia == "Bruto"')
        tab_serie_consist = tab_serie.query('Consistencia == "Consistido"')

        # Agrupando e resumindo os dados
        total_consistencia = tab_serie.groupby('Consistencia').count()['Vazao']

        # Resumindo os dados brutos por Ano e Mes, e selecionando os meses separadamente para o boxplot
        jan_bruto = tab_serie_bruto[['Ano','Mes','Vazao']].groupby(['Ano', 'Mes']).mean().query('Mes == 1')['Vazao']
        fev_bruto = tab_serie_bruto[['Ano','Mes','Vazao']].groupby(['Ano', 'Mes']).mean().query('Mes == 2')['Vazao']
        mar_bruto = tab_serie_bruto[['Ano','Mes','Vazao']].groupby(['Ano', 'Mes']).mean().query('Mes == 3')['Vazao']
        abr_bruto = tab_serie_bruto[['Ano','Mes','Vazao']].groupby(['Ano', 'Mes']).mean().query('Mes == 4')['Vazao']
        mai_bruto = tab_serie_bruto[['Ano','Mes','Vazao']].groupby(['Ano', 'Mes']).mean().query('Mes == 5')['Vazao']
        jun_bruto = tab_serie_bruto[['Ano','Mes','Vazao']].groupby(['Ano', 'Mes']).mean().query('Mes == 6')['Vazao']
        jul_bruto = tab_serie_bruto[['Ano','Mes','Vazao']].groupby(['Ano', 'Mes']).mean().query('Mes == 7')['Vazao']
        ago_bruto = tab_serie_bruto[['Ano','Mes','Vazao']].groupby(['Ano', 'Mes']).mean().query('Mes == 8')['Vazao']
        sep_bruto = tab_serie_bruto[['Ano','Mes','Vazao']].groupby(['Ano', 'Mes']).mean().query('Mes == 9')['Vazao']
        out_bruto = tab_serie_bruto[['Ano','Mes','Vazao']].groupby(['Ano', 'Mes']).mean().query('Mes == 10')['Vazao']
        nov_bruto = tab_serie_bruto[['Ano','Mes','Vazao']].groupby(['Ano', 'Mes']).mean().query('Mes == 11')['Vazao']
        dez_bruto = tab_serie_bruto[['Ano','Mes','Vazao']].groupby(['Ano', 'Mes']).mean().query('Mes == 12')['Vazao']

        # Resumindo os dados consistidos por Ano e Mes, e selecionando os meses separadamente para o boxplot
        jan_consist = tab_serie_consist[['Ano','Mes','Vazao']].groupby(['Ano', 'Mes']).mean().query('Mes == 1')['Vazao']
        fev_consist = tab_serie_consist[['Ano','Mes','Vazao']].groupby(['Ano', 'Mes']).mean().query('Mes == 2')['Vazao']
        mar_consist = tab_serie_consist[['Ano','Mes','Vazao']].groupby(['Ano', 'Mes']).mean().query('Mes == 3')['Vazao']
        abr_consist = tab_serie_consist[['Ano','Mes','Vazao']].groupby(['Ano', 'Mes']).mean().query('Mes == 4')['Vazao']
        mai_consist = tab_serie_consist[['Ano','Mes','Vazao']].groupby(['Ano', 'Mes']).mean().query('Mes == 5')['Vazao']
        jun_consist = tab_serie_consist[['Ano','Mes','Vazao']].groupby(['Ano', 'Mes']).mean().query('Mes == 6')['Vazao']
        jul_consist = tab_serie_consist[['Ano','Mes','Vazao']].groupby(['Ano', 'Mes']).mean().query('Mes == 7')['Vazao']
        ago_consist = tab_serie_consist[['Ano','Mes','Vazao']].groupby(['Ano', 'Mes']).mean().query('Mes == 8')['Vazao']
        sep_consist = tab_serie_consist[['Ano','Mes','Vazao']].groupby(['Ano', 'Mes']).mean().query('Mes == 9')['Vazao']
        out_consist = tab_serie_consist[['Ano','Mes','Vazao']].groupby(['Ano', 'Mes']).mean().query('Mes == 10')['Vazao']
        nov_consist = tab_serie_consist[['Ano','Mes','Vazao']].groupby(['Ano', 'Mes']).mean().query('Mes == 11')['Vazao']
        dez_consist = tab_serie_consist[['Ano','Mes','Vazao']].groupby(['Ano', 'Mes']).mean().query('Mes == 12')['Vazao']

        # Gerando gráfico de barras
        st.subheader('Contagem de dias com dados brutos e dados consistidos')
        fig1 = px.bar(total_consistencia, y='Vazao', labels={'Vazao':'Vazão', 'Consistencia':'Consistência'})
        st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

        # Gerando gráfico de linhas
        st.subheader('Histórico das vazões diárias')
        tab21, tab22 = st.tabs(['Dados Brutos', 'Dados Consistidos'])
        with tab21:
            fig21 = px.bar(tab_serie_bruto, x='Data', y='Vazao', labels={'Vazao':'Vazão'})
            st.plotly_chart(fig21, theme="streamlit", use_container_width=True)
        with tab22:
            fig22 = px.bar(tab_serie_consist, x='Data', y='Vazao', labels={'Vazao':'Vazão'})
            st.plotly_chart(fig22, theme="streamlit", use_container_width=True)

        # Gerando o boxplot por mês
        st.subheader('Boxplot das vazões médias mensais')
        tab31, tab32 = st.tabs(['Dados Brutos', 'Dados Consistidos'])
        with tab31:
            fig31 = go.Figure()
            fig31.add_trace(go.Box(y=jan_bruto, name='Jan', showlegend=False, marker_color='royalblue'))
            fig31.add_trace(go.Box(y=fev_bruto, name='Fev', showlegend=False, marker_color='royalblue'))
            fig31.add_trace(go.Box(y=mar_bruto, name='Mar', showlegend=False, marker_color='royalblue'))
            fig31.add_trace(go.Box(y=abr_bruto, name='Abr', showlegend=False, marker_color='royalblue'))
            fig31.add_trace(go.Box(y=mai_bruto, name='Mai', showlegend=False, marker_color='royalblue'))
            fig31.add_trace(go.Box(y=jun_bruto, name='Jun', showlegend=False, marker_color='royalblue'))
            fig31.add_trace(go.Box(y=jul_bruto, name='Jul', showlegend=False, marker_color='royalblue'))
            fig31.add_trace(go.Box(y=ago_bruto, name='Ago', showlegend=False, marker_color='royalblue'))
            fig31.add_trace(go.Box(y=sep_bruto, name='Set', showlegend=False, marker_color='royalblue'))
            fig31.add_trace(go.Box(y=out_bruto, name='Out', showlegend=False, marker_color='royalblue'))
            fig31.add_trace(go.Box(y=nov_bruto, name='Nov', showlegend=False, marker_color='royalblue'))
            fig31.add_trace(go.Box(y=dez_bruto, name='Dez', showlegend=False, marker_color='royalblue'))
            fig31.update_layout(xaxis_title="Meses", yaxis_title="Vazão")
            st.plotly_chart(fig31, theme="streamlit", use_container_width=True)
        with tab32:
            fig32 = go.Figure()
            fig32.add_trace(go.Box(y=jan_consist, name='Jan', showlegend=False, marker_color='royalblue'))
            fig32.add_trace(go.Box(y=fev_consist, name='Fev', showlegend=False, marker_color='royalblue'))
            fig32.add_trace(go.Box(y=mar_consist, name='Mar', showlegend=False, marker_color='royalblue'))
            fig32.add_trace(go.Box(y=abr_consist, name='Abr', showlegend=False, marker_color='royalblue'))
            fig32.add_trace(go.Box(y=mai_consist, name='Mai', showlegend=False, marker_color='royalblue'))
            fig32.add_trace(go.Box(y=jun_consist, name='Jun', showlegend=False, marker_color='royalblue'))
            fig32.add_trace(go.Box(y=jul_consist, name='Jul', showlegend=False, marker_color='royalblue'))
            fig32.add_trace(go.Box(y=ago_consist, name='Ago', showlegend=False, marker_color='royalblue'))
            fig32.add_trace(go.Box(y=sep_consist, name='Set', showlegend=False, marker_color='royalblue'))
            fig32.add_trace(go.Box(y=out_consist, name='Out', showlegend=False, marker_color='royalblue'))
            fig32.add_trace(go.Box(y=nov_consist, name='Nov', showlegend=False, marker_color='royalblue'))
            fig32.add_trace(go.Box(y=dez_consist, name='Dez', showlegend=False, marker_color='royalblue'))
            fig32.update_layout(xaxis_title="Meses", yaxis_title="Vazão")
            st.plotly_chart(fig32, theme="streamlit", use_container_width=True)

        # Transformando a tabela série histórica em um arquivo CSV
        tab_serie_csv = tab_serie[['Data', 'Vazao', 'Consistencia']]
        tab_serie_csv = tab_serie_csv.to_csv(index=False, sep=';').encode('ISO-8859-1')

        # Gerando o botão para download da tabela com a série histórica em um arquivo CSV
        st.subheader('Baixar a série histórica no formato de arquivo csv')
        st.download_button(
            label="Baixar arquivo csv",
            data=tab_serie_csv,
            file_name='vazao.csv',
            mime='csv')

    else:
        st.markdown("""
        #### Não foi possível identificar o arquivo. Para tentar corrigir esse erro:
        """)

        st.markdown("""
        #### 1 - Verifique se o arquivo baixado está no formato csv;
        """)

        st.markdown("""
        #### 2 - Verifique se o nome do arquivo baixado foi alterado;
        """)
