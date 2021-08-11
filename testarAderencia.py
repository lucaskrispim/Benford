import pandas as pd
from scipy.stats import chisquare,chi2
from numpy import log10

files = [
  "eleicoes/2014/frequencia-relativa-t1-2014.csv",
  "eleicoes/2014/frequencia-relativa-t2-2014.csv",
  "eleicoes/2018/frequencia-relativa-t1-2018.csv",
  "eleicoes/2018/frequencia-relativa-t2-2018.csv",
]

ben = [100.0*(log10(x + 1) - log10(x)) for x in range(1, 10)]

ben[7] = ben[7] + ben[8]
ben.pop()
#print(ben)

for f in files:
  try:
    df = pd.read_csv(f, encoding = "ISO-8859-1", delimiter=';')
    list = []
    for col in df.columns:
      #print(col)
      list = df.loc[0:6,col]
      list[7] = (df.loc[7,col] + df.loc[8,col])
      #print(list)
      
      stat, p  = chisquare(ben,list)
      chiCritico = chi2.ppf(0.95,7)
      print(f"{col} {stat} - {chiCritico}")        
      # # interpret p-value
      # alpha = 0.05
      # print("p value is " + str(p))
      # if p <= alpha:
      #     print('Dependent (reject H0)')
      # else:
      #     print('Independent (H0 holds true)')
      
      #print()
    #print(df)
    print()
  except Exception:
    print("An exception occurred")
    