from numpy import log10
import pandas as pd 
from csv import QUOTE_ALL

class BoletimDeUrna:
    _arquivo = []
    _colunasPadrao = ["SG_UF", "NM_VOTAVEL", "QT_VOTOS"]
    _colunas = []
    _cabecalho = True
    _codificacao = "ISO-8859-1"
    _delimitador = ";"
    _boletimDeUrna = None

    """
        Args:
            arquivo (list): lista com o caminho para cada arquivo do boletim de urnas.
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
    """
    def __init__(self, arquivo, colunas, filtro, cabecalho = True, codificacao = "ISO-8859-1", delimitador = ";"):
        self._arquivo = arquivo
        self._colunas = colunas
        self._filtro = filtro
        self._cabecalho = cabecalho
        self._codificacao = codificacao
        self._delimitador = delimitador
        self._boletimDeUrna = pd.DataFrame(
            columns = self._colunasPadrao
        )

    def apurar(self, agrupamento = ["SG_UF", "NM_VOTAVEL"]):
        """
        Determina a quantidade de votos recebido por cada candidato em cada município
        no arquivo.
        """
        # try:
        self._colunasPadrao = agrupamento.copy()
        self._colunasPadrao.append("QT_VOTOS")
        self._boletimDeUrna = pd.DataFrame(
            columns = self._colunasPadrao
        )
        for arq in self._arquivo:
            print(f"Apurando: {arq}")
            if(self._cabecalho):
                buAux = pd.read_csv(arq, encoding = self._codificacao, delimiter = self._delimitador)
                buAux = buAux[buAux.columns[list(self._colunas.values())]]
            else:
                buAux = pd.read_csv(arq, encoding = self._codificacao, delimiter = self._delimitador, header = None)
                buAux = buAux[self._colunas.values()]

            buAux.columns = [col.replace(" ", "") for col in buAux.columns]

            if("NR_TURNO" in self._filtro.keys()):
                buAux = buAux.loc[(buAux["DS_CARGO_PERGUNTA"] == self._filtro["DS_CARGO_PERGUNTA"]) & (buAux["NR_TURNO"] == self._filtro["NR_TURNO"])]
            else:
                buAux = buAux.loc[buAux["DS_CARGO_PERGUNTA"] == self._filtro["DS_CARGO_PERGUNTA"]]

            if(len(buAux) > 0):
                buAux = buAux.groupby(agrupamento)["QT_VOTOS"].sum().reset_index()
                buAux["NM_VOTAVEL"] = buAux["NM_VOTAVEL"].apply(lambda nome: nome.upper())
                self._boletimDeUrna = pd.concat([self._boletimDeUrna, buAux])

            print(f"Total de registros encontrados: {len(buAux)}\n")

        # except:
        #     print("Alguma coisa deu errado ao processar o arquivo.")

    def frequenciaAbsoluta(self):
        """
        Determina a frequência absoluta dos dígitos de 1 a 9 no primeiro dígito da quantidade
        de votos recebido por um candidato em cada município do Brasil.

        Args:
            boletimDeUrna (DataFrame): data frame com a apuração dos votos do boletim de urna.

        Returns:
            fqrel (DataFrame): a frequência absoluta dos dígitos de 1 a 9 no primeiro dígito da
            quantidade de votos recebido por um candidato.
        """
        buAux = self._boletimDeUrna.copy()
        buAux["QT_VOTOS"] = buAux["QT_VOTOS"].astype(str)
        buAux["PRIMEIRO_DIGITO"] = buAux["QT_VOTOS"].apply(lambda x: x[0])
        nomeVotavel = filter(None, buAux["NM_VOTAVEL"].unique())
        digitos = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        frequencia = {}
        for nome in nomeVotavel:
            frequencia[nome] = 9*[0]
            for i in range(9):
                frequencia[nome][i] = ((buAux["NM_VOTAVEL"] == nome) & (buAux["PRIMEIRO_DIGITO"] == digitos[i])).sum()

        fqabs = pd.DataFrame(frequencia)
        return fqabs

    def frequenciaRelativa(self):
        """
        Determina a frequência absoluta dos dígitos de 1 a 9 no primeiro dígito da quantidade
        de votos recebido por um candidato em cada município do Brasil.

        Returns:
            feq (DataFrame): a frequência absoluta dos dígitos de 1 a 9 no primeiro dígito da
            quantidade de votos recebido por um candidato.
        """
        fqrel = self.frequenciaAbsoluta()
        colunas = fqrel.columns
        for coluna in colunas:
            total = fqrel[coluna].sum()
            fqrel[coluna] = 100.0*fqrel[coluna]/total

        return fqrel

    def grafico(self, nomeDoVotavel, arquivo, titulo):
        fqrel = self.frequenciaRelativa()
        f = fqrel.copy()
        f["LEI DE BENFORD"] = [100.0*(log10(x + 1) - log10(x)) for x in range(1, 10)]
        ax = f.plot.line(x = "DÍGITO", y = nomeDoVotavel[0], xlabel = "DÍGITO", ylabel = "FREQUÊNCIA (%)", title = titulo, rot = 0, linestyle = "-", marker = "o", figsize = (10, 8))
        for nome in nomeDoVotavel[1:]:
            f.plot.line(x = "DÍGITO", y = nome, rot = 0, linestyle = "-", marker = "o", ax = ax)

        f.plot.line(x = "DÍGITO", y = "LEI DE BENFORD", rot = 0, linestyle = "-", marker = "o", color = "black", ax = ax)
        ax.figure.savefig(arquivo)

    def dividirArquivo(self, arquivo, numeroDeLinhas, prefixoDaSaida):
        try:
            arquivoOriginal = open(arquivo, "r", encoding = self._codificacao)
            parte = 1
            print(f"Criando arquivo: {prefixoDaSaida}{parte}.csv")
            arquivoParte = open(f"{prefixoDaSaida}{parte}.csv", "w", encoding = self._codificacao)
            lin = 0
            cab = ""
            for linha in arquivoOriginal:
                if(self._cabecalho and parte == 1):
                    cab = linha

                arquivoParte.write(linha)
                lin += 1
                if(lin >= numeroDeLinhas):
                    parte += 1
                    print(f"Criando arquivo: {prefixoDaSaida}{parte}.csv")
                    arquivoParte.close()
                    arquivoParte = open(f"{prefixoDaSaida}{parte}.csv", "w", encoding = self._codificacao)
                    if(self._cabecalho):
                        arquivoParte.write(cab)
                        lin = 1
                    else:
                        lin = 0

            arquivoOriginal.close()
            arquivoParte.close()
        except:
            print("Alguma coisa deu errado ao processar os arquivos.")
    
    def salvar(self, arquivo):
        try:
            self._boletimDeUrna.to_csv(
                arquivo,
                sep = self._delimitador,
                header = True,
                index = False,
                quoting = QUOTE_ALL,
                encoding = self._codificacao
            )
        except:
            print(f"Alguma coisa deu errado ao processar o arquivo {arquivo}.")

    def transferirVoto(self, votavelOrigem, votavelDestino, quantidadeDeVotos):
        #@todo
        return None