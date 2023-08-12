# PyDownload  
Implementação simples para download de arquivos

## Pré-requisitos:

```bat
pip install urllib3
```

## Parâmetros

* **url** -> endereço do arquivo na internet: <br>
  `https://raw.githubusercontent.com/samuelpcavalcantee/PyDownload/main/teste/teste.mp4`

* **path** -> endereço do sistema onde salvar o arquivo: <br>
  `C:/Users/{user}/Downloads/`

## Parâmetros Opcionais

* **file_name** -> nome do arquivo. Caso não esteja presente, é obtido da url: <br>
  `https://raw.githubusercontent.com/samuelpcavalcantee/PyDownload/main/teste/` `teste.mp4`

* **header** -> cabeçalhos personalizados: <br>
  ```Python
  {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
  }
  ```

* **human** -> obtém resultados já convertidos com unidades:
  `True` ou `False`

* **success** -> função executada após o download bem-sucedido

* **error** -> função executada após erro no download do arquivo

* **change** -> função executada durante o download do arquivo

* **success_args**, **error_args**, **change_args** -> parâmetros passados para suas respectivas funções `(parametro1, ...)`

## Exemplo

```Python
def teste1(data, x):
    print(data, x)

def teste2(data, x, y):
    print(data, x, y)

def teste3(data, x, y, z):
    print(data, x, y, z)

obj = download(
    url="https://raw.githubusercontent.com/samuelpcavalcantee/PyDownload/main/teste/teste.mp4",
    path="C:/Users/{user}/Downloads/",
    file_name="file.mp4",
    header={"Accept-Encoding": "gzip, deflate, br"},
    human=True,
    success=teste1,
    success_args=(1,),
    error=teste2,
    error_args=(1, 2),
    change=teste3,
    change_args=(1, 2, 3)
)

While True:
  print(obj.info())
  time.sleep(1)
```
`Data é um parâmetro obrigatório que retorna propriedades do download.`
