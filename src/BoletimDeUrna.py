from numpy import log10
from scipy import stats
from csv import QUOTE_ALL
import pandas as pd

class BoletimDeUrna:
    _leiDeBenford = []
    _boletimDeUrna = None

    def __init__(self, arquivo = None, cabecalho = True, delimitador = ";", codificacao = "ISO-8859-1"):
        if(arquivo is not None):
            self.abrir(arquivo, cabecalho, delimitador, codificacao)

        self._leiDeBenford = [100.0*(log10(d + 1) - log10(d)) for d in range(1, 10)]
        self._frequenciaEsperada = self._leiDeBenford[0:8]
        self._frequenciaEsperada[7] += self._leiDeBenford[8]

    def apurar(self, arquivos, colunas, filtro, agrupamento = ["SG_UF", "NM_VOTAVEL"], cabecalho = True, delimitador = ";", codificacao = "ISO-8859-1"):
        """
        Determina a quantidade de votos recebido por cada candidato em cada município
        no arquivo.
        """
        try:
            colunasPadrao = agrupamento.copy()
            colunasPadrao.append("QT_VOTOS")
            self._boletimDeUrna = pd.DataFrame(
                columns = colunasPadrao
            )
            for arq in arquivos:
                print(f"Apurando: {arq}")
                if(cabecalho):
                    buAux = pd.read_csv(arq, encoding = codificacao, delimiter = delimitador)
                    buAux = buAux[buAux.columns[list(colunas.values())]]
                else:
                    buAux = pd.read_csv(arq, encoding = codificacao, delimiter = delimitador, header = None)
                    buAux = buAux[colunas.values()]

                buAux.columns = [col.replace(" ", "") for col in buAux.columns]

                if("NR_TURNO" in filtro.keys()):
                    buAux = buAux.loc[(buAux["DS_CARGO_PERGUNTA"] == filtro["DS_CARGO_PERGUNTA"]) & (buAux["NR_TURNO"] == filtro["NR_TURNO"])]
                else:
                    buAux = buAux.loc[buAux["DS_CARGO_PERGUNTA"] == filtro["DS_CARGO_PERGUNTA"]]

                if(len(buAux) > 0):
                    buAux = buAux.groupby(agrupamento)["QT_VOTOS"].sum().reset_index()
                    buAux["NM_VOTAVEL"] = buAux["NM_VOTAVEL"].apply(lambda nome: nome.upper())
                    self._boletimDeUrna = pd.concat([self._boletimDeUrna, buAux])

                print(f"Total de registros encontrados: {len(buAux)}\n")

            return self._boletimDeUrna
        except:
            print("Alguma coisa deu errado ao processar o arquivo.")

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
        for coluna in fqrel.columns:
            total = fqrel[coluna].sum()
            fqrel[coluna] = 100.0*fqrel[coluna]/total

        return fqrel

    def orderDeGrandeza(self):
        nomeDoVotavel = self._boletimDeUrna["NM_VOTAVEL"].unique()
        ordemDeGrandeza = {}
        for nome in nomeDoVotavel:
            votos = self._boletimDeUrna.loc[self._boletimDeUrna["NM_VOTAVEL"] == nome]
            minimo = votos["QT_VOTOS"].min()
            maximo = votos["QT_VOTOS"].max()
            diferenca = maximo - minimo
            odg = 0
            while(diferenca >= 10.0):
                diferenca /= 10.0
                odg += 1

            ordemDeGrandeza[nome] = {
                "minimo" : minimo,
                "maximo" : maximo,
                "ordem" : odg
            }

        return(ordemDeGrandeza)

    def testeDeAderencia(self, alfa = 0.05):
        grauDeLiberdade = len(self._frequenciaEsperada) - 1
        nivelDeConfianca = 1 - alfa
        chi2Critico = stats.chi2.ppf(nivelDeConfianca, grauDeLiberdade)
        frequenciaRelativa = self.frequenciaRelativa()
        testeDeAderencia = {
            "chi2Critico" : chi2Critico,
            "alfa" : alfa,
            "grauDeLiberdade" : grauDeLiberdade,
            "NM_VOTAVEL" : {}
        }
        for nome in frequenciaRelativa.columns:
            fqrel = list(frequenciaRelativa[nome])
            frequenciaObservada = fqrel[0:8]
            frequenciaObservada[7] += fqrel[8]
            chi2, p = stats.chisquare(frequenciaObservada, self._frequenciaEsperada)
            testeDeAderencia["NM_VOTAVEL"][nome] = {
                "teste" : (chi2 < chi2Critico),
                "chi2" : chi2,
                "p" : p
            }

        return testeDeAderencia

    def grafico(self, nomeDoVotavel, arquivo, titulo):
        fqrel = self.frequenciaRelativa(self._boletimDeUrna)
        f = fqrel.copy()
        f["LEI DE BENFORD"] = self._leiDeBenford
        ax = f.plot.line(x = "DÍGITO", y = nomeDoVotavel[0], xlabel = "DÍGITO", ylabel = "FREQUÊNCIA (%)", title = titulo, rot = 0, linestyle = "-", marker = "o", figsize = (10, 8))
        for nome in nomeDoVotavel[1:]:
            f.plot.line(x = "DÍGITO", y = nome, rot = 0, linestyle = "-", marker = "o", ax = ax)

        f.plot.line(x = "DÍGITO", y = "LEI DE BENFORD", rot = 0, linestyle = "-", marker = "o", color = "black", ax = ax)
        ax.figure.savefig(arquivo)

    def dividirArquivo(self, arquivo, numeroDeLinhas, prefixoDaSaida, codificacao = "ISO-8859-1"):
        try:
            arquivoOriginal = open(arquivo, "r", encoding = codificacao)
            parte = 1
            print(f"Criando arquivo: {prefixoDaSaida}{parte}.csv")
            arquivoParte = open(f"{prefixoDaSaida}{parte}.csv", "w", encoding = codificacao)
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
                    arquivoParte = open(f"{prefixoDaSaida}{parte}.csv", "w", encoding = codificacao)
                    if(self._cabecalho):
                        arquivoParte.write(cab)
                        lin = 1
                    else:
                        lin = 0

            arquivoOriginal.close()
            arquivoParte.close()
        except:
            print(f"Alguma coisa deu errado ao dividir o arquivo {arquivo}.")

    def abrir(self, arquivo, cabecalho = True, delimitador = ";", codificacao = "ISO-8859-1"):
        try:
            if(cabecalho):
                self._boletimDeUrna = pd.read_csv(arquivo, encoding = codificacao, delimiter = delimitador)
            else:
                self._boletimDeUrna = pd.read_csv(arquivo, encoding = codificacao, delimiter = delimitador, header = None)

            # self._boletimDeUrna["QT_VOTOS"] = self._boletimDeUrna["QT_VOTOS"].astype(int64)
        except:
            print(f"Alguma coisa deu errado ao abrir o arquivo {arquivo}.")

    def salvar(self, arquivo, cabecalho = True, delimitador = ";", codificacao = "ISO-8859-1"):
        try:
            self._boletimDeUrna.to_csv(
                arquivo,
                sep = delimitador,
                header = cabecalho,
                index = False,
                quoting = QUOTE_ALL,
                encoding = codificacao
            )
        except:
            print(f"Alguma coisa deu errado ao salvar o arquivo {arquivo}.")

    def transferirVoto(self, votavelOrigem, votavelDestino, quantidadeDeVotos):
        municipios = self._boletimDeUrna["NM_MUNICIPIO"].unique()
        estados = self._boletimDeUrna["SG_UF"].unique()
        votaveis = self._boletimDeUrna["NM_VOTAVEL"].unique()
        print(municipios, estados, votaveis)