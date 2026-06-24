# Robô de Atendimento IA

Microsserviço de chatbot para atendimento ao cliente utilizando FastAPI, LangChain e Deepseek. Este serviço roda de forma independente, sem dependência direta do backend principal.

## Pré-requisitos

- Python 3.9+
- Chave de API da Deepseek (e/ou outras variáveis de ambiente necessárias)
- (Opcional) Docker para execução em contêiner

## Configuração Inicial

1. Clone o repositório e acesse a pasta `robo_ia_atendimento`.
2. Crie uma cópia do arquivo de configuração de ambiente:
   ```bash
   cp .env.example .env
   ```
3. Edite o arquivo `.env` e preencha as variáveis de ambiente necessárias (como a chave da Deepseek, URLs, etc).

## Como Executar Localmente

Recomenda-se o uso de um ambiente virtual (venv).

1. **Crie e ative o ambiente virtual:**
   - **Windows:**
     ```cmd
     python -m venv venv
     venv\Scripts\activate
     ```
   - **Linux/macOS:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Inicie o servidor:**
   Você pode iniciar o servidor de duas formas:
   
   **Opção A: Usando o script principal (porta 8002 padrão)**
   ```bash
   python main.py
   ```

   **Opção B: Usando uvicorn com hot-reload (ideal para desenvolvimento)**
   ```bash
   uvicorn main:app --reload --port 8002
   ```

A API estará acessível em `http://localhost:8002`.

## Como Executar com Docker

Se preferir rodar via Docker, você pode construir e executar o contêiner:

1. **Construa a imagem:**
   ```bash
   docker build -t robo_ia_atendimento .
   ```

2. **Execute o contêiner:**
   ```bash
   docker run -p 8002:8002 --env-file .env robo_ia_atendimento
   ```

## Como Testar

### 1. Documentação Interativa (Swagger UI)
A forma mais fácil de testar as rotas da API é através do Swagger UI embutido no FastAPI.
- Com o servidor rodando, acesse no seu navegador:
  [http://localhost:8002/docs](http://localhost:8002/docs)
- Lá você poderá ver todas as rotas disponíveis e testá-las interativamente.

### 2. Testes de Saúde (Healthcheck)
Verifique se o serviço está no ar acessando as rotas base:
```bash
curl http://localhost:8002/
# Resposta esperada: {"service": "robo_ia_atendimento", "status": "running"}

curl http://localhost:8002/health
# Resposta esperada: {"status": "healthy", "service": "robo_ia_atendimento"}
```

### 3. Testando as Funcionalidades de IA
Para testar a conversação do robô, você pode usar a rota do Swagger UI correspondente (provavelmente localizada no `router.py`, por exemplo, enviando uma requisição POST com a mensagem do cliente).
