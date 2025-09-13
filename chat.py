import google.generativeai as genai
import streamlit as st


@st.fragment
def chat(api_key, input_data):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemma-3-27b-it')

    st.header("Chat Assistente")

    # Inicializar histórico
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Botão para limpar chat
    if st.button("Limpar Chat"):
        st.session_state.messages = []
        st.rerun()

    # Container para mensagens com altura fixa e scroll
    chat_container = st.container(height=400)

    with chat_container:
        # Mostrar mensagens anteriores com chat_message
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

    # Input do usuário sempre embaixo
    if user_input := st.chat_input("Digite sua mensagem..."):
        # Adicionar mensagem do usuário ao histórico
        st.session_state.messages.append({
            "role": "user",
            "content": f'Usuario:\n\n{user_input}'
        })

        # Mostrar mensagem do usuário imediatamente
        with chat_container:
            with st.chat_message("user"):
                st.write(f'Usuario:\n\n{user_input}')

        # Mostrar indicador de carregamento
        with chat_container:
            with st.chat_message("assistant"):
                with st.spinner("Pensando..."):
                    try:
                        # Preparar histórico para Gemini
                        chat_history = []
                        for msg in st.session_state.messages[:-1]:
                            if msg["role"] == "user":
                                chat_history.append({"role": "user", "parts": f'Usuario:\n\n{[msg["content"]]}'})
                            else:
                                chat_history.append({"role": "model", "parts": f'Usuario:\n\n{[msg["content"]]}'})

                        # Iniciar chat com histórico
                        chat = model.start_chat(history=chat_history)

                        # Enviar mensagem atual
                        response = chat.send_message(f'com base nestes dados: {input_data} responda: {user_input}')
                        reply = response.text

                        # Adicionar resposta da IA ao histórico
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f'Julia:\n\n{reply}'
                        })

                    except Exception as e:
                        reply = f"Erro: {e}"
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": reply
                        })

        st.rerun(scope="fragment")