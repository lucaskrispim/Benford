from numpy import log10
import pandas as pd 
from pandas.core.frame import DataFrame

def apurar(arquivo, colunas, filtro, cabecalho = True, codificacao = "ISO-8859-1"):
    """
    Determina a quantidade de votos recebido por cada candidato em cada município
    no arquivo.

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
        df (DataFrame): data frame com a quantidade de votos recebido por cada
        candidato em cada município no arquivo
    """
    try:
        if(cabecalho):
            dfAux = pd.read_csv(arquivo, encoding = codificacao, delimiter=';')
            df = dfAux[dfAux.columns[list(colunas.values())]].copy()
        else:
            dfAux = pd.read_csv(arquivo, encoding = codificacao, delimiter=';', header = None)
            df = dfAux[colunas.values()].copy()

        df.columns = colunas.keys()
        if('NR_TURNO' in filtro.keys()):
            df = df.loc[(df['DS_CARGO_PERGUNTA'] == filtro['DS_CARGO_PERGUNTA']) & (df['NR_TURNO'] == filtro['NR_TURNO'])]
        else:
            df = df[df['DS_CARGO_PERGUNTA'] == filtro['DS_CARGO_PERGUNTA']]

        df = df.groupby(['NM_MUNICIPIO',"NM_VOTAVEL"])['QT_VOTOS'].sum().reset_index().copy()
        df["NM_VOTAVEL"] = df["NM_VOTAVEL"].apply(lambda nome: nome.upper())
        return df
    except:
        print("Alguma coisa deu errado ao processar o arquivo.")

def freqabs(df):
    """
    Determina a frequência absoluta dos dígitos de 1 a 9 no primeiro dígito da quantidade
    de votos recebido por um candidato em cada município do Brasil.

    Args:
        df (DataFrame): data frame com a apuração dos votos do boletim de urna.

    Returns:
        feq (DataFrame): a frequência absoluta dos dígitos de 1 a 9 no primeiro dígito da
        quantidade de votos recebido por um candidato.
    """
    dfAux = df.copy()
    dfAux["QT_VOTOS"] = dfAux['QT_VOTOS'].astype(str)
    dfAux["PRIMEIRO_DIGITO"] = dfAux['QT_VOTOS'].apply(lambda x: x[0])
    nomeVotavel = filter(None, dfAux["NM_VOTAVEL"].unique())
    digitos = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    frequencia = {}
    for nome in nomeVotavel:
        frequencia[nome] = 9*[0]
        for i in range(9):
            frequencia[nome][i] = ((dfAux["NM_VOTAVEL"] == nome) & (dfAux["PRIMEIRO_DIGITO"] == digitos[i])).sum()
    freq = DataFrame(frequencia)
    return freq

def gerarGrafico(frel, nomeDoVotavel, arquivo, titulo):
    f = frel.copy()
    f["LEI DE BENFORD"] = [100.0*(log10(x + 1) - log10(x)) for x in range(1, 10)]
    ax = f.plot.line(x = "DÍGITO", y = nomeDoVotavel[0], xlabel = "DÍGITO", ylabel = "FREQUÊNCIA (%)", title = titulo, rot = 0, linestyle = "-", marker = "o", figsize = (10, 8))
    for nome in nomeDoVotavel[1:]:
        f.plot.line(x = "DÍGITO", y = nome, rot = 0, linestyle = "-", marker = "o", ax = ax)

    f.plot.line(x = "DÍGITO", y = "LEI DE BENFORD", rot = 0, linestyle = "-", marker = "o", color = "black", ax = ax)
    ax.figure.savefig(arquivo)
    return None

def freqrel(df):
    """
    Determina a frequência absoluta dos dígitos de 1 a 9 no primeiro dígito da quantidade
    de votos recebido por um candidato em cada município do Brasil.

    Args:
        df (DataFrame): data frame com a apuração dos votos do boletim de urna.

    Returns:
        feq (DataFrame): a frequência absoluta dos dígitos de 1 a 9 no primeiro dígito da
        quantidade de votos recebido por um candidato.
    """
    feq = freqabs(df.copy())
    cols = feq.columns
    for col in cols:
        total = feq[col].sum()
        feq[col] = 100.0*feq[col]/total

    return feq

def dividirArquivo(nomeDoArquivo, quantidadeDeLinhas, prefixoDaSaida, cabecalho = True, codificacao = "ISO-8859-1"):
    try:
        arquivo = open(nomeDoArquivo, "r", encoding = codificacao)
        print(f"Criando arquivo: {prefixoDaSaida}1.csv")
        arquivoAux = open(f"{prefixoDaSaida}1.csv", "w", encoding = codificacao)
        lin = 0
        parte = 1
        cab = ""
        for linha in arquivo:
            if(cabecalho and len(cab) == 0):
                cab = linha
            arquivoAux.write(linha)
            lin += 1
            if(lin >= quantidadeDeLinhas):
                arquivoAux.close()
                parte += 1
                print(f"Criando arquivo: {prefixoDaSaida}{parte}.csv")
                arquivoAux = open(f"{prefixoDaSaida}{parte}.csv", "w", encoding = codificacao)
                if(cabecalho):
                    arquivoAux.write(cab)
                    lin = 1
                else:
                    lin = 0

        arquivo.close()
        arquivoAux.close()
    except:
        print("Alguma coisa deu errado ao processar o arquivo.")