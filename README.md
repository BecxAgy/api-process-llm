# API Process Edict

Este projeto é uma API FastAPI que processa documentos PDF através de mensagens SQS e armazenamento S3, utilizando múltiplos modelos de IA via OpenRouter.

## Funcionalidades Principais

- **Múltiplos Modelos de IA**: Suporte a Gemma 3n 4B, DeepSeek R1T2 Chimera, e Dolphin 3.0 R1 Mistral 24B
- **Extração de Documentos**: Análise automática de editais de licitação para extrair requisitos documentais
- **API REST**: Endpoints para upload e processamento de PDFs
- **Consumer SQS**: Processamento automático via fila SQS
- **Estrutura Modular**: Arquitetura com separação de responsabilidades

## Modelos de IA Disponíveis

1. **Gemma 3n 4B** (`gemma`) - Modelo do Google, ótimo para tarefas gerais
2. **DeepSeek R1T2 Chimera** (`deepseek`) - Especializado em análise de código e documentos
3. **Dolphin 3.0 R1 Mistral 24B** (`dolphin`) - **Modelo padrão**, otimizado para compreensão de texto

## Estrutura do Projeto

```
api-process-edict/
├── app/
│   ├── api/             # Endpoints da API REST
│   ├── clients/         # Configuração de clientes (AWS, OpenRouter)
│   ├── config/          # Configurações da aplicação
│   ├── consumers/       # Processadores de mensagens
│   ├── core/           # Funcionalidades centrais (logging, exceptions)
│   ├── models/         # Modelos Pydantic e templates de prompt
│   ├── services/       # Serviços de negócio
│   ├── main.py         # Aplicação FastAPI principal
│   └── sqs_consumer.py # Consumer SQS refatorado
├── requirements.txt    # Dependências Python
├── run.py             # Script de inicialização
├── start.ps1          # Script PowerShell para Windows
├── .env.example       # Exemplo de variáveis de ambiente
└── README.md          # Este arquivo
```

## Configuração

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e configure suas credenciais:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:

```env
# AWS Configuration
AWS_ACCESS_KEY=sua_aws_access_key
AWS_SECRET_KEY=sua_aws_secret_key
AWS_REGION=us-east-1
SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/123456789012/sua-fila
AWS_S3_BUCKET=seu-bucket-s3

# OpenRouter AI Configuration
OPENROUTER_API_KEY=sua_openrouter_api_key

# Application Configuration
LOG_LEVEL=INFO
MAX_MESSAGES_PER_POLL=1
POLL_WAIT_TIME=10
```

## Como Executar

### Opção 1: Usando o script run.py (Recomendado)

```bash
python run.py
```

### Opção 2: Diretamente com Uvicorn

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Opção 3: Para Produção

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Endpoints Disponíveis

### Endpoints Básicos
- `GET /` - Endpoint raiz com informações da API
- `GET /health` - Health check da aplicação
- `GET /consumer/status` - Status do consumer SQS

### Endpoints de Processamento
- `GET /api/v1/models` - Lista modelos de IA disponíveis
- `POST /api/v1/process-pdf` - Upload e processamento de PDF
- `POST /api/v1/test-llm` - Teste direto de modelos LLM

### Exemplo de Uso da API

**Listar modelos disponíveis:**
```bash
curl -X GET "http://localhost:8000/api/v1/models"
```

**Processar PDF:**
```bash
curl -X POST "http://localhost:8000/api/v1/process-pdf?model=dolphin" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@edital.pdf"
```

**Testar modelo com prompt customizado:**
```bash
curl -X POST "http://localhost:8000/api/v1/test-llm?model=gemma" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Olá, como você está?"}'
```

## Funcionalidades

1. **Consumer SQS**: Monitora fila SQS para novas mensagens
2. **Download S3**: Baixa arquivos PDF do S3 baseado nas mensagens
3. **Extração de Texto**: Extrai texto de PDFs usando PyPDF2
4. **Processamento IA**: Processa documentos usando modelos OpenRouter
5. **API REST**: Endpoints para upload direto e monitoramento
6. **Análise de Editais**: Extrai requisitos documentais automaticamente

## Formato de Resposta

O sistema retorna um JSON estruturado com os documentos exigidos:

```json
{
  "documents": [
    {
      "name": "Certidão Negativa de Débitos",
      "exigenceStatus": "OBRIGATORIO",
      "additionalInfo": "Válida na data da sessão",
      "possibleToAttach": true
    },
    {
      "name": "Declaração de Capacidade Técnica",
      "exigenceStatus": "OPCIONAL",
      "additionalInfo": null,
      "possibleToAttach": true
    }
  ],
  "total_documents": 2,
  "mandatory_count": 1,
  "optional_count": 1
}
```

## Logs

Os logs são salvos em:
- Console (stdout)
- Arquivo `app.log`

## Arquitetura

O projeto segue os princípios de:
- **Separação de Responsabilidades**: Cada módulo tem uma responsabilidade específica
- **Injeção de Dependência**: Clients são configurados separadamente
- **Modularidade**: Código organizado em services, clients, consumers
- **Observabilidade**: Logging estruturado e endpoints de monitoramento

## Desenvolvimento

Para desenvolvimento, use:

```bash
python run.py
```

Isso iniciará a aplicação com auto-reload habilitado.
