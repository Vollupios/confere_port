# Sistema de Consulta CNPJ - Brasil API

Sistema automatizado para consulta de informações públicas de empresas através da Brasil API, com controle de rate limiting (5 consultas por minuto) e processamento em lote via arquivos CSV.

## 🎯 Funcionalidades

- ✅ **Consulta individual de CNPJs** - Consulta um CNPJ específico
- ✅ **Processamento em lote** - Processa múltiplos CNPJs via arquivo CSV
- ✅ **Controle de rate limiting** - Intervalo fixo de 15 segundos entre consultas
- ✅ **Extração de porte** - Foca na extração do campo "porte" da empresa
- ✅ **Exportação de resultados** - Salva resultados em arquivo CSV com timestamp
- ✅ **Validação de CNPJs** - Valida formato e remove pontuação automaticamente
- ✅ **Interface amigável** - Menu interativo para facilitar o uso

## 🚀 Instalação

### Método 1: Instalação Automática (Windows)
```bash
exec instalar.bat
```

### Método 2: Instalação Manual
```bash
pip install -r requirements.txt
```

## 📋 Dependências

- `requests` - Para requisições HTTP à API
- `pandas` - Para manipulação de dados CSV
- `urllib3` - Para gerenciamento de conexões HTTP

## 🔧 Como Usar

### 1. Interface Principal
Execute o sistema com menu interativo:
```bash
python main.py
```

O menu oferece as seguintes opções:
- **Opção 1**: Consultar CNPJ individual
- **Opção 2**: Processar arquivo CSV com múltiplos CNPJs  
- **Opção 3**: Processar arquivo TXT com múltiplos CNPJs
- **Opção 4**: Criar arquivo CSV de exemplo
- **Opção 5**: Criar arquivo TXT de exemplo
- **Opção 6**: Sair

### 2. Consulta Individual
```python
from consultor_simples import ConsultorCNPJA

consultor = ConsultorCNPJA()
resultado = consultor.consultar_cnpj("19.131.243/0001-97")

if resultado:
    porte = consultor.extrair_acronym(resultado)
    print(f"Porte: {porte}")
```

### 3. Processamento via CSV

#### Formato do arquivo CSV:
```csv
cnpj
19.131.243/0001-97
11.222.333/0001-81
33.000.167/0001-01
```

#### Código para processamento:
```python
from consultor_simples import ConsultorCNPJA

consultor = ConsultorCNPJA()
resultados = consultor.processar_csv("exemplo_cnpjs.csv")
consultor.salvar_resultados(resultados)
```

### 4. Processamento via TXT

#### Formato do arquivo TXT (um CNPJ por linha):
```txt
19131243000197
07526557000116
11222333000181
33000167000101
```

#### Código para processamento:
```python
from consultor_simples import ConsultorCNPJA

consultor = ConsultorCNPJA()
resultados = consultor.processar_txt("exemplo_cnpjs.txt")
consultor.salvar_resultados(resultados, "resultado_txt.csv")
```

### 5. Processamento Genérico (CSV ou TXT)

```python
from consultor_simples import ConsultorCNPJA

consultor = ConsultorCNPJA()
# Detecta automaticamente o formato pelo arquivo
resultados = consultor.processar_arquivo("meus_cnpjs.csv")  # ou .txt
consultor.salvar_resultados(resultados)
```

## 📊 API Utilizada

**Endpoint**: `GET https://brasilapi.com.br/api/cnpj/v1/{cnpj}`

**Exemplo de requisição**:
```bash
curl --request GET --url 'https://brasilapi.com.br/api/cnpj/v1/19131243000197'
```

**Rate Limit**: 5 consultas por minuto (controlado automaticamente)

## 📁 Estrutura do Projeto

```
consulta_cnpj/
├── 📄 main.py                    # Interface principal com menu
├── 📄 consultor_simples.py       # Classe principal do consultor
├── 📄 instalar.bat              # Instalador para Windows
├── 📄 requirements.txt          # Dependências Python
├── 📄 README.md                 # Este arquivo
├── 📄 DOCUMENTACAO_TECNICA.md   # Documentação técnica detalhada
├── 📄 INSTALACAO.md             # Instruções de instalação
├── 📄 RESUMO_IMPLEMENTACOES.md  # Resumo das implementações
├── 📄 .gitignore                # Arquivos a serem ignorados pelo Git
├── 📁 exemplos/                 # Arquivos de exemplo
│   ├── exemplo_cnpjs.csv        # Exemplo em formato CSV
│   └── exemplo_cnpjs.txt        # Exemplo em formato TXT
├── 📁 docs/                     # Documentação adicional (se necessário)
└── 📁 resultados/               # Arquivos de resultado (gerados automaticamente)
```

