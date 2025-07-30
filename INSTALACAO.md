# Guia de Instalação - Sistema de Consulta CNPJA

## Pré-requisitos

- **Python 3.8+** instalado no sistema
- **pip** (gerenciador de pacotes Python)
- **Conexão com internet** para acessar a API CNPJA

## Instalação Rápida (Windows)

### Opção 1: Instalação Automática
1. Baixe todos os arquivos do projeto
2. Execute o arquivo `instalar.bat`
3. Aguarde a instalação das dependências

### Opção 2: Instalação Manual

#### Passo 1: Verificar Python
```bash
python --version
```
Deve retornar Python 3.8 ou superior.

#### Passo 2: Instalar Dependências
```bash
pip install -r requirements.txt
```

#### Passo 3: Testar Instalação
```bash
python teste.py
```

## Instalação no Linux/Mac

#### Passo 1: Verificar Python
```bash
python3 --version
pip3 --version
```

#### Passo 2: Instalar Dependências
```bash
pip3 install -r requirements.txt
```

#### Passo 3: Testar Sistema
```bash
python3 teste.py
```

## Dependências Instaladas

O sistema instalará automaticamente:

- **requests** (>=2.28.0) - Para requisições HTTP à API
- **pandas** (>=1.5.0) - Para manipulação de arquivos CSV
- **urllib3** (>=1.26.0) - Para gerenciamento de conexões

## Verificação da Instalação

### Teste Básico
```bash
python -c "from consultor_simples import ConsultorCNPJA; print('✓ Instalação OK')"
```

### Teste com Consulta (Opcional)
```bash
python exemplo_uso.py
```

## Solução de Problemas

### Erro: "ModuleNotFoundError"
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Erro: "Permission denied"
Use o parâmetro `--user`:
```bash
pip install -r requirements.txt --user
```

### Erro de SSL/Certificados
```bash
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### Erro de Rate Limit na API
- Aguarde 1 minuto entre testes
- A API permite apenas 5 consultas por minuto

## Estrutura dos Arquivos

Após a instalação, você terá:

```
consulta_cnpj/
├── main.py                  # Interface principal
├── consultor_simples.py     # Classe principal
├── teste.py                 # Testes do sistema
├── exemplo_uso.py           # Exemplo prático
├── exemplo_cnpjs.csv        # CNPJs de exemplo
├── requirements.txt         # Dependências
├── instalar.bat            # Instalador Windows
├── README.md               # Documentação
├── INSTALACAO.md           # Este arquivo
└── DOCUMENTACAO_TECNICA.md # Documentação técnica
```

## Primeiros Passos

### 1. Executar Interface Principal
```bash
python main.py
```

### 2. Testar com CSV de Exemplo
O sistema inclui um arquivo `exemplo_cnpjs.csv` pronto para teste.

### 3. Criar Seu Próprio CSV
Formato necessário:
```csv
cnpj
07.526.557/0001-16
11.222.333/0001-81
```

## Configurações Opcionais

### Timeout das Requisições
Edite `consultor_simples.py` linha ~65:
```python
response = requests.get(url, timeout=30)
```

### Rate Limit Personalizado
Edite `consultor_simples.py` linha ~15:
```python
self.rate_limit = 5  # Altere para o valor desejado
```

## Atualizações

Para atualizar as dependências:
```bash
pip install -r requirements.txt --upgrade
```

## Desinstalação

Para remover as dependências:
```bash
pip uninstall requests pandas urllib3
```

## Suporte

Em caso de problemas:

1. **Verifique a versão do Python** (`python --version`)
2. **Teste a conexão com internet**
3. **Execute os testes** (`python teste.py`)
4. **Verifique os logs** no terminal durante a execução

---

**Sistema pronto para uso após a instalação!**

Execute `python main.py` para começar a usar o sistema de consulta CNPJA.
