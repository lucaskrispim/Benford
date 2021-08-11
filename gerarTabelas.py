#!/usr/bin/python3
import pandas as pd
"""
    [Inserir documentação]
"""

turno = ['1', '2']
ano = ['2014', '2018']
nomeDoVotavel = []
temp = {
    '2014' : {'1' : [], '2' : []},
    '2018' : {'1' : [], '2' : []}
}
dirbase = "/opt/eleicoes/"
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
        temp[a][t] = nomeDoVotavel.copy()
        for nome in nomeDoVotavel:
            print(f"{nome} ", end = '')
            for fq in frel[nome]:
                print(f"{fq:4.2f} ", end = '')

            print("")

        print("\n")

estado = [
    "AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT",
    "PA", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO",
    "ZZ"
]
for a in ano:
    for t in turno:
        totalDeMunicipios = 0
        nomeDoVotavel = temp[a][t]
        df = {}
        for nome in nomeDoVotavel:
            df[nome] = {"MIN": 1.0e+10, "MAX": -1.0e+10, "QTD_MUNICIPIOS" : 0}

        print(f"TABELA MÍNIMO E MÁXIMO DE VOTOS NO TURNO {t} ANO {a}\n")
        for es in estado:
            ap = f"{dirbase}{a}/apuracao-t{t}-{a}-{es}.csv"
            dfAux = pd.read_csv(ap, encoding = codificacao, delimiter = delimitador)
            totalDeMunicipios += len(dfAux["NM_MUNICIPIO"].unique())
            for nome in nomeDoVotavel:
                votos = dfAux.loc[(dfAux["NM_VOTAVEL"] == nome) & (dfAux["QT_VOTOS"] > 0)]
                if(len(votos) > 0):
                    df[nome]["QTD_MUNICIPIOS"] += len(votos)
                    if(nome in df.keys()):
                        if(votos['QT_VOTOS'].min() < df[nome]["MIN"]):
                            df[nome]["MIN"] = votos['QT_VOTOS'].min()

                        if(votos['QT_VOTOS'].max() > df[nome]["MAX"]):
                            df[nome]["MAX"] = votos['QT_VOTOS'].max()

        for nome in df.keys():
            print(f"{nome} {df[nome]['MIN']} {df[nome]['MAX']} {(100.0*df[nome]['QTD_MUNICIPIOS']/totalDeMunicipios):4.2f}")

        print("")
