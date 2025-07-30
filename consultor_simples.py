import requests
import pandas as pd
import time
import json
import re
from datetime import datetime
from typing import List, Dict, Optional
import csv
import os

class ConsultorCNPJA:
    """
    Classe para consultar informações de CNPJs através da Brasil API
    com controle de rate limiting (5 consultas por minuto)
    """
    
    def __init__(self):
        self.base_url = "https://brasilapi.com.br/api/cnpj/v1"
        self.rate_limit = 5  # 5 consultas por minuto
        self.consultas_realizadas = []
        
    def limpar_cnpj(self, cnpj: str) -> str:
        """Remove pontuação do CNPJ, mantendo apenas números"""
        return re.sub(r'[^0-9]', '', str(cnpj))
    
    def validar_cnpj(self, cnpj: str) -> bool:
        """Valida se o CNPJ tem 14 dígitos"""
        cnpj_limpo = self.limpar_cnpj(cnpj)
        return len(cnpj_limpo) == 14 and cnpj_limpo.isdigit()
    
    def controlar_rate_limit(self):
        """Controla o limite de 5 consultas por minuto com intervalo fixo de 15 segundos"""
        # Intervalo fixo de 15 segundos entre consultas (mais conservador que 12s)
        intervalo_fixo = 15  # 15 segundos entre cada consulta
        
        if self.consultas_realizadas:
            ultima_consulta = self.consultas_realizadas[-1]
            tempo_desde_ultima = time.time() - ultima_consulta
            
            if tempo_desde_ultima < intervalo_fixo:
                tempo_espera = intervalo_fixo - tempo_desde_ultima
                print(f"Aguardando intervalo obrigatório de 15s entre consultas. Restam {tempo_espera:.1f} segundos...")
                time.sleep(tempo_espera)
        
        # Remove consultas antigas (mais de 1 minuto) para manter histórico limpo
        agora = time.time()
        self.consultas_realizadas = [
            timestamp for timestamp in self.consultas_realizadas 
            if agora - timestamp < 60
        ]
    
    def consultar_cnpj(self, cnpj: str) -> Optional[Dict]:
        """
        Consulta um CNPJ específico na Brasil API
        Retorna o objeto JSON completo ou None em caso de erro
        """
        cnpj_limpo = self.limpar_cnpj(cnpj)
        
        if not self.validar_cnpj(cnpj_limpo):
            print(f"⚠ CNPJ inválido (não possui 14 dígitos), pulando: {cnpj} -> {cnpj_limpo}")
            return None
        
        # Controla o rate limit
        self.controlar_rate_limit()
        
        try:
            url = f"{self.base_url}/{cnpj_limpo}"
            print(f"Consultando CNPJ: {cnpj_limpo}")
            
            response = requests.get(url, timeout=30)
            self.consultas_realizadas.append(time.time())
            
            if response.status_code == 200:
                dados = response.json()
                print(f"✓ Consulta realizada com sucesso para CNPJ: {cnpj_limpo}")
                return dados
            elif response.status_code == 404:
                print(f"✗ CNPJ não encontrado: {cnpj_limpo}")
                return None
            else:
                print(f"✗ Erro na consulta do CNPJ {cnpj_limpo}: Status {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            print(f"✗ Timeout na consulta do CNPJ: {cnpj_limpo}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"✗ Erro de conexão para CNPJ {cnpj_limpo}: {str(e)}")
            return None
        except json.JSONDecodeError:
            print(f"✗ Erro ao decodificar JSON para CNPJ: {cnpj_limpo}")
            return None
    
    def extrair_acronym(self, dados_cnpj: Dict) -> Optional[str]:
        """
        Extrai o campo 'porte' dos dados do CNPJ da Brasil API
        Na Brasil API, o porte está diretamente em 'porte' (ex: "DEMAIS", "ME", "EPP", etc.)
        """
        try:
            # Na Brasil API, o porte está diretamente no campo 'porte'
            porte = dados_cnpj.get('porte')
            return porte
        except (KeyError, AttributeError, TypeError):
            return None
    
    def processar_arquivo(self, arquivo: str, coluna_cnpj: str = 'cnpj') -> List[Dict]:
        """
        Processa um arquivo CSV ou TXT com CNPJs e consulta cada um
        Retorna uma lista com os resultados
        """
        if not os.path.exists(arquivo):
            print(f"Arquivo não encontrado: {arquivo}")
            return []
        
        resultados = []
        
        try:
            # Verifica a extensão do arquivo
            _, extensao = os.path.splitext(arquivo.lower())
            
            if extensao == '.csv':
                # Lê o CSV preservando zeros à esquerda como string
                df = pd.read_csv(arquivo, dtype={coluna_cnpj: str})
                
                if coluna_cnpj not in df.columns:
                    print(f"Coluna '{coluna_cnpj}' não encontrada no CSV")
                    print(f"Colunas disponíveis: {list(df.columns)}")
                    return []
                
                cnpjs = df[coluna_cnpj].tolist()
                
            elif extensao == '.txt':
                # Lê o TXT linha por linha
                with open(arquivo, 'r', encoding='utf-8') as f:
                    cnpjs = [linha.strip() for linha in f.readlines() if linha.strip()]
                
            else:
                print(f"Formato de arquivo não suportado: {extensao}")
                print("Formatos suportados: .csv, .txt")
                return []
            
            total_cnpjs = len(cnpjs)
            
            print(f"Processando {total_cnpjs} CNPJs do arquivo {arquivo}")
            print("=" * 50)
            
            cnpjs_validos = 0
            cnpjs_invalidos = 0
            
            for i, cnpj in enumerate(cnpjs, 1):
                try:
                    print(f"\nProcessando {i}/{total_cnpjs}")
                    
                    # Verifica se CNPJ é válido antes de consultar
                    # Converte para string e preserva zeros à esquerda
                    cnpj_str = str(cnpj).strip()
                    cnpj_limpo = self.limpar_cnpj(cnpj_str)
                    
                    # Garante que o CNPJ limpo tenha zeros à esquerda se necessário
                    if cnpj_limpo.isdigit() and len(cnpj_limpo) < 14:
                        cnpj_limpo = cnpj_limpo.zfill(14)
                    
                    if not self.validar_cnpj(cnpj_limpo):
                        print(f"⚠ CNPJ inválido (não possui 14 dígitos), pulando: {cnpj_str} -> {cnpj_limpo}")
                        cnpjs_invalidos += 1
                        resultado = {
                            'cnpj_original': cnpj_str,
                            'cnpj_limpo': cnpj_limpo,
                            'consulta_realizada': False,
                            'acronym': None,
                            'dados_completos': None,
                            'motivo_falha': 'CNPJ inválido - não possui 14 dígitos'
                        }
                    else:
                        cnpjs_validos += 1
                        # Consulta o CNPJ
                        dados = self.consultar_cnpj(cnpj_limpo)
                        
                        resultado = {
                            'cnpj_original': cnpj_str,
                            'cnpj_limpo': cnpj_limpo,
                            'consulta_realizada': dados is not None,
                            'acronym': self.extrair_acronym(dados) if dados else None,
                            'dados_completos': dados,
                            'motivo_falha': None if dados else 'Erro na API ou rate limit'
                        }
                    
                    resultados.append(resultado)
                    
                except KeyboardInterrupt:
                    print(f"\n⚠ Processamento interrompido pelo usuário no CNPJ {i}")
                    print(f"Salvando resultados parciais...")
                    break
                except Exception as e:
                    print(f"✗ Erro inesperado ao processar CNPJ {i} ({cnpj}): {str(e)}")
                    # Adiciona um resultado de erro para não perder o registro
                    cnpj_str = str(cnpj).strip() if 'cnpj' in locals() else 'N/A'
                    resultado = {
                        'cnpj_original': cnpj_str,
                        'cnpj_limpo': self.limpar_cnpj(cnpj_str).zfill(14) if cnpj_str != 'N/A' else '',
                        'consulta_realizada': False,
                        'acronym': None,
                        'dados_completos': None,
                        'motivo_falha': f'Erro inesperado: {str(e)}'
                    }
                    resultados.append(resultado)
                    # Continua o processamento mesmo com erro
            
            print(f"\n" + "=" * 50)
            print(f"Processamento concluído: {len(resultados)} CNPJs processados")
            print(f"CNPJs válidos: {cnpjs_validos}")
            print(f"CNPJs inválidos (pulados): {cnpjs_invalidos}")
            
            # Verifica se processou todos os CNPJs
            if len(resultados) < total_cnpjs:
                cnpjs_nao_processados = total_cnpjs - len(resultados)
                print(f"⚠ Aviso: {cnpjs_nao_processados} CNPJs não foram processados devido a erros")
            
        except KeyboardInterrupt:
            print(f"\n⚠ Processamento interrompido pelo usuário")
            print(f"CNPJs processados até o momento: {len(resultados)}")
        except Exception as e:
            print(f"Erro crítico ao processar CSV: {str(e)}")
            print(f"CNPJs processados antes do erro: {len(resultados)}")
            # Não retorna vazio mesmo com erro - retorna o que foi processado até então
        
        return resultados
    
    def processar_csv(self, arquivo_csv: str, coluna_cnpj: str = 'cnpj') -> List[Dict]:
        """
        Método de compatibilidade para processar CSV
        Redireciona para processar_arquivo()
        """
        return self.processar_arquivo(arquivo_csv, coluna_cnpj)
    
    def processar_txt(self, arquivo_txt: str) -> List[Dict]:
        """
        Método específico para processar arquivos TXT
        Redireciona para processar_arquivo()
        """
        return self.processar_arquivo(arquivo_txt)
    
    def salvar_resultados(self, resultados: List[Dict], arquivo_saida: Optional[str] = None):
        """
        Salva os resultados em um arquivo CSV
        """
        if not resultados:
            print("Nenhum resultado para salvar")
            return
        
        if arquivo_saida is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            arquivo_saida = f"resultados_cnpj_{timestamp}.csv"
        
        # Prepara os dados para o CSV
        dados_csv = []
        for resultado in resultados:
            linha = {
                'cnpj_original': resultado['cnpj_original'],
                'cnpj_limpo': resultado['cnpj_limpo'],
                'consulta_realizada': resultado['consulta_realizada'],
                'acronym': resultado['acronym'] or '',
                'motivo_falha': resultado.get('motivo_falha', '') or ''
            }
            
            # Adiciona alguns campos principais dos dados completos se disponíveis
            if resultado['dados_completos']:
                dados = resultado['dados_completos']
                
                linha.update({
                    'razao_social': dados.get('razao_social', ''),
                    'nome_fantasia': dados.get('nome_fantasia', ''),
                    'situacao': dados.get('descricao_situacao_cadastral', ''),
                    'porte': dados.get('porte', ''),  # DEMAIS, ME, EPP, etc.
                    'codigo_porte': dados.get('codigo_porte', ''),
                    'natureza_juridica': dados.get('natureza_juridica', ''),
                    'cnae_fiscal': dados.get('cnae_fiscal', ''),
                    'cnae_fiscal_descricao': dados.get('cnae_fiscal_descricao', ''),
                    'telefone': dados.get('ddd_telefone_1', ''),
                    'telefone_2': dados.get('ddd_telefone_2', ''),
                    'email': dados.get('email', ''),
                    'cep': dados.get('cep', ''),
                    'municipio': dados.get('municipio', ''),
                    'uf': dados.get('uf', ''),
                    'logradouro': dados.get('logradouro', ''),
                    'numero': dados.get('numero', ''),
                    'bairro': dados.get('bairro', ''),
                    'complemento': dados.get('complemento', ''),
                    'capital_social': dados.get('capital_social', ''),
                    'data_inicio_atividade': dados.get('data_inicio_atividade', ''),
                    'data_situacao_cadastral': dados.get('data_situacao_cadastral', ''),
                })
            
            dados_csv.append(linha)
        
        # Salva no CSV
        try:
            df_resultado = pd.DataFrame(dados_csv)
            df_resultado.to_csv(arquivo_saida, index=False, encoding='utf-8-sig')
            print(f"\nResultados salvos em: {arquivo_saida}")
            print(f"Total de registros: {len(dados_csv)}")
            
            # Estatísticas
            consultas_realizadas = sum(1 for r in resultados if r['consulta_realizada'])
            acronyms_encontrados = sum(1 for r in resultados if r['acronym'])
            
            print(f"Consultas realizadas com sucesso: {consultas_realizadas}")
            print(f"Acronyms encontrados: {acronyms_encontrados}")
            
        except Exception as e:
            print(f"Erro ao salvar resultados: {str(e)}")

