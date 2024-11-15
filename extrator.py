import os
import zipfile
import tarfile

def extrair_arquivo(arquivo, diretorio_destino):
    # Extrai arquivos ZIP
    if zipfile.is_zipfile(arquivo):
        with zipfile.ZipFile(arquivo, 'r') as arquivo_zip:
            arquivo_zip.extractall(diretorio_destino)
            print(f'Extraído: {arquivo}')
    # Extrai arquivos TAR (incluindo tar.gz e tar.bz2)
    elif tarfile.is_tarfile(arquivo):
        with tarfile.open(arquivo, 'r:*') as arquivo_tar:
            arquivo_tar.extractall(diretorio_destino)
            print(f'Extraído: {arquivo}')
    else:
        print(f'Formato não suportado: {arquivo}')
        return False
    return True

def extrair_todos_arquivos(diretorio_origem):
    # Percorre todos os arquivos e pastas dentro do diretório
    for root, _, files in os.walk(diretorio_origem):
        for file in files:
            caminho_arquivo = os.path.join(root, file)
            
            # Tenta extrair o arquivo, se for compactado
            if extrair_arquivo(caminho_arquivo, root):
                # Remove o arquivo compactado original após a extração
                os.remove(caminho_arquivo)

def extrair_recursivo(diretorio_origem):
    while True:
        # Extrai todos os arquivos compactados na pasta e subpastas
        extrair_todos_arquivos(diretorio_origem)

        # Verifica se ainda existem arquivos compactados após a extração
        arquivos_compactados_restantes = False
        for root, _, files in os.walk(diretorio_origem):
            for file in files:
                caminho_arquivo = os.path.join(root, file)
                if zipfile.is_zipfile(caminho_arquivo) or tarfile.is_tarfile(caminho_arquivo):
                    arquivos_compactados_restantes = True
                    break
            if arquivos_compactados_restantes:
                break
        
        # Se não houver mais arquivos compactados, encerra o loop
        if not arquivos_compactados_restantes:
            print("Extração completa.")
            break

# Exemplo de uso
diretorio_origem = '/caminho/para/pasta/origem'
extrair_recursivo(diretorio_origem)
