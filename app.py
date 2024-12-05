import streamlit as st
import upload as up
import pandas as pd

def page_upload():
    col1, col2 = st.columns(2, gap='large')

    with col1:
        st.header("Enviar dados para Banco")
        st.divider()
        arquivos = st.file_uploader('Planilhas', ['xlsx'], accept_multiple_files=True)
        botao = st.button('Enviar')

    with col2:
        st.header('Logs')
        st.divider()
        if arquivos and botao:
            for arquivo in arquivos:
                st.markdown(f'### -> {arquivo.name}')
                progresso = st.progress(0, 'Lendo arquivo...')

                try: 
                    data_frame = pd.read_excel(arquivo)
                except:
                    progresso.empty()
                    st.error('Erro ao abrir arquivo')
                    continue
                
                progresso.progress(1/5, 'Validando planilha...')

                try:
                    up.validar_planilha(data_frame)
                except Exception as e:
                    progresso.empty()
                    st.error(f'Planilha inválida. Erro: {e}')
                    continue

                progresso.progress(2/5, 'Filtrando Registros...')

                try:
                    novos_dados = up.filtrar_novos_dados(data_frame)
                except Exception as e:
                    progresso.empty()
                    st.error(f'Erro ao se conectar ao banco de dados. Error: {e}')
                    continue

                if novos_dados.empty:
                    progresso.empty()
                    st.warning('Não há dados novos na planilha')
                    continue
                    
                progresso.progress(3/5, 'Formatando Planilha...')
                try: 
                    df_formatado = up.formatar_df(novos_dados)
                except Exception as e:
                    progresso.empty()
                    st.error(f'Erro ao formatar planilha: {e}')
                    continue

                progresso.progress(4/5, 'Enviando Dados...')

                try:
                    up.adicionar_registros(df_formatado)
                    progresso.progress(5/5, 'Finalizado!')
                    progresso.empty()
                    st.success(f'Base de dados atualizada com sucesso! {len(df_formatado)} registros adicionados')
                except Exception as e:
                    progresso.empty()
                    st.warning(f'Houve um erro ao enviar dados. Erro: {e}')
                    continue

def main():
    st.set_page_config(layout='wide')
    page_upload()

if __name__ == "__main__":
    main()