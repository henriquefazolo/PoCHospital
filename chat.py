import google.generativeai as genai
import streamlit as st


@st.fragment
def chat(api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemma-3-27b-it')

    st.header("Chat Assistente")

    # Inicializar histórico
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Container para mensagens (com altura limitada)
    chat_container = st.container()

    with chat_container:
        # Mostrar mensagens anteriores
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.write(f"**Você:** {message['content']}")
            else:
                st.write(f"**Bot:** {message['content']}")

    # Input do usuário no sidebar
    user_input = st.text_input("Digite sua mensagem:", key="chat_input")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Enviar") and user_input:
            # Adicionar mensagem do usuário
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Gerar resposta da IA com Gemini
            try:
                # Preparar histórico para Gemini
                chat_history = []
                for msg in st.session_state.messages[:-1]:  # Excluir última mensagem (atual)
                    if msg["role"] == "user":
                        chat_history.append({"role": "user", "parts": [msg["content"]]})
                    else:
                        chat_history.append({"role": "model", "parts": [msg["content"]]})

                # Iniciar chat com histórico
                chat = model.start_chat(history=chat_history)

                # Enviar mensagem atual
                response = chat.send_message(user_input)
                reply = response.text

                st.session_state.messages.append({"role": "assistant", "content": reply})

                # Rerun para atualizar
                st.rerun(scope="fragment")

            except Exception as e:
                st.error(f"Erro: {e}")

    with col2:
        if st.button("Limpar Chat"):
            st.session_state.messages = []
            st.rerun()
