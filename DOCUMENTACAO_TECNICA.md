# Documentação Técnica - Sistema de Consulta CNPJA

## Visão Geral
Sistema desenvolvido para automatizar consultas à API CNPJA (https://open.cnpja.com/office/:cnpj) com controle de rate limiting e processamento em lote via CSV.

## Arquitetura

### Classe Principal: `ConsultorCNPJA`

#### Atributos:
- `base_url`: URL base da API CNPJA
- `rate_limit`: Limite de consultas por minuto (5)
- `consultas_realizadas`: Lista de timestamps das consultas para controle de rate limit

#### Métodos Principais:

##### `consultar_cnpj(cnpj: str) -> Optional[Dict]`
- **Descrição**: Consulta um CNPJ específico na API
- **Parâmetros**: 
  - `cnpj`: String com CNPJ (formatado ou não)
- **Retorno**: Dicionário com dados JSON da API ou None em caso de erro
- **Rate Limit**: Controlado automaticamente
- **Tratamento de Erros**: Status HTTP, timeout, JSON decode

##### `processar_csv(arquivo_csv: str, coluna_cnpj: str) -> List[Dict]`
- **Descrição**: Processa arquivo CSV com múltiplos CNPJs
- **Parâmetros**: 
  - `arquivo_csv`: Caminho para o arquivo CSV
  - `coluna_cnpj`: Nome da coluna contendo os CNPJs (padrão: 'cnpj')
- **Retorno**: Lista de dicionários com resultados
- **Rate Limit**: Aplicado entre cada consulta

##### `extrair_acronym(dados_cnpj: Dict) -> Optional[str]`
- **Descrição**: Extrai especificamente o campo 'acronym' dos dados
- **Localização**: Campo encontrado em `company.size.acronym`
- **Parâmetros**: 
  - `dados_cnpj`: Dicionário com dados completos da API
- **Retorno**: String com acronym (ex: "ME", "EPP", "DEMAIS") ou None se não encontrado
- **Valores Comuns**: 
  - "ME": Microempresa
  - "EPP": Empresa de Pequeno Porte  
  - "DEMAIS": Empresas de médio/grande porte

##### `salvar_resultados(resultados: List[Dict], arquivo_saida: str)`
- **Descrição**: Salva resultados em arquivo CSV
- **Formato**: CSV com timestamp automático se nome não especificado
- **Campos**: CNPJ, acronym, dados principais da empresa

## API Utilizada

### Endpoint
```
GET https://open.cnpja.com/office/:cnpj
```

### Exemplo de Requisição
```bash
curl --request GET --url 'https://open.cnpja.com/office/07526557011659'
```

### Rate Limiting
- **Limite**: 5 consultas por minuto (máximo)
- **Implementação**: 
  - Intervalo fixo de 15 segundos entre cada consulta
  - Aguarda obrigatoriamente 15s após cada requisição
  - Mais conservador que o mínimo teórico de 12s
- **Comportamento**: 
  - Pausa fixa de 15 segundos entre todas as consultas
  - Garante que nunca exceda o limite da API
  - Mais previsível e seguro para grandes volumes

### Status Codes Tratados
- `200`: Sucesso
- `404`: CNPJ não encontrado
- `429`: Rate limit excedido
- `Outros`: Erro genérico

## Estrutura de Dados

### Objeto de Resultado
```python
{
    'cnpj_original': str,        # CNPJ como fornecido
    'cnpj_limpo': str,           # CNPJ apenas números
    'consulta_realizada': bool,  # Se consulta foi realizada
    'acronym': str|None,         # Campo acronym extraído
    'dados_completos': dict|None, # Dados completos da API
    'motivo_falha': str|None     # Motivo da falha se aplicável
}
```

### Campos do CSV de Saída
- `cnpj_original`, `cnpj_limpo`, `consulta_realizada`, `acronym`, `motivo_falha`
- `razao_social`, `nome_fantasia`, `situacao`, `porte_acronym`, `porte_text`
- `natureza_juridica`, `atividade_principal`
- `telefone`, `email`, `cep`, `municipio`, `uf`

## Validações

### CNPJ
- **Formato**: Remove pontuação automaticamente
- **Validação**: Verifica se tem 14 dígitos numéricos
- **Tratamento**: CNPJs inválidos são automaticamente pulados (não interrompem o processamento)
- **Comportamento**: CNPJs com menos ou mais de 14 dígitos são registrados como inválidos mas o processamento continua

### Arquivo CSV
- **Verificações**: Existência do arquivo, presença da coluna especificada
- **Encoding**: UTF-8 com BOM para compatibilidade com Excel

## Tratamento de Erros

### Níveis de Erro
1. **Validação**: CNPJ inválido, arquivo não encontrado
2. **Rede**: Timeout, erro de conexão
3. **API**: Status HTTP não-200, JSON inválido
4. **Sistema**: Erro de I/O, exceções gerais

### Estratégias
- **Graceful Degradation**: Continua processamento mesmo com falhas individuais
- **Logging**: Mensagens informativas sobre progresso e erros
- **Retry**: Não implementado (respeitando rate limit)

## Performance

### Considerações
- **Sequencial**: Processamento um CNPJ por vez (respeitando rate limit)
- **Tempo**: 15 segundos fixos entre cada consulta
- **Capacidade**: Máximo 4 consultas por minuto (240 consultas por hora)
- **Previsibilidade**: Tempo total = (número de CNPJs × 15 segundos)
- **Memória**: Baixo uso, dados processados incrementalmente

### Otimizações Implementadas
- Cache de timestamps para rate limit eficiente
- Processamento incremental do CSV
- Validação prévia antes de consultas

## Configurações

### Timeouts
- **Requisição HTTP**: 30 segundos
- **Rate Limit**: Calculado dinamicamente baseado em consultas anteriores

### Dependências
```python
requests>=2.28.0    # Requisições HTTP
pandas>=1.5.0       # Manipulação CSV
urllib3>=1.26.0     # Gerenciamento de conexões
```

## Exemplos de Uso Avançado

### Consulta com Retry Manual
```python
consultor = ConsultorCNPJA()
cnpj = "07526557000116"

# Primeira tentativa
resultado = consultor.consultar_cnpj(cnpj)
if not resultado:
    print("Aguardando rate limit...")
    time.sleep(60)  # Aguarda 1 minuto
    resultado = consultor.consultar_cnpj(cnpj)
```

### Processamento com Callback
```python
def callback_progresso(atual, total, cnpj, resultado):
    acronym = consultor.extrair_acronym(resultado) if resultado else "N/A"
    print(f"[{atual}/{total}] {cnpj} -> Acronym: {acronym}")

# Implementaria callback no método processar_csv
```

### Filtros Personalizados
```python
# Filtrar apenas CNPJs ativos
resultados_ativos = [
    r for r in resultados 
    if r['dados_completos'] and 
       r['dados_completos'].get('status', {}).get('text') == 'Ativa'
]
```

## Monitoramento

### Métricas Sugeridas
- Taxa de sucesso das consultas
- Tempo médio por consulta
- Rate limit hits por hora
- CNPJs com acronym vs. sem acronym

### Logs Implementados
- Progresso de processamento
- Erros por CNPJ
- Rate limit ativado
- Estatísticas finais

## Extensibilidade

### Pontos de Extensão
1. **Novos Campos**: Adicionar extração de outros campos da API
2. **Formatos**: Suporte a Excel, JSON como entrada/saída
3. **APIs**: Integração com outras APIs de CNPJ
4. **Cache**: Implementar cache local para evitar consultas duplicadas

### Exemplo de Extensão
```python
class ConsultorCNPJAExtendido(ConsultorCNPJA):
    def extrair_campos_personalizados(self, dados):
        return {
            'acronym': dados.get('acronym'),
            'capital_social': dados.get('capitalStock', {}).get('value'),
            'data_abertura': dados.get('registrations', [{}])[0].get('registeredAt')
        }
```
