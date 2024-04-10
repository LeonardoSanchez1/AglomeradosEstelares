import os
import numpy as np
import matplotlib.pyplot as plt
import glob

# Função para calcular os valores e salvar os arquivos filtrados e calculados
def processar_arquivo(nome_arquivo):
    # Lendo os dados do arquivo
    dados = np.loadtxt(nome_arquivo, dtype=str)

    # Convertendo as colunas numéricas relevantes para float
    dados_numericos = dados[:, [13, 14, 15, 16, 17, 18]].astype(float)

    # Calculando os valores
    dados_numericos[:, [1, 3, 5]] /= 1000
    erro_x = np.sqrt(dados_numericos[:, 3]**2 + dados_numericos[:, 5]**2)
    erro_y = np.sqrt(dados_numericos[:, 1]**2 + dados_numericos[:, 3]**2)
    x = dados_numericos[:, 2] - dados_numericos[:, 4]
    y = dados_numericos[:, 0] - dados_numericos[:, 2]

    # Arredondando os valores para duas casas decimais
    y = np.around(y, 2)
    x = np.around(x, 2)
    erro_y = np.around(erro_y, 2)
    erro_x = np.around(erro_x, 2)

    # Adicionando os resultados das contas como colunas adicionais aos dados originais
    dados_com_resultados = np.column_stack((dados, y, x, erro_y, erro_x))

    # Salvando os dados com resultados das contas em um novo arquivo
    nome_arquivo_calculado = nome_arquivo.split('.')[0] + 'Calculado.txt'
    np.savetxt(nome_arquivo_calculado, dados_com_resultados, fmt='%-15s', delimiter='\t')

    # Aplicando as condições fornecidas
    mask = ~(
        ((dados_numericos[:, 0] < 3) | (dados_numericos[:, 0] > 10)) |
        ((dados_numericos[:, 2] < 3) | (dados_numericos[:, 2] > 10)) |
        ((dados_numericos[:, 4] < 3) | (dados_numericos[:, 4] > 10)) |
        ((dados_numericos[:, 1] / 1000) / dados_numericos[:, 0] > 0.01) |
        ((dados_numericos[:, 3] / 1000) / dados_numericos[:, 2] > 0.01) |
        ((dados_numericos[:, 5] / 1000) / dados_numericos[:, 4] > 0.01)
    )

    # Selecionando apenas as linhas que não atendem às condições
    dados_filtrados = dados[mask]

    # Adicionando as colunas dos resultados das contas ao arquivo filtrado
    dados_filtrados_com_resultados = np.column_stack((dados_filtrados, y[mask], x[mask], erro_y[mask], erro_x[mask]))

    # Salvando os dados filtrados com resultados das contas em um novo arquivo
    nome_arquivo_filtrado = nome_arquivo.split('.')[0] + 'Filtrado.txt'
    np.savetxt(nome_arquivo_filtrado, dados_filtrados_com_resultados, fmt='%-15s', delimiter='\t')

    # Calculando os valores do diagrama HR a partir dos dados filtrados
    x = x[mask]
    y = y[mask]
    erro_x = erro_x[mask]
    erro_y = erro_y[mask]

    # Criando o diagrama HR e salvando a imagem
    plt.figure(figsize=(8, 6))
    plt.errorbar(x, y, xerr=erro_x, yerr=erro_y, fmt='o', markersize=5, color='blue', alpha=0.5)
    plt.gca().invert_yaxis()
    plt.xlabel('Índice de Cor (H-K)')
    plt.ylabel('Índice de Cor (J-H)')
    plt.title('Diagrama HR (Filtrado)')
    plt.grid(True)

    # Salvando o diagrama HR
    nome_diagrama = nome_arquivo.split('.')[0] + '_HR_Diagram_Filtrado.png'
    plt.savefig(nome_diagrama)
    plt.close()

    return nome_arquivo_calculado, nome_arquivo_filtrado, nome_diagrama

# Buscando por arquivos .txt na pasta atual
arquivos_txt = glob.glob("*.txt")

# Diretório onde o script está localizado
diretorio_script = os.path.dirname(os.path.realpath(__file__))

# Processando cada arquivo encontrado
for arquivo in arquivos_txt:
    # Criando o nome da pasta de destino
    nome_pasta = os.path.splitext(arquivo)[0]
    # Criando o caminho completo para a pasta de destino
    caminho_pasta_destino = os.path.join(diretorio_script, nome_pasta)
    # Criando a pasta de destino se ela não existir
    if not os.path.exists(caminho_pasta_destino):
        os.makedirs(caminho_pasta_destino)
    # Movendo o arquivo para a pasta de destino
    os.rename(arquivo, os.path.join(caminho_pasta_destino, arquivo))
    # Processando o arquivo
    processar_arquivo(os.path.join(caminho_pasta_destino, arquivo))
