import pandas as pd 
import numpy as np 

#Obtendo os dados
try:
    print('Obetendo os dados...')


    ENDEREÇO_DADOS='https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    #utf-8 , iso-8859-1, latin1 , cp1252 
    df_ocorrencias = pd.read_csv(ENDEREÇO_DADOS, sep=';', encoding='iso-8859-1')
    # print(df_ocorrencias)

    #delimitando os dados
    df_roubo_veiculo = df_ocorrencias[['munic','roubo_veiculo']]
    # print(df_roubo_veiculo.tail(30))
    # print(df_roubo_veiculo.head(30))

    ###Preparando os dados

    #Totalizando os roubos por cidade (Var Qualitativa 'munic' e Var Quantitativa 'roubo_veiculo') 
    df_roubo_veiculo = df_roubo_veiculo.groupby('munic', as_index=False)['roubo_veiculo'].sum()

    

    #Ordenando os dados
    df_roubo_veiculo = df_roubo_veiculo.sort_values(
        by='roubo_veiculo', 
        ascending =False 
    )

    print(df_roubo_veiculo.head(5))
    print(50*'=')
    print(df_roubo_veiculo.tail(5))


except Exception as e:
    print(f'Erro ao obter os dados - {e}')

try:
    print(f'\n Obtendo Informações a cerca de roubo dos veiculos...')
    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])

    media_roubo_veiculo = np.mean(array_roubo_veiculo)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)
    #quantificar a distancia da media para mediana 
    distancia = abs((media_roubo_veiculo - mediana_roubo_veiculo)
                    / mediana_roubo_veiculo *100 )



    print('\n Medidas de Tendencia Central')
    print(f'Media: {media_roubo_veiculo}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distancia Média - Mediana: {distancia} %')

except Exception as e:
    print(f'Obetendo Medidas -{e}')

try: 
    q1 = np.quantile(array_roubo_veiculo, .25)
    q2 = np.quantile(array_roubo_veiculo, .50)
    q3 = np.quantile(array_roubo_veiculo, .75)

# Cidades c/ menos ocorrências de roubos 
    df_roubo_veiculo_menores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] <q1]
    df_roubo_veiculo_menores.to_csv('menores.csv',index=False)  #----- transforma o codigo em arquivo csv

#cidade c / maiores ocorrencias de roubos 
    
    df_roubo_veiculo_maiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] >q3]
    df_roubo_veiculo_menores.to_csv('maiores.csv', index=False, sep=';')  #----- transforma o codigo em arquivo csv

#prints 
    print('\n Municipios com menores roubos')
    print(30*'-')
    print(df_roubo_veiculo_menores.sort_values(by= 'roubo_veiculo',ascending=True))

    print('\n Municipios com maiores roubos')
    print(30*'-')
    print(df_roubo_veiculo_maiores.sort_values(by='roubo_veiculo', ascending=False))

    print('\n Medidas de Posição')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')


except Exception as e:
    print(f'Erro ao analisar a distribuição {e} ')


#Achando os outliers
try: 
    #Intervalo Interquartil  que é q3 - q1 , mostrando a distancia entre eles 
    #É a amplitude dos dados mais centrais 
    iqr = q3 - q1

    #calculando os limites

    #superior
    limite_superior = q3 + (1.5 * iqr)

    #inferior
    limite_inferior = q1 - (1.5 * iqr)

    # print(f'\n Limite Superior: {limite_superior}')
    # print(f'\n Limite Inferior: {limite_inferior}') printando numero negativo no inferior, quer dizer que nao teremos outliers inferiores

    #filtrando os outliers menores
    df_roubo_veiculo_outliers_menores = (
        df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < limite_inferior]
    )

    print('\n Municipios com outliers inferiores')
    print(30*'-')
    if len(df_roubo_veiculo_outliers_menores) == 0:
        print('Não há outliers inferiores')
    else:
        print(df_roubo_veiculo_outliers_menores)

    #filtrando os outliers maiore
    df_roubo_veiculo_outliers_maiores = (
        df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limite_superior]
    )

    print('\n Municipios com outliers superiores')
    print(30*'-')
    if len(df_roubo_veiculo_outliers_maiores) == 0:
        print('Não há outliers superiores')
    else:
        print(df_roubo_veiculo_outliers_maiores)



except Exception as e:
    print(f'Erro ao verificar os outliers {e} ')