def exemplo_uso():
    """Exemplo de uso da classe ConsultorCNPJA"""
    consultor = ConsultorCNPJA()
    
    # Exemplo 1: Consulta de um CNPJ específico
    print("=== EXEMPLO 1: Consulta individual ===")
    cnpj_exemplo = "19.131.243/0001-97"  # CNPJ de exemplo para Brasil API
    resultado = consultor.consultar_cnpj(cnpj_exemplo)
    
    if resultado:
        porte = consultor.extrair_acronym(resultado)
        print(f"Porte encontrado: {porte}")
        print(f"Razão Social: {resultado.get('razao_social', 'N/A')}")
    else:
        print("Consulta não retornou dados")
    
    # Exemplo 2: Processamento via CSV
    print("\n=== EXEMPLO 2: Processamento via CSV ===")
    arquivo_csv = "exemplo_cnpjs.csv"
    
    if os.path.exists(arquivo_csv):
        resultados = consultor.processar_csv(arquivo_csv)
        consultor.salvar_resultados(resultados)
    else:
        print(f"Arquivo {arquivo_csv} não encontrado")
    
    # Exemplo 3: Processamento via TXT
    print("\n=== EXEMPLO 3: Processamento via TXT ===")
    arquivo_txt = "exemplo_cnpjs.txt"
    
    if os.path.exists(arquivo_txt):
        resultados = consultor.processar_txt(arquivo_txt)
        consultor.salvar_resultados(resultados, "resultados_txt.csv")
    else:
        print(f"Arquivo {arquivo_txt} não encontrado")

if __name__ == "__main__":
    exemplo_uso()
