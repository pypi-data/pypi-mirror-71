# TakeAicHelper


### Instanciando a classe

```Python
from TakeAicHelper.metrics import Metrics

analyse = Metrics(path=r'C:\Users\base.csv', encoding='utf-8', sep=';', minimunScore=0.6)
analyse.overview()
```


* Obter e manipular o tamanho da base de entrada (o número de inputs), a quantidade de intenções, 
a Taxa de Compreensão Geral (TCG) e a quantidade de inputs reconhecidos com o score maior e menor que o mínimo.

`analyse.overview()`

* Obter e manipular somente o valor da Taxa de Compreensão Geral.

`analyse.tcg()`
  
* Obter um ranking das entidades reconhecidas.

`analyse.intentDetails("NOME_DA_INTENÇÃO")`
  
* analyse.entities(n=0, mode=None, intentName=None)

`n = 0` - Mostra todas as entidades
`n > 0` - Top > n  entidades reconheidas
`n < 0` - Top < n  entidades reconheidas

`mode = total` - Reconhecidas em geral (Considerando se reconhecidas junto com outras entidades)
`mode = individual` - Reconhecidas em geral (ignorando se reconhecidas junto com outras entidades)

`intentName = NOME_DE_UMA_INTENCAO` -  (Caso queira analisar as entidades reconhecidas numa intenção específica)


* Salvar arquivos em csv separados por intenção:

`analyse.csvByIntentions(output, sep)`

`output = diretório do nome da pasta`
`sep = separador do arquivo`


**obs**: No databricks, para salvar mais tabelas, é utilizado a função `analyse.tableByIntentions()`

* Com a função tr() (Taxa de Reconhecimento) e tci() (Taxa de Compreensão Interna) é possível obter três visualizações (dataframe,tabela ou gráfico)

`analyse.tr(figure, valueType, order)`
`analyse.tci(figure, valueType, order, minimunScore=0.6)`

`figure = 'dataframe', 'chart' (gráfico), 'table' (tabela)`
`valueType = '%' (porcecntagem) , 'total' (número inteiro)`
`order = 'asc' (crescente) , 'desc' (decrescente)`
`minimunScore (apenas na tci) = score mínimo a ser a analisado, por default é 0.6`