## 📈 Arquivo de Resultado

O sistema gera automaticamente um arquivo CSV com os resultados, contendo:

| Campo | Descrição |
|-------|-----------|
| `cnpj_original` | CNPJ como fornecido originalmente |
| `cnpj_limpo` | CNPJ sem formatação (apenas números) |
| `consulta_realizada` | Se a consulta foi realizada com sucesso |
| `acronym` | Campo porte extraído (ex: "DEMAIS", "ME", "EPP") |
| `razao_social` | Razão social da empresa |
| `nome_fantasia` | Nome fantasia |
| `situacao` | Situação cadastral |
| `porte` | Porte da empresa |
| `natureza_juridica` | Natureza jurídica |
| `cnae_fiscal` | Código CNAE fiscal |
| `cnae_fiscal_descricao` | Descrição da atividade principal |
| `telefone` | Telefone de contato |
| `email` | Email de contato |
| `cep` | CEP do endereço |
| `municipio` | Município |
| `uf` | Unidade federativa |
| `logradouro` | Logradouro do endereço |
| `numero` | Número do endereço |
| `bairro` | Bairro |
| `complemento` | Complemento do endereço |

## 🧪 Testes

Execute os testes do sistema:
```bash
python teste.py
```

Os testes verificam:
- ✅ Consulta individual de CNPJ
- ✅ Processamento de arquivo CSV
- ✅ Funcionamento do rate limiting
- ✅ Extração do campo acronym
- ✅ Geração de arquivo de resultados

## ⚠️ Considerações Importantes

### Rate Limiting
- Intervalo **fixo de 15 segundos** entre cada consulta
- Mais conservador que o limite mínimo da API (5 consultas/minuto)
- Garante que nunca exceda os limites mesmo com flutuações de rede
- Tempo previsível: número de CNPJs × 15 segundos

### Tratamento de Erros
- CNPJs inválidos são identificados e ignorados
- Erros de conexão são tratados graciosamente
- Timeouts são configurados para evitar travamentos
- Dados indisponíveis retornam valores padrão

### Performance
- Processa CNPJs sequencialmente respeitando o rate limit
- Exibe progresso durante processamento em lote
- Salva resultados incrementalmente

## 📝 Exemplos Práticos

### Exemplo 1: Consulta Rápida
```python
from consultor_simples import ConsultorCNPJA

consultor = ConsultorCNPJA()
dados = consultor.consultar_cnpj("19131243000197")
porte = consultor.extrair_acronym(dados) if dados else None
print(f"Porte: {porte}")
```

### Exemplo 2: Processamento em Lote
```python
from consultor_simples import ConsultorCNPJA

consultor = ConsultorCNPJA()

# Processa arquivo CSV
resultados = consultor.processar_csv("meus_cnpjs.csv", "coluna_cnpj")

# Salva resultados
consultor.salvar_resultados(resultados, "resultado_final.csv")

# Estatísticas
total = len(resultados)
sucessos = sum(1 for r in resultados if r['consulta_realizada'])
acronyms = sum(1 for r in resultados if r['acronym'])

print(f"Processados: {total}")
print(f"Sucessos: {sucessos}")  
print(f"Acronyms encontrados: {acronyms}")
```

## 🔍 Solução de Problemas

### Erro de Dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Erro de Rate Limit
O sistema controla automaticamente, mas se houver problemas:
- Aguarde 1 minuto entre lotes de consultas
- Verifique se não há outras instâncias rodando

### Arquivo CSV não encontrado
- Verifique se o arquivo está no diretório correto
- Use caminhos absolutos se necessário
- Verifique se a coluna especificada existe

## 📄 Licença

Este projeto é disponibilizado como exemplo educacional para consulta de APIs públicas.

## 🤝 Contribuições

Contribuições são bem-vindas! Abra uma issue ou envie um pull request.

---

**Desenvolvido para consulta automatizada da Brasil API**  
*Respeitando os limites de rate limiting e boas práticas de uso de APIs públicas*
