import pandas as pd
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from os import environ
import sqlalchemy

load_dotenv(find_dotenv())

def validar_planilha(data_frame: pd.DataFrame) -> None:
    colunas_esperadas = ['Vendedor', 'Nome', 'Data Compra', 'Mês', 'Data Devolução', 'Unidade',
       'Série', 'Número', 'Pedido', 'Romaneio', 'Frete', 'Código Cliente',
       'Rede', 'Razão Social', 'Tipo de Cliente', 'Rota Cliente',
       'Rota Pedido', 'Cidade', 'UF', 'Ramo Ativ.', 'Código Produto',
       'Descrição Produto', 'Unidade Produto', 'Família', 'CFOP', 'Descrição',
       'Volumes', 'Peso', 'Lista', 'Ocorr', 'Pre.Base', 'Preço Praticado',
       'Valor Produto', 'Desconto Comercial', 'Valor Total Faturado', 'Desc.',
       'Nota Refaturada', 'Romaneio Refaturada', 'Nota Devolução',
       'Cliente Original', 'Cond. Pag. Cliente', 'Cond. Pag. Nota']
    
    if data_frame.empty:
        raise ValueError('Planilha Vazia')

    if list(data_frame.columns) != colunas_esperadas:
        raise TypeError('Colunas Incompatíveis')
    
    if not pd.api.types.is_datetime64_any_dtype(data_frame['Data Compra']):
        raise TypeError('A coluna Data Compra não é do tipo datetime.')

    if not pd.api.types.is_datetime64_any_dtype(data_frame['Data Devolução']):
        raise TypeError('A coluna Data Devolução não é do tipo datetime.')
    
def filtrar_novos_dados(data_frame: pd.DataFrame) -> pd.DataFrame:
    url_db = environ.get('URL_DB')
    conn = sqlalchemy.create_engine(url_db)
    query = 'SELECT numero FROM relatorios_avinor;'
    pedidos_registrados = pd.read_sql_query(query, conn)

    df_filtrado = data_frame[~data_frame['Número'].isin(pedidos_registrados.numero)]
    
    return df_filtrado

def formatar_df(df_original: pd.DataFrame) -> pd.DataFrame:
    data_frame = df_original.copy()

    data_frame.columns = ['vendedor', 'nome', 'data_compra', 'mes', 'data_devolucao', 'unidade',
       'serie', 'numero', 'pedido', 'romaneio', 'frete', 'codigo_cliente',
       'rede', 'razao_social', 'tipo_de_cliente', 'rota_cliente',
       'rota_pedido', 'cidade', 'uf', 'ramo_ativ', 'codigo_produto',
       'descricao_produto', 'unidade_produto', 'familia', 'cfop', 'descricao',
       'volumes', 'peso', 'lista', 'ocorr', 'prebase', 'preco_praticado',
       'valor_produto', 'desconto_comercial', 'valor_total_faturado', 'desc',
       'nota_refaturada', 'romaneio_refaturada', 'nota_devolucao',
       'cliente_original', 'cond_pag_cliente', 'cond_pag_nota']
    
    vendedores_ativos = [2, 13, 36, 784, 1003, 1008, 1014, 1038, 1040, 1054, 1063]
    data_frame['status_vendedor'] = 'inativo'

    data_frame.loc[data_frame['vendedor'].isin(vendedores_ativos), 'status_vendedor'] = 'ativo'

    return data_frame

def adicionar_registros(novos_dados: pd.DataFrame) -> None:
    url_db = environ.get('URL_DB')
    conn = sqlalchemy.create_engine(url_db)  
    novos_dados.to_sql('relatorios_avinor', conn, if_exists='append', index=False)