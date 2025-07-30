#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Consulta CNPJA - Interface Principal
Consulta automatizada de CNPJs através da API CNPJA
Limitado a 5 consultas por minuto conforme especificação da API
"""

import os
import sys
from consultor_simples import ConsultorCNPJA

def menu_principal():
    """Exibe o menu principal do sistema"""
    print("\n" + "="*60)
    print("       SISTEMA DE CONSULTA CNPJ - Brasil API")
    print("="*60)
    print("1. Consultar CNPJ individual")
    print("2. Processar arquivo CSV com múltiplos CNPJs")
    print("3. Processar arquivo TXT com múltiplos CNPJs")
    print("4. Criar arquivo CSV de exemplo")
    print("5. Criar arquivo TXT de exemplo")
    print("6. Sair")
    print("="*60)

def consultar_cnpj_individual():
    """Função para consultar um CNPJ específico"""
    consultor = ConsultorCNPJA()
    
    print("\n--- CONSULTA INDIVIDUAL ---")
    cnpj = input("Digite o CNPJ (com ou sem formatação): ").strip()
    
    if not cnpj:
        print("CNPJ não pode estar vazio!")
        return
    
    print(f"\nIniciando consulta para CNPJ: {cnpj}")
    print("-" * 40)
    
    resultado = consultor.consultar_cnpj(cnpj)
    
    if resultado:
        print("\n✓ CONSULTA REALIZADA COM SUCESSO!")
        print("-" * 40)
        
        # Exibe informações principais
        porte = consultor.extrair_acronym(resultado)
        print(f"Porte: {porte or 'Não informado'}")
        
        # Outras informações úteis  
        print(f"Razão Social: {resultado.get('razao_social', 'Não informado')}")
        print(f"Nome Fantasia: {resultado.get('nome_fantasia', 'Não informado')}")
        print(f"Situação: {resultado.get('descricao_situacao_cadastral', 'Não informado')}")
        print(f"Município: {resultado.get('municipio', 'Não informado')}")
        print(f"UF: {resultado.get('uf', 'Não informado')}")
        print(f"Nome Fantasia: {resultado.get('alias', 'Não informado')}")
        
        status = resultado.get('status', {})
        print(f"Situação: {status.get('text', 'Não informado')}")
        
        # Pergunta se quer salvar os dados completos
        salvar = input("\nDeseja salvar os dados completos em CSV? (s/n): ").lower().strip()
        if salvar in ['s', 'sim', 'y', 'yes']:
            consultor.salvar_resultados([{
                'cnpj_original': cnpj,
                'cnpj_limpo': consultor.limpar_cnpj(cnpj),
                'consulta_realizada': True,
                'acronym': porte,
                'dados_completos': resultado
            }])
    else:
        print("\n✗ Falha na consulta!")

def processar_csv():
    """Função para processar arquivo CSV com múltiplos CNPJs"""
    consultor = ConsultorCNPJA()
    
    print("\n--- PROCESSAMENTO DE ARQUIVO CSV ---")
    
    # Lista arquivos CSV disponíveis
    arquivos_csv = [f for f in os.listdir('.') if f.endswith('.csv')]
    
    if arquivos_csv:
        print("\nArquivos CSV encontrados:")
        for i, arquivo in enumerate(arquivos_csv, 1):
            print(f"{i}. {arquivo}")
        
        try:
            escolha = int(input(f"\nEscolha um arquivo (1-{len(arquivos_csv)}) ou 0 para digitar o nome: "))
            
            if escolha == 0:
                arquivo_csv = input("Digite o nome do arquivo CSV: ").strip()
            elif 1 <= escolha <= len(arquivos_csv):
                arquivo_csv = arquivos_csv[escolha - 1]
            else:
                print("Opção inválida!")
                return
                
        except ValueError:
            print("Entrada inválida!")
            return
    else:
        arquivo_csv = input("Digite o nome do arquivo CSV: ").strip()
    
    if not arquivo_csv:
        print("Nome do arquivo não pode estar vazio!")
        return
    
    # Pergunta sobre a coluna do CNPJ
    coluna_cnpj = input("Nome da coluna com os CNPJs (padrão: 'cnpj'): ").strip()
    if not coluna_cnpj:
        coluna_cnpj = 'cnpj'
    
    print(f"\nIniciando processamento do arquivo: {arquivo_csv}")
    print(f"Coluna de CNPJs: {coluna_cnpj}")
    print("-" * 50)
    
    resultados = consultor.processar_csv(arquivo_csv, coluna_cnpj)
    
    if resultados:
        consultor.salvar_resultados(resultados)
        
        # Resume dos resultados
        print("\n" + "="*50)
        print("RESUMO DOS RESULTADOS:")
        print("="*50)
        
        total = len(resultados)
        sucesso = sum(1 for r in resultados if r['consulta_realizada'])
        acronyms = sum(1 for r in resultados if r['acronym'])
        
        print(f"Total de CNPJs processados: {total}")
        print(f"Consultas realizadas com sucesso: {sucesso}")
        print(f"Portes encontrados: {acronyms}")
        print(f"Taxa de sucesso: {(sucesso/total)*100:.1f}%")

def processar_txt():
    """Função para processar arquivo TXT com múltiplos CNPJs"""
    consultor = ConsultorCNPJA()
    
    print("\n--- PROCESSAMENTO DE ARQUIVO TXT ---")
    
    # Lista arquivos TXT disponíveis
    arquivos_txt = [f for f in os.listdir('.') if f.endswith('.txt')]
    
    if arquivos_txt:
        print("\nArquivos TXT encontrados:")
        for i, arquivo in enumerate(arquivos_txt, 1):
            print(f"{i}. {arquivo}")
        
        try:
            escolha = int(input(f"\nEscolha um arquivo (1-{len(arquivos_txt)}) ou 0 para digitar o nome: "))
            
            if escolha == 0:
                arquivo_txt = input("Digite o nome do arquivo TXT: ").strip()
            elif 1 <= escolha <= len(arquivos_txt):
                arquivo_txt = arquivos_txt[escolha - 1]
            else:
                print("Opção inválida!")
                return
                
        except ValueError:
            print("Entrada inválida!")
            return
    else:
        arquivo_txt = input("Digite o nome do arquivo TXT: ").strip()
    
    if not arquivo_txt:
        print("Nome do arquivo não pode estar vazio!")
        return
    
    print(f"\nIniciando processamento do arquivo: {arquivo_txt}")
    print("-" * 50)
    
    resultados = consultor.processar_txt(arquivo_txt)
    
    if resultados:
        # Cria nome do arquivo de saída baseado no TXT
        nome_base = os.path.splitext(arquivo_txt)[0]
        arquivo_saida = f"resultados_{nome_base}.csv"
        consultor.salvar_resultados(resultados, arquivo_saida)
        
        # Resume dos resultados
        print("\n" + "="*50)
        print("RESUMO DOS RESULTADOS:")
        print("="*50)
        
        total = len(resultados)
        sucesso = sum(1 for r in resultados if r['consulta_realizada'])
        portes = sum(1 for r in resultados if r['acronym'])
        
        print(f"Total de CNPJs processados: {total}")
        print(f"Consultas realizadas com sucesso: {sucesso}")
        print(f"Portes encontrados: {portes}")
        print(f"Taxa de sucesso: {(sucesso/total)*100:.1f}%")

def criar_csv_exemplo():
    """Cria um arquivo CSV de exemplo"""
    print("\n--- CRIAR ARQUIVO CSV DE EXEMPLO ---")
    
    nome_arquivo = input("Nome do arquivo (sem extensão, padrão: 'exemplo_cnpjs'): ").strip()
    if not nome_arquivo:
        nome_arquivo = 'exemplo_cnpjs'
    
    if not nome_arquivo.endswith('.csv'):
        nome_arquivo += '.csv'
    
    cnpjs_exemplo = [
        "07.526.557/0001-16",  # Google Brasil
        "11.222.333/0001-81",  # Exemplo
        "33.000.167/0001-01",  # Exemplo  
        "08.775.724/0001-12",  # Exemplo
        "34.238.864/0001-17"   # Exemplo
    ]
    
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write("cnpj\n")
            for cnpj in cnpjs_exemplo:
                f.write(f"{cnpj}\n")
        
        print(f"\n✓ Arquivo '{nome_arquivo}' criado com sucesso!")
        print(f"Contém {len(cnpjs_exemplo)} CNPJs de exemplo")
        
    except Exception as e:
        print(f"\n✗ Erro ao criar arquivo: {str(e)}")

def criar_txt_exemplo():
    """Cria um arquivo TXT de exemplo"""
    print("\n--- CRIAR ARQUIVO TXT DE EXEMPLO ---")
    
    nome_arquivo = input("Nome do arquivo TXT (padrão: exemplo_cnpjs.txt): ").strip()
    if not nome_arquivo:
        nome_arquivo = "exemplo_cnpjs.txt"
    
    if not nome_arquivo.endswith('.txt'):
        nome_arquivo += '.txt'
    
    # CNPJs de exemplo com zeros à esquerda para demonstrar preservação
    cnpjs_exemplo = [
        "19131243000197",  # Open Knowledge Brasil
        "07526557000116",  # CNPJ com zero à esquerda
        "03878957000123",  # CNPJ com zero à esquerda
        "11222333000181",  # Exemplo
        "33000167000101",  # Exemplo
        "08775724000112",  # CNPJ com zero à esquerda
        "34238864000117"   # Exemplo
    ]
    
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            for cnpj in cnpjs_exemplo:
                f.write(f"{cnpj}\n")
        
        print(f"\n✓ Arquivo '{nome_arquivo}' criado com sucesso!")
        print(f"Contém {len(cnpjs_exemplo)} CNPJs de exemplo")
        print("⚠️  Inclui CNPJs com zeros à esquerda para demonstrar preservação")
        
    except Exception as e:
        print(f"\n✗ Erro ao criar arquivo: {str(e)}")

def main():
    """Função principal do sistema"""
    while True:
        try:
            menu_principal()
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == '1':
                consultar_cnpj_individual()
            elif opcao == '2':
                processar_csv()
            elif opcao == '3':
                processar_txt()
            elif opcao == '4':
                criar_csv_exemplo()
            elif opcao == '5':
                criar_txt_exemplo()
            elif opcao == '6':
                print("\nSaindo do sistema...")
                break
            else:
                print("\nOpção inválida! Tente novamente.")
            
            # Pausa antes de voltar ao menu
            input("\nPressione Enter para continuar...")
            
        except KeyboardInterrupt:
            print("\n\nSistema interrompido pelo usuário.")
            break
        except Exception as e:
            print(f"\nErro inesperado: {str(e)}")
            input("Pressione Enter para continuar...")

if __name__ == "__main__":
    print("Iniciando Sistema de Consulta CNPJ - Brasil API...")
    main()
