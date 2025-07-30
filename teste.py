#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arquivo de teste para o sistema de consulta CNPJA
"""

from consultor_simples import ConsultorCNPJA
import json

def teste_consulta_individual():
    """Testa a consulta de um CNPJ individual"""
    print("=== TESTE: Consulta Individual ===")
    
    consultor = ConsultorCNPJA()
    
    # CNPJ de teste - Google Brasil
    cnpj_teste = "07.526.557/0001-16"
    
    print(f"Testando CNPJ: {cnpj_teste}")
    resultado = consultor.consultar_cnpj(cnpj_teste)
    
    if resultado:
        print("✓ Consulta realizada com sucesso!")
        
        # Extrai o acronym
        acronym = consultor.extrair_acronym(resultado)
        print(f"Acronym encontrado: {acronym}")
        
        # Exibe algumas informações principais
        print(f"Razão Social: {resultado.get('company', {}).get('name', 'N/A')}")
        print(f"Nome Fantasia: {resultado.get('alias', 'N/A')}")
        print(f"Situação: {resultado.get('status', {}).get('text', 'N/A')}")
        
        return True
    else:
        print("✗ Falha na consulta!")
        return False

def teste_processamento_csv():
    """Testa o processamento de arquivo CSV"""
    print("\n=== TESTE: Processamento CSV ===")
    
    consultor = ConsultorCNPJA()
    
    # Verifica se existe o arquivo de exemplo
    arquivo_teste = "exemplo_cnpjs.csv"
    
    try:
        resultados = consultor.processar_csv(arquivo_teste)
        
        if resultados:
            print(f"✓ Processamento concluído: {len(resultados)} CNPJs processados")
            
            # Conta sucessos e acronyms
            sucessos = sum(1 for r in resultados if r['consulta_realizada'])
            acronyms = sum(1 for r in resultados if r['acronym'])
            
            print(f"Consultas realizadas: {sucessos}")
            print(f"Acronyms encontrados: {acronyms}")
            
            # Salva os resultados
            consultor.salvar_resultados(resultados, "teste_resultados.csv")
            
            return True
        else:
            print("✗ Nenhum resultado obtido")
            return False
            
    except Exception as e:
        print(f"✗ Erro no teste: {str(e)}")
        return False

def teste_rate_limit():
    """Testa o controle de rate limit"""
    print("\n=== TESTE: Rate Limit ===")
    
    consultor = ConsultorCNPJA()
    
    # CNPJs para testar rate limit - usando apenas 2 para teste mais rápido
    cnpjs_teste = [
        "07.526.557/0001-16",
        "11.222.333/0001-81"
    ]
    
    print(f"Testando {len(cnpjs_teste)} consultas para verificar rate limit...")
    print("NOTA: O sistema agora aplica intervalo FIXO de 15 segundos entre consultas")
    print("Isso garante que nunca exceda o limite da API (mais seguro)")
    
    import time
    inicio = time.time()
    
    for i, cnpj in enumerate(cnpjs_teste, 1):
        print(f"\nConsulta {i}/{len(cnpjs_teste)}: {cnpj}")
        tempo_consulta = time.time()
        resultado = consultor.consultar_cnpj(cnpj)
        tempo_final = time.time()
        
        duracao = tempo_final - tempo_consulta
        print(f"Tempo da consulta: {duracao:.1f}s")
        
        if i > 1:
            tempo_entre_consultas = tempo_consulta - tempo_anterior
            print(f"Intervalo desde última consulta: {tempo_entre_consultas:.1f}s")
            
        tempo_anterior = tempo_final
    
    tempo_total = time.time() - inicio
    print(f"\n✓ Rate limit testado! Tempo total: {tempo_total:.1f} segundos")
    print(f"Com intervalo fixo de 15s, cada consulta demora ~15s")

def main():
    """Executa todos os testes"""
    print("INICIANDO TESTES DO SISTEMA CNPJA")
    print("=" * 50)
    
    try:
        # Teste 1: Consulta individual
        sucesso1 = teste_consulta_individual()
        
        # Teste 2: Processamento CSV
        sucesso2 = teste_processamento_csv()
        
        # Teste 3: Rate limit (opcional - consome quota)
        print("\nDeseja testar o rate limit? (pode consumir várias consultas)")
        testar_rate = input("Digite 's' para sim: ").lower().strip() == 's'
        
        sucesso3 = True
        if testar_rate:
            teste_rate_limit()
        
        # Resumo
        print("\n" + "=" * 50)
        print("RESUMO DOS TESTES:")
        print("=" * 50)
        print(f"Consulta Individual: {'✓ SUCESSO' if sucesso1 else '✗ FALHA'}")
        print(f"Processamento CSV: {'✓ SUCESSO' if sucesso2 else '✗ FALHA'}")
        print(f"Rate Limit: {'✓ TESTADO' if testar_rate else '- NÃO TESTADO'}")
        
        if sucesso1 and sucesso2:
            print("\n✓ TODOS OS TESTES PRINCIPAIS PASSARAM!")
        else:
            print("\n✗ ALGUNS TESTES FALHARAM!")
            
    except Exception as e:
        print(f"\nErro durante os testes: {str(e)}")

if __name__ == "__main__":
    main()
