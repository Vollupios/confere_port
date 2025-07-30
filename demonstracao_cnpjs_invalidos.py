#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demonstração do comportamento com CNPJs inválidos
Mostra como o sistema pula CNPJs que não têm 14 dígitos
"""

from consultor_simples import ConsultorCNPJA
import pandas as pd

def demonstrar_comportamento():
    """Demonstra como CNPJs inválidos são tratados"""
    print("=== DEMONSTRAÇÃO: Tratamento de CNPJs Inválidos ===")
    print("O sistema agora PULA automaticamente CNPJs que não têm 14 dígitos")
    print("=" * 60)
    
    consultor = ConsultorCNPJA()
    
    # Criar um arquivo de exemplo com CNPJs mistos
    dados_exemplo = {
        'cnpj': [
            '07526557000116',    # 14 dígitos - VÁLIDO
            '123456789',         # 9 dígitos - INVÁLIDO (será pulado)
            '11222333000181',    # 14 dígitos - VÁLIDO
            '12345',             # 5 dígitos - INVÁLIDO (será pulado)
            '33000167000101',    # 14 dígitos - VÁLIDO
            '123456789012345',   # 15 dígitos - INVÁLIDO (será pulado)
        ]
    }
    
    # Salva arquivo de teste
    df = pd.DataFrame(dados_exemplo)
    arquivo_teste = 'demonstracao_cnpjs.csv'
    df.to_csv(arquivo_teste, index=False)
    
    print(f"Arquivo criado: {arquivo_teste}")
    print("Conteúdo:")
    print(df.to_string(index=False))
    
    print(f"\n" + "=" * 60)
    print("PROCESSANDO ARQUIVO COM CNPJs MISTOS:")
    print("=" * 60)
    
    # Processa o arquivo
    resultados = consultor.processar_csv(arquivo_teste)
    
    # Salva resultados
    arquivo_resultado = 'resultado_demonstracao.csv'
    consultor.salvar_resultados(resultados, arquivo_resultado)
    
    print(f"\n" + "=" * 60)
    print("RESUMO DO COMPORTAMENTO:")
    print("=" * 60)
    print("✅ CNPJs válidos (14 dígitos): Consultados na API")
    print("⚠️ CNPJs inválidos (≠14 dígitos): Pulados automaticamente")
    print("📄 Todos registrados no CSV final com motivo da falha")
    print("🔄 Processamento continua sem interrupção")
    
    # Mostra estatísticas finais
    if resultados:
        total = len(resultados)
        validos = sum(1 for r in resultados if r['consulta_realizada'])
        invalidos = sum(1 for r in resultados if r.get('motivo_falha') == 'CNPJ inválido - não possui 14 dígitos')
        
        print(f"\nESTATÍSTICAS:")
        print(f"Total de CNPJs: {total}")
        print(f"CNPJs válidos processados: {validos}")
        print(f"CNPJs inválidos pulados: {invalidos}")
        print(f"Arquivo resultado: {arquivo_resultado}")

if __name__ == "__main__":
    demonstrar_comportamento()
