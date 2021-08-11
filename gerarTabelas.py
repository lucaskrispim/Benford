#!/usr/bin/python3
import pandas as pd
from scipy.stats import chisquare, chi2
from numpy import log10

turno = ['1', '2']
ano = ['2014', '2018']
estado = [
    "AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT",
    "PA", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO",
    "ZZ"
]
nomeDoVotavel = []
dirbase = "eleicoes/"
codificacao = "ISO-8859-1"
delimitador = ";"
for a in ano:
    for t in turno:
        print(f"TABELA TURNO {t} ANO {a}\n")
        arquivoFrequenciaRelativa = f"{dirbase}{a}/frequencia-relativa-t{t}-{a}.csv"
        frel = pd.read_csv(arquivoFrequenciaRelativa, encoding = codificacao, delimiter = delimitador)        
        nomeDoVotavel = list(frel.columns)
        nomeDoVotavel = [nome.upper() for nome in nomeDoVotavel]
        retirar = ["BRANCO", "NULO", "DÍGITO"]
        for r in retirar:
            nomeDoVotavel.remove(r)

        nomeDoVotavel.append("BRANCO")
        nomeDoVotavel.append("NULO")
        for nome in nomeDoVotavel:
            print(f"{nome} ", end = '')
            for fq in frel[nome]:
                print(f"{fq:4.2f} ", end = '')

            print("")

        print("\n")
        totalDeMunicipios = 0
        votosExtremos = {}
        for nome in nomeDoVotavel:
            votosExtremos[nome] = {"MIN": 1.0e+10, "MAX": -1.0e+10, "QTD_MUNICIPIOS" : 0}

        print(f"TABELA MÍNIMO E MÁXIMO DE VOTOS NO TURNO {t} ANO {a}\n")
        for es in estado:
            ap = f"{dirbase}{a}/apuracao-t{t}-{a}-{es}.csv"
            dfAux = pd.read_csv(ap, encoding = codificacao, delimiter = delimitador)
            totalDeMunicipios += len(dfAux["NM_MUNICIPIO"].unique())
            for nome in nomeDoVotavel:
                votos = dfAux.loc[dfAux["NM_VOTAVEL"] == nome]
                if(len(votos) > 0):
                    votosExtremos[nome]["QTD_MUNICIPIOS"] += len(votos)
                    votosMin = votos['QT_VOTOS'].min()
                    votosMax = votos['QT_VOTOS'].max()
                    if(votosMin < votosExtremos[nome]["MIN"]):
                        votosExtremos[nome]["MIN"] = votosMin

                    if(votosMax > votosExtremos[nome]["MAX"]):
                        votosExtremos[nome]["MAX"] = votosMax

        for nome in votosExtremos.keys():
            print(f"{nome} {votosExtremos[nome]['MIN']} {votosExtremos[nome]['MAX']} {(100.0*votosExtremos[nome]['QTD_MUNICIPIOS']/totalDeMunicipios):4.2f}")

        print("\n")
        print(f"TESTE DE ADERÊNCIA TURNO {t} ANO {a}")
        lfrel = []
        leiDeBenford = [100.0*(log10(x + 1) - log10(x)) for x in range(1, 10)]
        leiDeBenford[7] = leiDeBenford[7] + leiDeBenford[8]
        leiDeBenford.pop()
        degreeOfFreendom = len(leiDeBenford) - 1
        alfa = 0.05
        chiCritico = chi2.ppf(1 - alfa, degreeOfFreendom)
        print(f"(chiCritico = {chiCritico:6.4f}, alfa = {alfa})\n")
        for nome in nomeDoVotavel:
            lfrel = frel.loc[0:6, nome]
            lfrel[7] = (frel.loc[7, nome] + frel.loc[8, nome])
            chi, p  = chisquare(leiDeBenford, lfrel)
            if(chi < chiCritico):
                print(f"{nome} Sucesso {chi:6.4f} {p:6.4f}")
            else:
                print(f"{nome} Falha {chi:6.4f} {p:6.4f}")

        print("")