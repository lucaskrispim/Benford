from numpy import log10
import csv
import pandas as pd

class BoletimDeUrna:
    _delimitador = ";"
    _codificacao = "ISO-8859-1"
    _cabecalho = True
    _leiDeBenford = []
    _boletimDeUrna = None

    def __init__(self, arquivo = None, cabecalho = True, delimitador = ";", codificacao = "ISO-8859-1"):
        """
            Inicialização do objeto.

            Argumentos:
                arquivos (list): caminho dos arquivos de boletim de urnas.
                cabecalho (bool, optional): informa se o arquivo do boletim de urnas tem
                um cabeçalho na primeira linha. O padrão é True.
                delimitador (string): caracter que separa as colunas no arquivo do boletim 
                de urnas.
                codificacao (str, optional): codificação dos caracteres no arquivo do boletim
                de urnas. O padrão é "ISO-8859-1".
        """
        if(arquivo is not None):
            self.abrir(arquivo, cabecalho, delimitador, codificacao)
            self._delimitador = delimitador
            self._codificacao = codificacao
            self._cabecalho = cabecalho

        self._leiDeBenford = [(log10(d + 1) - log10(d)) for d in range(1, 10)]

    def apurar(self, arquivos, colunas, filtro, agrupamento = ["SG_UF", "NM_VOTAVEL"], cabecalho = True, delimitador = ";", codificacao = "ISO-8859-1"):
        """
        Determina a quantidade de votos recebido por cada candidato em cada município
        no arquivo.

        Argumentos:
            arquivos (list): caminho dos arquivos de boletim de urnas.
            colunas (dict): dicionário com a posição no arquivo do boletim de urnas
            das colunas "número do turno" (NR_TURNO), "descrição do cargo/pergunta"
            (DS_CARGO_PERGUNTA), "nome do município" (NM_MUNICIPIO), "nome do votável"
            (NM_VOTAVEL), "quantidade de votos" (QT_VOTOS), "número da zona" (NR_ZONA) e 
            "número da seção" (NR_SECAO).
            filtro (dict): dicionário com o valor do "número de turno" (NR_TURNO) e da
            "descrição do cargo/pergunta" (DS_CARGO_PERGUNTA). Se o arquivo do boletim
            de urnas apenas tiver um número de turno, então o valor de NR_TURNO
            não precisa ser informado.
            agrupamento (list): colunas que devem ser agrupadas.
            cabecalho (bool, optional): informa se o arquivo do boletim de urnas tem
            um cabeçalho na primeira linha. O padrão é True.
            delimitador (string): caracter que separa as colunas no arquivo do boletim 
            de urnas.
            codificacao (str, optional): codificação dos caracteres no arquivo do boletim
            de urnas. O padrão é "ISO-8859-1".

        Retorno:
            self._boletimDeUrna (DataFrame): data frame com a quantidade de votos recebido por cada
            candidato no arquivo.
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
                    buAux.columns = colunas.keys()

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
        de votos recebido por um candidato.

        Retorno:
            fqabs (DataFrame): a frequência absoluta dos algarismos de 1 a 9 no primeiro dígito da
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
        """
            Determina o mínimo e o máximo da amostra de dados, bem como a ordem de
            grandeza entre a diferença dos mesmos.

            Retorno:
                minimo (int): menor valor dos dados.
                maximo (int): maior valor dos dados.
                odg (int): ordem de grandeza da diferença entre o máximo e o mínimo.
        """
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

    def erroRelativo(self, frequenciaObservada, frequenciaEsperada):
        """
            Determina o erro percentual entre o valor da frequência observada e
            o valor da frequência esperada.

            Retorno:
            erroRelativo (list) lista com os erros.
        """
        erroRelativo = [frequenciaObservada[i]/frequenciaEsperada[i] - 1.0 for i in range(len(frequenciaObservada))]
        return erroRelativo

    def grafico(self, nomeDoVotante, nomeDoArquivo, titulo, cores = ["#009c3b", "#002776"]):
        """
            Gera o arquivo com o gráfico de barras da frequência absoluta
            juntamente com a curva da lei de Benford.

            Argumento:
                nomeDoVotante (string): nome do votante que deve ser feito o gráfico.
                nomeDoArquivo (string): nome do arquivo do gráfico.
                titulo (string): título do gráfico.
                cores (list): lista com os códigos das cores usadas no gráfico.
        """
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

    def dividirArquivo(self, arquivo, numeroDeLinhas, sufixoDaSaida, codificacao = "ISO-8859-1"):
        """
            Divide o arquivo de boletim de urnas em vários arquivos com, 
            no máximo, uma quantidade desejada de linhas.

        Argumentos:
            arquivo (string): nome do arquivo do boletim de urnas.
            numeroDeLinhas (int): quantidade máxima do número de linhas nos novos arquivos.
            sufixoDaSaida (string): sufixo adicionado ao nome de cada novo arquivo criado.
            codificacao (str): codificação do arquivo.
        """
        try:
            arquivoOriginal = open(arquivo, "r", encoding = codificacao)
            parte = 1
            print(f"Criando arquivo: {sufixoDaSaida}{parte}.csv")
            arquivoParte = open(f"{sufixoDaSaida}{parte}.csv", "w", encoding = codificacao)
            lin = 0
            cab = ""
            for linha in arquivoOriginal:
                if(self._cabecalho and parte == 1):
                    cab = linha

                arquivoParte.write(linha)
                lin += 1
                if(lin >= numeroDeLinhas):
                    parte += 1
                    print(f"Criando arquivo: {sufixoDaSaida}{parte}.csv")
                    arquivoParte.close()
                    arquivoParte = open(f"{sufixoDaSaida}{parte}.csv", "w", encoding = codificacao)
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
        """
            Abrir o arquivo CSV com os dados apurados.

        Argumentos:
            arquivo (string): nome do arquivo com os dados apurados.
            cabecalho (bool): indica se a primeira linha do arquivo deve ser
            considerada como cabeçalho.
            delimitador (string): caracter que separa as colunas no arquivo do boletim 
            de urnas.
            codificacao (str, optional): codificação dos caracteres no arquivo do boletim
            de urnas. O padrão é "ISO-8859-1".
        """
        try:
            if(cabecalho):
                self._boletimDeUrna = pd.read_csv(arquivo, encoding = codificacao, delimiter = delimitador)
            else:
                self._boletimDeUrna = pd.read_csv(arquivo, encoding = codificacao, delimiter = delimitador, header = None)

        except:
            print(f"Alguma coisa deu errado ao abrir o arquivo {arquivo}.")

    def salvar(self, arquivo, cabecalho = True, delimitador = ";", codificacao = "ISO-8859-1"):
        """
            Salvar o arquivo CSV com os dados apurados.

        Argumentos:
            arquivo (string): nome do arquivo com os dados apurados.
            cabecalho (bool): indica se a primeira linha do arquivo deve ser
            considerada como cabeçalho.
            delimitador (string): caracter que separa as colunas no arquivo do boletim 
            de urnas.
            codificacao (str, optional): codificação dos caracteres no arquivo do boletim
            de urnas. O padrão é "ISO-8859-1".
        """
        try:
            self._boletimDeUrna.to_csv(
                arquivo,
                sep = delimitador,
                header = cabecalho,
                index = False,
                quoting = csv.QUOTE_ALL,
                encoding = codificacao
            )
        except:
            print(f"Alguma coisa deu errado ao salvar o arquivo {arquivo}.")

    def transferirVoto(self, arquivo, nomeNovoArquivo, removerVoto, adicionarVoto, porcentagem, quantidadeDeVotos, quantidadeDeVotaveisNoPleito, ordemAlfabeticaDoVotavelParaAdicionar, local = {}):
        """
            Transfere votos de um grupo de votantes para um outro votante.

        Argumentos:
            arquivo (string): nome do arquivo com os dados apurados.
            nomeNovoArquivo ([type]): nome do novo arquivo com os dados.
            removerVoto (list): lista de votáveis para retirar votos.
            adicionarVoto (string): votavel para adicionar os votos.
            porcentagem (float): porcentagem de votos que devem ser retirados.
            quantidadeDeVotos (int): quantidade de votos que deve ser transferida.
            quantidadeDeVotaveisNoPleito (int): quantidade de votaveis no arquivo
            de dados.
            ordemAlfabeticaDoVotavelParaAdicionar (int): posição do votável que
            receberá os votos na lista de votáveis em ordem alfabética.
            local (dict): dicionário formado com as chaves sendo a sigla do
            estado desejado e com os valores sendo uma lista de municípios
            do respectivo estado. Se a lista de municípios for vazia, então
            serão considerados todos os municípios do estado.
        """
        SG_UF = 0
        NM_MUNICIPIO = 1
        NM_VOTAVEL = 2
        QT_VOTOS = 3
        estados = local.keys()
        apuracaoReal = open(arquivo, encoding = self._codificacao)
        apuracaoSimulada = open(nomeNovoArquivo, "w", encoding = self._codificacao)
        dfApuracaoReal = csv.reader(apuracaoReal, delimiter = self._delimitador)
        dfApuracaoSimulada = csv.writer(apuracaoSimulada, delimiter = self._delimitador, quoting=csv.QUOTE_ALL)
        indices = []
        totalDeIndices = 0
        novoArquivo = []
        indices = []
        for linha in dfApuracaoReal:
            if(linha[SG_UF] in estados):
                if(len(local[linha[SG_UF]]) > 0):
                    if((linha[NM_MUNICIPIO] in local[linha[SG_UF]]) and (linha[NM_VOTAVEL] == adicionarVoto)):
                        indices.append(totalDeIndices)
                else:
                    if(linha[NM_VOTAVEL] == adicionarVoto):
                        indices.append(totalDeIndices)

            novoArquivo.append(linha)
            totalDeIndices += 1

        for id in indices:
            if(quantidadeDeVotos > 0):
                if(id > ordemAlfabeticaDoVotavelParaAdicionar):
                    inicio = id - ordemAlfabeticaDoVotavelParaAdicionar
                else:
                    inicio = 0

                if(id + (quantidadeDeVotaveisNoPleito - ordemAlfabeticaDoVotavelParaAdicionar - 1) < totalDeIndices):
                    fim = id + (quantidadeDeVotaveisNoPleito - ordemAlfabeticaDoVotavelParaAdicionar - 1)
                else:
                    fim = totalDeIndices - 1

                totalDeVotos = 0
                removerVotoId = []
                for i in range(inicio, fim + 1):
                    if((novoArquivo[i][NM_MUNICIPIO] == novoArquivo[id][NM_MUNICIPIO])):
                        totalDeVotos += int(novoArquivo[i][QT_VOTOS])
                        if(novoArquivo[i][NM_VOTAVEL] in removerVoto):
                            removerVotoId.append(i)

                vt = int(novoArquivo[id][QT_VOTOS])
                universoDeVotosParaRemover = totalDeVotos - vt
                quantidadeDeVotosParaRedistribuir = round(porcentagem*universoDeVotosParaRemover)
                retirados = 0
                if(quantidadeDeVotosParaRedistribuir > 0):
                    retirar = {}
                    for i in removerVotoId:
                        vt = int(novoArquivo[i][QT_VOTOS])
                        r = round(porcentagem*vt)
                        retirar[i] = r
                        retirados += r

                    if(retirados > 0):
                        for i in removerVotoId:
                            if(quantidadeDeVotos - retirar[i] <= 0):
                                retirar[i] = quantidadeDeVotos

                            novoArquivo[i][QT_VOTOS] = str(int(novoArquivo[i][QT_VOTOS]) - retirar[i])
                            novoArquivo[id][QT_VOTOS] = str(int(novoArquivo[id][QT_VOTOS]) + retirar[i])
                            quantidadeDeVotos -= retirar[i]
                            if(quantidadeDeVotos <= 0):
                                break

                    if(quantidadeDeVotos <= 0):
                        break

                if((quantidadeDeVotosParaRedistribuir == 0) or (retirados == 0)):
                    print(f"{novoArquivo[id][NM_MUNICIPIO]}: nenhum voto retirado.")

        for linha in novoArquivo:
            dfApuracaoSimulada.writerow(linha)
        
        self.abrir(nomeNovoArquivo, self._cabecalho, self._delimitador, self._codificacao)