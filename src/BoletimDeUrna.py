from numpy import fabs, log10
from scipy import stats
from csv import QUOTE_ALL
import pandas as pd

class BoletimDeUrna:
    _leiDeBenford = []
    _boletimDeUrna = None

    def __init__(self, arquivo = None, cabecalho = True, delimitador = ";", codificacao = "ISO-8859-1"):
        if(arquivo is not None):
            self.abrir(arquivo, cabecalho, delimitador, codificacao)

        self._leiDeBenford = [(log10(d + 1) - log10(d)) for d in range(1, 10)]

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
        Determina a frequência absoluta dos algarismos de 1 a 9 no primeiro dígito da quantidade
        de votos recebido por um candidato em cada município do Brasil.

        Args:
            boletimDeUrna (DataFrame): data frame com a apuração dos votos do boletim de urna.

        Returns:
            fqrel (DataFrame): a frequência absoluta dos algarismos de 1 a 9 no primeiro dígito da
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

    def ordemDeGrandeza(self):
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

    def erroRelativo(self, frequenciaAbsoluta, frequenciaEsperada):
        erroRelativo = [frequenciaAbsoluta[i]/frequenciaEsperada[i] - 1.0 for i in range(len(frequenciaAbsoluta))]
        return erroRelativo

    """
        Gera o arquivo com o gráfico da frequência absoluta juntamente com a 
        curva da lei de Benford.

        Argumento:
            frequenciaAbsoluta (list): lista com a frequência absoluta dos
            dígitos de 1 até 9 na amostra de dados.
            nomeDoArquivo (str): caminho do arquivo.
            titulo (str): título do gráfico.
            cores (list): lista com os códigos hexadecimais das cores usadas
            no gráfico.
        Retorno:
            Nenhum retorno de variável. Gera o arquivo com o gráfico desejado.
    """
    def grafico(self, nomeDoVotante, nomeDoArquivo, titulo, cores = ["#009c3b", "#002776"]):
        frequenciaAbsoluta = self.frequenciaAbsoluta()
        fqAbs = {
            nomeDoVotante : list(frequenciaAbsoluta[nomeDoVotante])
        }
        fqAbs["PRIMEIRO DIGITO"] = range(1, 10)
        total = sum(fqAbs[nomeDoVotante])
        fqAbs["LEI DE BENFORD"] = [total*self._leiDeBenford[i] for i in range(9)]
        fqAbs = pd.DataFrame(fqAbs)

        ax = fqAbs.plot(
            x = "PRIMEIRO DIGITO",
            y = "LEI DE BENFORD",
            xlabel = "PRIMEIRO DÍGITO",
            ylabel = "FREQUÊNCIA ABSOLUTA",
            title = titulo,
            rot = 0,
            marker = "o",
            color = cores[0],
            figsize = (10, 8),
            use_index = False
        )

        fqAbs.plot(
            x = "PRIMEIRO DIGITO",
            y = nomeDoVotante,
            label = nomeDoVotante,
            rot = 0,
            color = cores[1],
            kind = "bar",
            ax = ax
        )

        ax.figure.savefig(nomeDoArquivo)
        ax.close()

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
        #@todo Implementar
        return None