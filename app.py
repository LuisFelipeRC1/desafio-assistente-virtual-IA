"""Interface Streamlit do FinIA."""

from __future__ import annotations

import os
import uuid

import streamlit as st

from src.assistant import FinancialAssistant
from src.finance import (
    compound_interest,
    format_simulation,
    loan_payment,
    monthly_savings_for_goal,
)
from src.storage import SQLiteConversationStore


st.set_page_config(
    page_title="FinIA — Assistente Financeiro",
    page_icon="💬",
    layout="centered",
)

st.title("💬 FinIA")
st.subheader("Assistente financeiro educacional com IA")
st.caption(
    "Tire dúvidas, faça simulações e aprenda sobre segurança financeira. "
    "O protótipo não acessa contas nem executa transações."
)

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

database_path = os.getenv("FINIA_DB_PATH", "data/conversations.db")
store = SQLiteConversationStore(database_path)
assistant = FinancialAssistant()

with st.sidebar:
    st.header("Sobre esta sessão")
    ai_enabled = bool(os.getenv("OPENAI_API_KEY"))
    st.success("IA generativa ativada") if ai_enabled else st.info("Modo local ativado")
    st.caption(
        "No modo local, as respostas usam a base de FAQs e os simuladores do projeto."
    )

    if st.button("Limpar conversa", use_container_width=True):
        store.clear(st.session_state.session_id)
        st.rerun()

    st.divider()
    st.subheader("Perguntas sugeridas")
    st.markdown(
        """
- Como evitar golpes no PIX?
- O que devo comparar em um empréstimo?
- Como funciona o cartão de crédito?
- Simule R$ 1.000 a 1% ao mês por 12 meses.
"""
    )

    st.divider()
    st.subheader("Simulações rápidas")

    simulation_type = st.selectbox(
        "Escolha",
        ("Investimento", "Empréstimo", "Meta financeira"),
    )

    with st.form("quick_simulation"):
        if simulation_type == "Investimento":
            principal = st.number_input("Valor inicial (R$)", min_value=1.0, value=1000.0)
            rate = st.number_input("Taxa mensal (%)", min_value=0.0, value=1.0)
            months = st.number_input("Prazo (meses)", min_value=1, value=12, step=1)
            initial = 0.0
        elif simulation_type == "Empréstimo":
            principal = st.number_input(
                "Valor financiado (R$)", min_value=1.0, value=10000.0
            )
            rate = st.number_input("Taxa mensal (%)", min_value=0.0, value=2.0)
            months = st.number_input(
                "Número de parcelas", min_value=1, value=24, step=1
            )
            initial = 0.0
        else:
            principal = st.number_input("Meta (R$)", min_value=1.0, value=20000.0)
            rate = st.number_input("Taxa mensal (%)", min_value=0.0, value=0.8)
            months = st.number_input("Prazo (meses)", min_value=1, value=36, step=1)
            initial = st.number_input(
                "Valor já guardado (R$)", min_value=0.0, value=0.0
            )

        submitted = st.form_submit_button("Calcular", use_container_width=True)

    if submitted:
        if simulation_type == "Investimento":
            result = compound_interest(principal, rate, int(months))
        elif simulation_type == "Empréstimo":
            result = loan_payment(principal, rate, int(months))
        else:
            result = monthly_savings_for_goal(
                principal,
                rate,
                int(months),
                initial,
            )
        st.markdown(format_simulation(result))

history = store.get_messages(st.session_state.session_id)

if not history:
    with st.chat_message("assistant"):
        st.markdown(
            "Olá! Posso explicar produtos financeiros, orientar sobre segurança "
            "digital e realizar simulações educacionais."
        )

for message in history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Digite sua dúvida financeira")

if prompt:
    store.add_message(st.session_state.session_id, "user", prompt)

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analisando sua pergunta..."):
            reply = assistant.answer(prompt, history=history)
            st.markdown(reply.text)
            if reply.sources:
                with st.expander("Base utilizada"):
                    for source in reply.sources:
                        st.write(f"- {source}")
            if reply.used_generative_ai:
                st.caption("Resposta refinada por IA generativa.")

    store.add_message(st.session_state.session_id, "assistant", reply.text)

st.divider()
st.caption(
    "Não compartilhe CPF, senha, token, CVV ou número completo do cartão. "
    "Conteúdo educacional; consulte canais oficiais antes de decidir."
)
