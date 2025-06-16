import os
import time
import requests

# Cores
VERMELHO = '\033[91m'
BRANCO = '\033[97m'
RESET = '\033[0m'

def banner():
    os.system("clear")
    print(VERMELHO + r"""
 ██████╗ ██╗      ██╗  ██╗ ██████╗ 
██╔═══██╗██║      ██║  ██║██╔═══██╗
██║   ██║██║█████╗███████║██║   ██║
██║   ██║██║╚════╝██╔══██║██║   ██║
╚██████╔╝███████╗ ██║  ██║╚██████╔╝
 ╚═════╝ ╚══════╝ ╚═╝  ╚═╝ ╚═════╝ 
""" + BRANCO + "       OLHO DE DEUS 2.0\n" + RESET)

def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11:
        return False
    if cpf == cpf[0] * 11:
        return False
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    dig1 = (soma * 10) % 11
    if dig1 == 10:
        dig1 = 0
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    dig2 = (soma * 10) % 11
    if dig2 == 10:
        dig2 = 0
    return dig1 == int(cpf[9]) and dig2 == int(cpf[10])

def consultar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    if not validar_cpf(cpf):
        print(VERMELHO + "CPF inválido." + RESET)
        return
    
    url = "https://encomendasdobrasil.com/api.php"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "cpf": cpf
    }
    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        response.raise_for_status()
        
        # Tente interpretar como JSON, se falhar mostra texto puro
        try:
            resultado = response.json()
            print(BRANCO + "Resultado da consulta CPF:")
            print(resultado)
        except ValueError:
            print(BRANCO + "Resposta da API:")
            print(response.text)
        
    except requests.exceptions.RequestException as e:
        print(VERMELHO + "Erro na consulta CPF:" + RESET, e)

def consultar_cnpj(cnpj):
    print(BRANCO + f"Consultando CNPJ: {cnpj}..." + RESET)
    url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if 'status' in data and data['status'] == 'ERROR':
            print(VERMELHO + "Erro: " + data.get('message', 'CNPJ inválido ou não encontrado.') + RESET)
        else:
            print(BRANCO + f"Nome: {data.get('nome')}")
            print(f"Fantasia: {data.get('fantasia')}")
            print(f"Situação: {data.get('situacao')}")
            print(f"Município: {data.get('municipio')}")
            print(f"UF: {data.get('uf')}")
            print(f"Abertura: {data.get('abertura')}")
            print(f"Natureza Jurídica: {data.get('natureza_juridica')}" + RESET)
    except Exception as e:
        print(VERMELHO + "Erro ao consultar CNPJ." + RESET)
        print(VERMELHO + str(e) + RESET)

def consultar_ip(ip):
    print(BRANCO + f"Consultando IP: {ip}..." + RESET)
    url = f"http://ip-api.com/json/{ip}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data['status'] == 'fail':
            print(VERMELHO + "IP inválido ou não encontrado." + RESET)
        else:
            print(BRANCO + f"País: {data.get('country')}")
            print(f"Região: {data.get('regionName')}")
            print(f"Cidade: {data.get('city')}")
            print(f"ISP: {data.get('isp')}")
            print(f"Organização: {data.get('org')}" + RESET)
    except Exception as e:
        print(VERMELHO + "Erro ao consultar IP." + RESET)
        print(VERMELHO + str(e) + RESET)

def menu():
    print(BRANCO + "[1] Consultar CPF")
    print("[2] Consultar CNPJ")
    print("[3] Consultar IP")
    print("[0] Sair\n" + RESET)

    escolha = input(VERMELHO + "Escolha uma opção: " + RESET)

    if escolha == "1":
        cpf = input("\nDigite o CPF (somente números): ")
        consultar_cpf(cpf)
    elif escolha == "2":
        cnpj = input("\nDigite o CNPJ (somente números): ")
        consultar_cnpj(cnpj)
    elif escolha == "3":
        ip = input("\nDigite o IP: ")
        consultar_ip(ip)
    elif escolha == "0":
        print("\nSaindo...")
        time.sleep(1)
        exit()
    else:
        print("\nOpção inválida.")

    input("\nPressione Enter para voltar ao menu...")
    main()

def main():
    banner()
    menu()

if __name__ == "__main__":
    main()
