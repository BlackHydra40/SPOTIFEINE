import os
import requests
import time
import json
from tkinter import Tk, filedialog

banner = """
\033[32m
 __             _   _  __      _            
/ _\\_ __   ___ | |_(_)/ _| ___(_)_ __   ___ 
\\ \\| '_ \\ / _ \\| __| | |_ / _ \\ | '_ \\ / _ \\
_\\ \\ |_) | (_) | |_| |  _|  __/ | | | |  __/
\\__/ .__/ \\___/ \\__|_|_|  \\___|_|_| |_|\\___|
   |_|  

BY: @MS40GG   
\033[0m
"""
print(banner)



def parse_cookies(file_path):
    """
    Processa cookies em formato específico para extrair apenas chaves e valores.
    """
    cookies = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                # Ignorar linhas de comentário ou vazias
                if line.startswith("#") or not line.strip():
                    continue

                # Dividir a linha por tabulação ou espaços
                parts = line.strip().split("\t")

                # Verificar se a linha tem pelo menos 7 campos (padrão esperado)
                if len(parts) >= 7:
                    cookie = {
                        "domain": parts[0],  # Domínio
                        "path": parts[2],    # Caminho
                        "name": parts[5],    # Nome do cookie
                        "value": parts[6],   # Valor do cookie
                    }
                    cookies.append(cookie)
    except Exception as e:
        print(f"Erro ao processar cookies do arquivo {file_path}: {e}")
    return cookies

def convert_to_requests_cookies(cookies):
    """
    Converte os cookies extraídos para o formato que o requests espera (dicionário de chave-valor).
    """
    req_cookies = {}
    for cookie in cookies:
        req_cookies[cookie['name']] = cookie['value']
    return req_cookies

def test_cookie(cookies, folder_path):
    """
    Testa cookies realizando uma requisição para a URL.
    """
    url = "https://www.spotify.com/eg-ar/api/account/v1/datalayer/"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0",
        "Referer": "https://www.spotify.com/",
        "Origin": "https://www.spotify.com",
    }

    # Converter cookies para o formato esperado pelo requests
    req_cookies = convert_to_requests_cookies(cookies)
    
    print("Cookies usados na requisição:", req_cookies)  # Log para verificar os cookies

    try:
        response = requests.get(url, headers=headers, cookies=req_cookies)
        if response.status_code == 200:
            data = response.json()
            current_plan = data.get("currentPlan", "Desconhecido")
            account_age = data.get("accountAgeDays", "N/A")
            country = data.get("country", "N/A")
            
            # Exibir informações
            print(f"Cookies válidos!")
            print(f"Plano atual: {current_plan}")
            print(f"Idade da conta: {account_age} dias")
            print(f"País: {country}")
            
            # Definindo o caminho do arquivo para salvar os cookies válidos (pasta do script)
            valid_cookies_file = os.path.join(os.getcwd(), "cookies_validos.json")
            
            # Salvar cookies válidos em JSON com separação e plano/país
            with open(valid_cookies_file, "a") as file:
                # Adiciona a separação visual
                file.write("\n===============\n")
                
                # Adiciona o plano e o país abaixo da linha de separação
                file.write(f"Plano da conta: {current_plan}\n")
                file.write(f"País: {country}\n")
                
                # Salva os cookies válidos em formato JSON
                json.dump(cookies, file, ensure_ascii=False, indent=4)
                file.write("\n")  # Separar cookies válidos por nova linha
        elif response.status_code == 401:
            print("Cookies inválidos: Não autorizado (401). Verifique a validade ou o domínio.")
        else:
            print(f"Erro desconhecido: Status Code {response.status_code}")
    except Exception as e:
        print(f"Erro ao testar cookies: {e}")

def main():
    # Abre a janela para selecionar a pasta
    Tk().withdraw()  # Oculta a janela principal do tkinter
    folder_path = filedialog.askdirectory(title="Selecione a pasta com os arquivos .txt")

    if not folder_path:
        print("Nenhuma pasta selecionada.")
        return

    # Lista todos os arquivos .txt na pasta
    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

    if not txt_files:
        print("Nenhum arquivo .txt encontrado na pasta.")
        return
    
    # Testa os cookies de cada arquivo
    for txt_file in txt_files:
        file_path = os.path.join(folder_path, txt_file)
        print(f"\nTestando cookies do arquivo: {txt_file}")
        cookies = parse_cookies(file_path)
        if cookies:
            test_cookie(cookies, folder_path)  # O arquivo valid_cookies.json é salvo automaticamente
        else:
            print("Nenhum cookie encontrado no arquivo.")
        
        # Delay de 2 segundos entre requisições
        time.sleep(2)

if __name__ == "__main__":
    main()
