import streamlit as st
import numpy as np

st.set_page_config('Testes em Ar Condiciionado', page_icon=':test_tube:')


# Função para carregar as instruções de teste a partir de um arquivo txt
def carregar_instrucoes(teste_selecionado):
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



with st.sidebar:
    st.title('Selecione os dados')
    fabricante = st.selectbox('Fabricante', ['selecione...', 'LG', 'MIDEA'])
    modelo = st.selectbox('Modelo', ['selecione...', 'Hi Wall', 'Teto', 'Cassete'])
    tipo_teste = st.selectbox('Tipo de Teste', ['selecione...', 'Aparelho não liga','Compressão do compressor', 'Comunicação entre as unidades', 'Motoventilador da Condensadora Convencional', 'Motoventilador da Condensadora Inverter', 'Motoventilador da Evaporadora', 'Rendimento do Aparelho', 'Sensores', 'Superaquecimento','Teste de Compressor Inverter', 'Válvula Reversora'])
    

st.title('**Testes em Ar Condicionado** :male-mechanic:')   
st.write('''
             Obs.: Para os testes é necessário ter os seguintes instrumentos:  
             1. Multímetro
             2. Alicate Amperímetro
             3. Conjunto Manifold
             ''')

# Carregar instruções para o teste selecionado
if fabricante != 'selecione...':  # Verifica se um fabricante foi selecionado
    instrucoes = carregar_instrucoes(tipo_teste)
    
    if instrucoes:  # Se houver instruções a serem exibidas
        st.subheader(f'Teste: {tipo_teste}')
        
        # Formatar e exibir as instruções, garantindo que as quebras de linha sejam respeitadas
        st.markdown(instrucoes.replace("\n", "<br>"), unsafe_allow_html=True)  # Exibe as instruções carregadas
    else:
        st.warning("Por favor, selecione um tipo de teste válido.")
else:
    st.warning("Por favor, selecione um fabricante.")

