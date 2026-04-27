# Santorini API 🏛️

API REST de restaurante com pipeline de Machine Learning para predição de churn de clientes, desenvolvida com FastAPI e integração contínua via GitHub Actions.

---

## Sobre o projeto

Este projeto foi desenvolvido como parte da disciplina de Ciência de Dados 2 (CDIA) e cobre um fluxo completo de engenharia de software e MLOps:

- API REST organizada com roteamento modular
- Pipeline de ML com dados sintéticos, treinamento e publicação no Hugging Face Hub
- Suíte de testes automatizados com pytest
- CI/CD com GitHub Actions em dois estágios

---

## Estrutura do projeto

```
Aula-01---CDIA-7/
├── .github/
│   └── workflows/
│       └── ci.yml              # Pipeline de CI/CD
├── Santorini/
│   ├── main.py                 # Aplicação FastAPI principal
│   ├── config.py               # Configurações da aplicação
│   ├── models/                 # Modelos Pydantic
│   │   ├── pratos.py
│   │   ├── bebidas.py
│   │   ├── pedidos.py
│   │   └── reservas.py
│   └── routers/                # Routers da API
│       ├── pratos.py
│       ├── bebidas.py
│       ├── pedidos.py
│       ├── reservas.py
│       └── predict.py          # Endpoint de predição de churn
├── tests/
│   ├── test_pratos.py
│   ├── test_bebidas.py
│   ├── test_pedidos.py
│   ├── test_reservas.py
│   └── test_modelo.py          # Testes de integração do modelo
├── gerar_dados.py              # Geração de dataset sintético de churn
├── treinar_modelo.py           # Treinamento e serialização do modelo
├── model_utils.py              # Carregamento do modelo via Hugging Face Hub
├── model.pkl                   # Modelo serializado
├── churn_dataset.csv           # Dataset gerado
└── requirements.txt
```

---

## Tecnologias

- **Python 3.12**
- **FastAPI** — framework web
- **Pydantic** — validação de dados
- **scikit-learn** — treinamento do modelo de ML
- **joblib** — serialização do modelo
- **Hugging Face Hub** — registry do modelo
- **pytest + httpx** — testes automatizados
- **GitHub Actions** — CI/CD

---

## Instalação e execução local

### Pré-requisitos

- Python 3.12+
- Conta no [Hugging Face](https://huggingface.co) com token de acesso

### Instalação

```bash
git clone https://github.com/becamparezzo/Aula-01---CDIA-7
cd Aula-01---CDIA-7
pip install -r requirements.txt
```

### Configuração do token

```bash
export HF_TOKEN=hf_seu_token_aqui
```

### Executando a API

```bash
uvicorn Santorini.main:app --reload
```

Acesse a documentação interativa em `http://localhost:8000/docs`.

---

## Endpoints

### Restaurante

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Informações do restaurante |

### Pratos

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/pratos/pratos` | Lista todos os pratos (filtros: `categoria`, `preco_maximo`) |
| GET | `/pratos/pratos/{id}` | Busca um prato pelo ID |
| POST | `/pratos/pratos` | Adiciona um novo prato |

### Bebidas

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/bebidas/bebidas` | Lista todas as bebidas (filtros: `tipo`, `alcoolica`) |
| GET | `/bebidas/bebidas/{id}` | Busca uma bebida pelo ID |
| POST | `/bebidas/bebidas` | Adiciona uma nova bebida |

### Pedidos

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/pedidos/pedidos` | Cria um novo pedido |

### Reservas

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/reservas/` | Cria uma nova reserva |
| GET | `/reservas/` | Lista reservas (filtros: `data`, `apenas_ativas`) |
| GET | `/reservas/{id}` | Busca uma reserva pelo ID |
| GET | `/reservas/mesa/{numero}` | Lista reservas de uma mesa |
| DELETE | `/reservas/{id}` | Cancela uma reserva |

### Predição de Churn

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/predict/` | Prediz risco de churn de um cliente |

#### Exemplo de requisição — `/predict/`

```json
{
  "dias_sem_login": 90,
  "num_chamados": 8,
  "valor_mensalidade": 200.0,
  "meses_contrato": 3,
  "nps_score": 2
}
```

#### Exemplo de resposta

```json
{
  "churn": true,
  "probabilidade": 1.0,
  "mensagem": "Cliente com risco de churn"
}
```

---

## Pipeline de Machine Learning

### Dados sintéticos

O dataset é gerado pela função `gerar_churn()` em `gerar_dados.py`, com 5 features que simulam o comportamento de clientes:

| Feature | Descrição |
|---------|-----------|
| `dias_sem_login` | Dias desde o último acesso (clientes com churn têm mais) |
| `num_chamados` | Chamados de suporte abertos (clientes com churn têm mais) |
| `valor_mensalidade` | Valor mensal do contrato em R$ |
| `meses_contrato` | Tempo de contrato em meses (clientes com churn têm menos) |
| `nps_score` | NPS do cliente de 0 a 10 (clientes com churn têm menor) |

Para gerar e treinar:

```bash
python gerar_dados.py
python treinar_modelo.py
```

### Modelo

- Algoritmo: `RandomForestClassifier` com 100 estimadores
- Acurácia no conjunto de teste: 100% (dados sintéticos bem separados)
- Modelo publicado em: [becamparezzo/churn-model](https://huggingface.co/becamparezzo/churn-model)

---

## Testes

### Rodando todos os testes

```bash
python -m pytest tests/ -v
```

### Rodando por categoria

```bash
# Apenas testes da API
python -m pytest tests/ -v --ignore=tests/test_modelo.py

# Apenas testes do modelo
python -m pytest tests/test_modelo.py -v
```

### Cobertura atual

| Arquivo | Testes | Status |
|---------|--------|--------|
| `test_pratos.py` | 5 | ✅ |
| `test_bebidas.py` | 7 | ✅ |
| `test_pedidos.py` | 4 | ✅ |
| `test_reservas.py` | 7 | ✅ |
| `test_modelo.py` | 4 | ✅ |
| **Total** | **27** | ✅ |

---

## CI/CD

O pipeline está definido em `.github/workflows/ci.yml` e roda a cada push ou pull request no branch `main`.

### Fluxo

```
push/PR
   ↓
testes-smoke (sempre roda)
   → instala dependências
   → roda 23 testes da API
   ↓ (só se smoke passar)
testes-integracao (só em push no main)
   → verifica HF_TOKEN
   → baixa modelo do Hugging Face Hub
   → roda 4 testes do /predict
```

### Configuração do secret

Para o job de integração funcionar, configure o secret `HF_TOKEN` no repositório:

**Settings → Secrets and variables → Actions → New repository secret**

- Name: `HF_TOKEN`
- Secret: seu token do Hugging Face com permissão de leitura

---

## Autor

Rebecca Campos — [@becamparezzo](https://github.com/becamparezzo)