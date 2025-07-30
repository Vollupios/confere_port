#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo de uso do Sistema de Consulta CNPJA
Demonstra como usar o sistema para consultar CNPJs via API
"""

from consultor_simples import ConsultorCNPJA
import time

def exemplo_consulta_individual():
    """Exemplo de consulta individual"""
    print("=== EXEMPLO: Consulta Individual ===")
    
    consultor = ConsultorCNPJA()
    
    # CNPJ de exemplo (Google Brasil)
    cnpj = "07.526.557/0001-16"
    
    print(f"Consultando CNPJ: {cnpj}")
    resultado = consultor.consultar_cnpj(cnpj)
    
    if resultado:
        # Extrai o acronym (foco principal)
        acronym = consultor.extrair_acronym(resultado)
        print(f"\n✓ Acronym encontrado: {acronym}")
        
        # Outras informações úteis
        print(f"Razão Social: {resultado.get('company', {}).get('name', 'N/A')}")
        print(f"Situação: {resultado.get('status', {}).get('text', 'N/A')}")
    else:
        print("✗ Consulta não realizada (possível rate limit)")

def exemplo_processamento_csv():
    """Exemplo de processamento de arquivo CSV"""
    print("\n=== EXEMPLO: Processamento CSV ===")
    
    consultor = ConsultorCNPJA()
    
    # Verifica se o arquivo existe
    arquivo_csv = "exemplo_cnpjs.csv"
    
    print(f"Processando arquivo: {arquivo_csv}")
    
    # Aguarda um pouco para respeitar rate limit
    print("Aguardando para respeitar rate limit...")
    time.sleep(15)  # 15 segundos de pausa
    
    resultados = consultor.processar_csv(arquivo_csv)
    
    if resultados:
        print(f"\n✓ Processamento concluído!")
        print(f"Total processado: {len(resultados)}")
        
        # Conta sucessos e acronyms
        sucessos = sum(1 for r in resultados if r['consulta_realizada'])
        acronyms = sum(1 for r in resultados if r['acronym'])
        
        print(f"Consultas realizadas: {sucessos}")
        print(f"Acronyms encontrados: {acronyms}")
        
        # Exibe os acronyms encontrados
        print("\nAcronyms encontrados:")
        for resultado in resultados:
            if resultado['acronym']:
                print(f"- CNPJ {resultado['cnpj_limpo']}: {resultado['acronym']}")
        
        # Salva os resultados
        consultor.salvar_resultados(resultados, "exemplo_resultado.csv")
        print("\n✓ Resultados salvos em 'exemplo_resultado.csv'")

def main():
    """Executa os exemplos"""
    print("SISTEMA DE CONSULTA CNPJA - EXEMPLOS")
    print("=" * 50)
    print("API: https://open.cnpja.com/office/:cnpj")
    print("Rate Limit: 5 consultas por minuto")
    print("=" * 50)
    
    try:
        # Exemplo 1: Consulta individual
        exemplo_consulta_individual()
        
        # Exemplo 2: Processamento CSV (com pausa para rate limit)
        exemplo_processamento_csv()
        
        print("\n" + "=" * 50)
        print("✓ EXEMPLOS CONCLUÍDOS!")
        print("Verifique os arquivos de resultado gerados.")
        print("=" * 50)
        
    except KeyboardInterrupt:
        print("\n\nExemplos interrompidos pelo usuário.")
    except Exception as e:
        print(f"\nErro durante os exemplos: {str(e)}")

if __name__ == "__main__":
    main()
