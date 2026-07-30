# FinIA — Assistente Virtual Financeiro com Inteligência Artificial

Projeto desenvolvido para o desafio **Construa seu Assistente Virtual com Inteligência Artificial**, da trilha **Bradesco — Dados, Cibersegurança & GenAI**, na DIO.

O **FinIA** é um protótipo educacional de relacionamento financeiro que combina:

- compreensão de perguntas em linguagem natural;
- respostas contextualizadas sobre produtos e segurança financeira;
- simulações demonstrativas de investimentos, empréstimos e metas;
- persistência do histórico da conversa;
- boas práticas de UX, privacidade e uso responsável de IA;
- integração opcional com um modelo generativo por meio da API da OpenAI.

> Este projeto não acessa contas bancárias, não movimenta dinheiro e não substitui orientação financeira profissional.

## Funcionalidades

### FAQ inteligente

O assistente pesquisa uma base local de conhecimento para explicar temas como:

- PIX e transferências;
- cartão de crédito;
- empréstimos e financiamentos;
- investimentos;
- segurança digital;
- renegociação de dívidas;
- proteção de dados.

### Simulações financeiras

O usuário pode escrever perguntas como:

```text
Simule R$ 1.000 a 1% ao mês por 12 meses.
Calcule um empréstimo de R$ 10.000 a 2% ao mês em 24 meses.
Quanto devo guardar por mês para alcançar R$ 20.000 em 36 meses a 0,8% ao mês?
```

As simulações são apenas demonstrativas e apresentam premissas e fórmulas de maneira transparente.

### Contexto e persistência

As mensagens são salvas localmente em SQLite. Assim, a conversa permanece disponível quando a aplicação é recarregada.

### IA generativa opcional

Sem chave de API, a aplicação funciona em **modo local**, usando intenção, recuperação da base de conhecimento e respostas estruturadas.

Com `OPENAI_API_KEY`, o projeto utiliza a API da OpenAI para tornar as respostas mais naturais, mantendo a base local e as regras de segurança como contexto.

### Segurança e privacidade

O assistente:

- alerta quando identifica CPF, senha, número de cartão ou código de segurança;
- não solicita credenciais;
- não promete rentabilidade;
- diferencia conteúdo educacional de recomendação financeira;
- informa as premissas usadas nas simulações.

## Arquitetura

```text
Usuário
  ↓
Interface Streamlit
  ↓
Camada de segurança
  ↓
Identificação de intenção
  ├── Simuladores financeiros
  ├── FAQ / base de conhecimento
  └── IA generativa opcional
  ↓
Persistência SQLite
```

## Estrutura do projeto

```text
.
├── app.py
├── main.py
├── data/
│   └── faqs.json
├── src/
│   ├── __init__.py
│   ├── assistant.py
│   ├── finance.py
│   ├── generative.py
│   ├── knowledge_base.py
│   ├── models.py
│   ├── safety.py
│   └── storage.py
├── tests/
│   ├── test_assistant.py
│   ├── test_finance.py
│   └── test_storage.py
├── .github/workflows/tests.yml
├── .env.example
├── .gitignore
├── pyproject.toml
└── requirements.txt
```

## Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/LuisFelipeRC1/desafio-assistente-virtual-IA.git
cd desafio-assistente-virtual-IA
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux ou macOS:

```bash
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure a IA generativa, opcionalmente

```bash
cp .env.example .env
```

Defina as variáveis no ambiente:

```env
OPENAI_API_KEY=sua_chave
OPENAI_MODEL=gpt-5
```

Nunca publique sua chave no GitHub. Quando nenhuma chave é informada, o modo local é ativado automaticamente.

### 5. Inicie a interface

```bash
streamlit run app.py
```

Também é possível testar pelo terminal:

```bash
python main.py
```

## Testes

```bash
pytest
```

Os testes cobrem:

- juros compostos;
- parcelas de empréstimo;
- cálculo de meta financeira;
- identificação de intenção;
- proteção contra dados sensíveis;
- persistência e exclusão de conversas.

## Exemplos de experiência

**Pergunta**

```text
O que devo fazer se receber uma mensagem pedindo minha senha?
```

**Resposta esperada**

O assistente explica que instituições financeiras não devem solicitar senha ou código de autenticação por mensagem, orienta a não clicar em links e recomenda utilizar apenas canais oficiais.

---

**Pergunta**

```text
Simule R$ 5.000 a 0,9% ao mês por 18 meses.
```

**Resposta esperada**

O assistente apresenta valor inicial, taxa, prazo, montante estimado, rendimento e a fórmula utilizada.

## Princípios de UX aplicados

- linguagem simples e direta;
- transparência sobre limitações;
- mensagens de erro acionáveis;
- atalhos para dúvidas frequentes;
- feedback visual durante o processamento;
- separação entre informação, simulação e recomendação;
- controle do usuário para limpar o histórico.

## Limitações

- não consulta saldo, extrato, fatura ou dados bancários reais;
- não executa transações;
- não considera impostos, tarifas, inflação ou regras específicas de instituições;
- a base de conhecimento é pequena e tem finalidade educacional;
- resultados de IA generativa devem ser revisados antes de qualquer decisão real.

## Próximas evoluções

- autenticação;
- base de conhecimento vetorial;
- avaliação automática de qualidade das respostas;
- suporte a voz;
- acessibilidade ampliada;
- integração com APIs financeiras em ambiente controlado;
- painel de métricas de experiência.

## Autor

Desenvolvido por **Luis Felipe Ramalho Carvalho** para fins educacionais.

## Licença

Distribuído sob a licença MIT.
