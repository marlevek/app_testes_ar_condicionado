import streamlit as st
import numpy as np
import sounddevice as sd
import scipy.io.wavfile
import speech_recognition as sr
import os

st.set_page_config('Testes em Ar Condiciionado', page_icon=':test_tube:')

# Função para carregar as instruções de teste a partir de um arquivo txt
def carregar_instrucoes(tipo_teste):
    try:
        with open('testes.txt', 'r', encoding='utf-8') as file:
            conteudo = file.read()
        
        # Dividir o conteúdo por seções
        instrucoes = conteudo.split("\n\n")  # Divide por parágrafos

        # Criar um dicionário para armazenar as instruções
        instrucoes_dict = {}
        for instrucao in instrucoes:
            if instrucao.strip():  # Ignora seções vazias
                titulo, texto = instrucao.split(":", 1)
                instrucoes_dict[titulo.strip()] = texto.strip()

        # Retornar as instruções do tipo de teste solicitado
        return instrucoes_dict.get(tipo_teste, "Instruções não encontradas.")

    except FileNotFoundError:
        return "Arquivo de instruções não encontrado."
    except Exception as e:
        return f"Erro ao ler o arquivo: {str(e)}"

# Função para capturar áudio e salvar como um arquivo .wav
def capturar_audio(duracao=5, taxa_amostragem=16000, arquivo="audio.wav"):
    st.write("Gravando...")
    audio = sd.rec(int(duracao * taxa_amostragem), samplerate=taxa_amostragem, channels=1, dtype='int16')
    sd.wait()  # Espera o áudio terminar de gravar
    scipy.io.wavfile.write(arquivo, taxa_amostragem, audio)
    st.write(f"Gravação salva como {arquivo}")
    

# Função para reconhecer fala usando o arquivo de áudio gravado
def reconhecer_fala(arquivo="audio.wav"):
    recognizer = sr.Recognizer()
    with sr.AudioFile(arquivo) as source:
        audio = recognizer.record(source)  # Lê o áudio do arquivo
    try:
        texto = recognizer.recognize_google(audio, language="pt-BR")
        st.write("Você disse: " + texto)
        return texto
    except sr.UnknownValueError:
        st.write("Google Speech Recognition não entendeu o áudio")
        return None
    except sr.RequestError as e:
        st.write(f"Erro ao conectar ao serviço de reconhecimento: {e}")
        return None


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








































