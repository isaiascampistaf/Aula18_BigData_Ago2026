import pandas as pd 
import numpy as np 


#obtendo os dados

try: 
    print('Obtendo os dados...')


    ENDEREÇO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    df_ocorrencias = pd.read_csv(ENDEREÇO_DADOS,sep=';',encoding= 'iso-8859-1')

    # print(df_ocorrencias)

    df_estelionato = df_ocorrencias[['mes_ano','estelionato']]

    # print(df_estelionato)

    df_estelionato = df_ocorrencias.groupby('mes_ano',as_index=False)['estelionato'].sum()

    # print(df_estelionato)

    df_estelionato = df_estelionato.sort_values(
        by= 'estelionato', ascending= False 
    ) 
    
    
    
    # df_estelionato2 = df_estelionato.sort_values(
        # by = 'estelionato', ascending=True
    # )

    print(50*'=')
    print('Meses e anos com maiores registros')
    print(df_estelionato.head(10))
    print(50*'=')
    print('Meses e anos com menores registros')
    print(df_estelionato.tail(10))


except Exception as e:
    print(f'Erro ao obter os dados - {e}')

try:
    array_df_estelionato = np.array(df_estelionato['estelionato'])

    media_df_estelionato = np.mean(array_df_estelionato)
    mediana_df_estelionato = np.median(array_df_estelionato)

    distancia = abs((media_df_estelionato - mediana_df_estelionato) / mediana_df_estelionato * 100)

    print(50*'=')
    print('\n Medidas de Tendencia Central')
    print(f'Media: {media_df_estelionato}')
    print(f'Mediana: {mediana_df_estelionato}')
    print(f'Distancia Média - Mediana: {distancia} %')
    print(50*'=')

except Exception as e:
    print(f'Obtendo medidas {e}')


try:
    q1= np.quantile(array_df_estelionato, .25)
    q2= np.quantile(array_df_estelionato, .50)
    q3= np.quantile(array_df_estelionato, .75)

    df_estelionato_menores = df_estelionato[df_estelionato['estelionato']<q1]

    

    df_estelionato_maiores = df_estelionato[df_estelionato['estelionato']<q3]

    print('Meses e anos com menores indices')
    print(df_estelionato_menores.sort_values(by='estelionato',ascending=True))

    print(50*'=')
    print('Meses e anos com maiores indices')
    print(df_estelionato_maiores.sort_values(by='estelionato',ascending=False))

    print('\nMedidas de posição')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')
    
    print('Existe uma tendencia de crescimento ao longo dos anos considerando que os maiores indices ocorrem após 2010, porém não é possivel definir um padrão pois a distância entre a média e a mediana é de 50% ')


except Exception as e:
    print(f'Erro ao analisar a distribuição {e}')


try:
    iqr = q3 - q1 

    limite_superior = q3 + (1.5 * iqr)

    limite_inferior = q1 - (1.5 * iqr)
    print(50*'=')
    print(f'\n Limite Superior: {limite_superior}')
    print(f'\n Limite Inferior: {limite_inferior}')

    df_estelionato_outliers_menor = (
        df_estelionato[df_estelionato['estelionato'] < limite_inferior]
    )
    print(50*'=')
    print('\nMunicipios com outliers inferiores ')
    if len(df_estelionato_outliers_menor) == 0:
        print('Não há outliers inferiores')
    else:
        print(df_estelionato_outliers_menor)

    df_estelionato_outliers_maior = (
        df_estelionato[df_estelionato['estelionato'] > limite_superior]
    )
    print(50*'=')
    print('\n Municipios com outliers superiores')
    if len(df_estelionato_outliers_maior) == 0:
        print('Não há outliers superiores')

    else:
        print(df_estelionato_outliers_maior)

except Exception as e:
    print(f'Erro ao verificar os outliers {e}')
