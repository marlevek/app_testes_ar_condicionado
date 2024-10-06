import streamlit as st
import numpy as np
import os
import base64

st.set_page_config('Testes em Ar Condiciionado', page_icon=':test_tube:')

# Função para capturar áudio do navegador
def audio_recorder():
    st.write("Clique no botão abaixo para gravar seu áudio.")
    
    # Variável de estado para controlar a gravação
    if 'recording' not in st.session_state:
        st.session_state.recording = False

    # Botão para iniciar/parar a gravação
    if st.button("Iniciar Gravação"):
        st.session_state.recording = True
        st.markdown(
            """
            <script>
            let mediaRecorder;
            let audioChunks = [];

            async function startRecording() {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);

                mediaRecorder.ondataavailable = function(event) {
                    audioChunks.push(event.data);
                };

                mediaRecorder.onstop = function() {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    const url = URL.createObjectURL(audioBlob);
                    const audio = new Audio(url);
                    audio.play();

                    const reader = new FileReader();
                    reader.readAsDataURL(audioBlob);
                    reader.onloadend = function() {
                        const base64data = reader.result;
                        window.parent.postMessage(base64data, "*");
                    };
                };

                mediaRecorder.start();
                st.write("Gravando...");

                // Função para parar a gravação ao clicar no botão
                document.getElementById('stop-button').onclick = function() {
                    mediaRecorder.stop();
                    st.session_state.recording = false;
                };
            }

            window.onload = function() {
                startRecording();
            }
            </script>
            """,
            unsafe_allow_html=True
        )

    if st.session_state.recording:
        st.markdown("<button id='stop-button'>Parar Gravação</button>", unsafe_allow_html=True)
    
    # Receber o áudio gravado
    audio_base64 = st.session_state.get('audio_base64', None)
    if audio_base64:
        st.audio(audio_base64, format='audio/wav')

# Executar a função de gravação de áudio
audio_recorder()


# Opções para o selectbox
fabricantes = ['selecione...', 'LG', 'MIDEA']
modelos = ['selecione...', 'Hi Wall', 'Teto', 'Cassete']
tipos_teste = ['selecione...', 'Aparelho não liga', 'Compressão do compressor', 'Comunicação entre as unidades', 'Disjuntor Desarmando', 'Evaporador Congelando', 'Motoventilador da Condensadora Convencional', 'Motoventilador da Condensadora Inverter', 'Motoventilador da Evaporadora', 'Rendimento do Aparelho', 'Sensores', 'Superaquecimento','Teste de Compressor Inverter', 'Válvula Reversora']

# Sidebar para seleção manual
with st.sidebar:
    st.title('Selecione os dados')
    fabricante = st.selectbox('Fabricante', fabricantes)
    modelo = st.selectbox('Modelo', modelos)
    st.write('Digite ou Fale o tipo de teste desejado')
    tipo_teste_manual = st.selectbox('Tipo de Teste', tipos_teste)

    # Botão para usar reconhecimento de fala para selecionar o tipo de teste
    if st.button("Falar Tipo de Teste"):
        capturar_audio()  # Captura o áudio do usuário
        tipo_teste_falado = reconhecer_fala()  # Reconhece o que o usuário disse
        
        # Comparar o texto reconhecido com as opções de tipos de teste
        if tipo_teste_falado:
            tipo_teste_falado = tipo_teste_falado.lower()  # Para evitar problemas de case
            tipo_teste_encontrado = None
            for teste in tipos_teste:
                if teste.lower() in tipo_teste_falado:
                    tipo_teste_encontrado = teste
                    break
            
            if tipo_teste_encontrado:
                st.success(f"Tipo de Teste identificado: {tipo_teste_encontrado}")
                tipo_teste_manual = tipo_teste_encontrado  # Atualiza o tipo de teste com a fala reconhecida
            else:
                st.error("Tipo de Teste não identificado. Tente novamente.")
        
st.title('**Testes em Ar Condicionado** :male-mechanic:')
st.write('''
         Obs.: Para alguns testes é necessário ter os seguintes instrumentos:
         1. Multímetro
         2. Alicate Amperímetro
         3. Conjunto Manifold
         ''')

# Carregar instruções para o teste selecionado
if fabricante != 'selecione...':  # Verifica se um fabricante foi selecionado
    if tipo_teste_manual != 'selecione...':  # Verifica se um tipo de teste foi selecionado
        instrucoes = carregar_instrucoes(tipo_teste_manual)  # Passa tipo_teste como argumento para a função
        
        if instrucoes:  # Se houver instruções a serem exibidas
            st.subheader(f'Teste: {tipo_teste_manual}')
            
            # Formatar e exibir as instruções, garantindo que as quebras de linha sejam respeitadas
            st.markdown(instrucoes.replace("\n", "<br>"), unsafe_allow_html=True)  # Exibe as instruções carregadas
        else:
            st.warning("Instruções não encontradas para o tipo de teste selecionado.")
    else:
        st.warning("Por favor, selecione um tipo de teste válido.")
else:
    st.warning("Por favor, selecione um fabricante.")








































