import pandas as pd 
import csv

from pandas.core.frame import DataFrame

def freqabs(nomeDoArquivo, colunas, filtro, cabecalho = True, codificacao = "ISO-8859-1"):
    """
    Determina a frequência absoluta dos dígitos de 1 a 9 no primeiro dígito da quantidade
    de votos recebido por um candidato em cada município do Brasil.

    Args:
        nomeDoArquivo (string): caminho do arquivo do boletim de urnas.
        colunas (dict): dicionário com a posição no arquivo do boletim de urnas
            das colunas "número do turno" (NR_TURNO), "descrição do cargo/pergunta"
            (DS_CARGO_PERGUNTA), "nome do município" (NM_MUNICIPIO), "nome do votável"
            (NM_VOTAVEL) e "quantidade de votos" (QT_VOTOS).
        filtro (dict): dicionário com o valor do "número de turno" (NR_TURNO) e da
            "descrição do cargo/pergunta" (DS_CARGO_PERGUNTA). Se o arquivo do boletim
            de urnas apenas tiver um número de turno, então o valor de NR_TURNO
            não precisa ser informado.
        cabecalho (bool, optional): informa se o arquivo do boletim de urnas tem
            um cabeçalho na primeira linha. O padrão é True.
        codificacao (str, optional): codificação dos caracteres no arquivo do boletim
            de urnas. O padrão é "ISO-8859-1".

    Returns:
        fa: a frequência absoluta dos dígitos de 1 a 9 no primeiro dígito da
        quantidade de votos recebido por um candidato.
    """
    fa = DataFrame(lerarquivo(nomeDoArquivo, colunas, filtro, cabecalho, codificacao))
    return fa

def freqrel(nomeDoArquivo, colunas, filtro, cabecalho = True, codificacao = "ISO-8859-1"):
    """
    Determina a frequência relativa dos dígitos de 1 a 9 no primeiro dígito da quantidade
    de votos recebido por um candidato em cada município do Brasil.

    Args:
        nomeDoArquivo (string): caminho do arquivo do boletim de urnas.
        colunas (dict): dicionário com a posição no arquivo do boletim de urnas
            das colunas "número do turno" (NR_TURNO), "descrição do cargo/pergunta"
            (DS_CARGO_PERGUNTA), "nome do município" (NM_MUNICIPIO), "nome do votável"
            (NM_VOTAVEL) e "quantidade de votos" (QT_VOTOS).
        filtro (dict): dicionário com o valor do "número de turno" (NR_TURNO) e da
            "descrição do cargo/pergunta" (DS_CARGO_PERGUNTA). Se o arquivo do boletim
            de urnas apenas tiver um número de turno, então o valor de NR_TURNO
            não precisa ser informado.
        cabecalho (bool, optional): informa se o arquivo do boletim de urnas tem
            um cabeçalho na primeira linha. O padrão é True.
        codificacao (str, optional): codificação dos caracteres no arquivo do boletim
            de urnas. O padrão é "ISO-8859-1".

    Returns:
        fr: a frequência relativa dos dígitos de 1 a 9 no primeiro dígito da
        quantidade de votos recebido por um candidato.
    """
    fr = DataFrame(lerarquivo(nomeDoArquivo, colunas, filtro, cabecalho, codificacao))
    cols = fr.columns
    for col in cols:
        total = fr[col].sum()
        fr[col] = 100.0*fr[col]/total

    return fr

def lerarquivo(nomeDoArquivo, colunas, filtro, cabecalho = True, codificacao = "ISO-8859-1"):
    """
    Determina a frequência absoluta dos dígitos de 1 a 9 no primeiro dígito da quantidade
    de votos recebido por um candidato em cada município do Brasil.

    Args:
        nomeDoArquivo (string): caminho do arquivo do boletim de urnas.
        colunas (dict): dicionário com a posição no arquivo do boletim de urnas
        das colunas "número do turno" (NR_TURNO), "descrição do cargo/pergunta"
        (DS_CARGO_PERGUNTA), "nome do município" (NM_MUNICIPIO), "nome do votável"
        (NM_VOTAVEL) e "quantidade de votos" (QT_VOTOS).
        filtro (dict): dicionário com o valor do "número de turno" (NR_TURNO) e da
        "descrição do cargo/pergunta" (DS_CARGO_PERGUNTA). Se o arquivo do boletim
        de urnas apenas tiver um número de turno, então o valor de NR_TURNO
        não precisa ser informado.
        cabecalho (bool, optional): informa se o arquivo do boletim de urnas tem
        um cabeçalho na primeira linha. O padrão é True.
        codificacao (str, optional): codificação dos caracteres no arquivo do boletim
        de urnas. O padrão é "ISO-8859-1".

    Returns:
        [DataFrame]: a frequência absoluta dos dígitos de 1 a 9 no primeiro dígito da
        quantidade de votos recebido por um candidato.
    """
    try:
        if(cabecalho):
            dfAux = pd.read_csv(nomeDoArquivo, encoding = codificacao, delimiter=';')
            df = dfAux[dfAux.columns[list(colunas.values())]].copy()
        else:
            dfAux = pd.read_csv(nomeDoArquivo, encoding = codificacao, delimiter=';', header = None)
            df = dfAux[colunas.values()].copy()

        df.columns = colunas.keys()
        if('NR_TURNO' in filtro.keys()):
            df = df.loc[(df['DS_CARGO_PERGUNTA'] == filtro['DS_CARGO_PERGUNTA']) & (df['NR_TURNO'] == filtro['NR_TURNO'])]
        else:
            df = df[df['DS_CARGO_PERGUNTA'] == filtro['DS_CARGO_PERGUNTA']]

        df["QT_VOTOS"] = pd.to_numeric(df["QT_VOTOS"])
        df = df.groupby(['NM_MUNICIPIO','NM_VOTAVEL'])['QT_VOTOS'].sum().reset_index().copy()
        df["QT_VOTOS"] = df['QT_VOTOS'].astype(str)
        df['PRIMEIRO_DIGITO'] = df['QT_VOTOS'].apply(lambda x: x[0])
        nomeVotavel = filter(None, df['NM_VOTAVEL'].unique())
        digitos = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        frequencia = {}
        for nome in nomeVotavel:
            frequencia[nome] = 9*[0]
            for i in range(9):
                frequencia[nome][i] = ((df['NM_VOTAVEL'] == nome) & (df['PRIMEIRO_DIGITO'] == digitos[i])).sum()

        return frequencia
    except:
        print("Alguma coisa deu errado ao processar o arquivo.")