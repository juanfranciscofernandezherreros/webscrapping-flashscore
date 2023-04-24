# Foobar

Foobar is a Python library for dealing with word pluralization.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install foobar
```

## index.py

```python
Este es un script de Python que utiliza Pyppeteer, una librería que nos permite interactuar con un navegador web a través de Python, para extraer enlaces (hrefs) de una página web.

El script comienza definiendo varias funciones que interactúan con una base de datos MySQL utilizando el módulo "config.database". Las funciones son las siguientes:

create_urls_table(): Esta función comprueba si existe una tabla llamada "urls" en la base de datos. Si no existe, la crea.

count_unopened_urls(): Esta función cuenta la cantidad de URLs que aún no han sido abiertas en la base de datos.

get_unopened_urls(): Esta función obtiene una lista de URLs que aún no han sido abiertas en la base de datos.

insert_url(url): Esta función inserta una nueva URL en la base de datos.

update_url(url): Esta función actualiza el estado de una URL a "abierta" en la base de datos.

check_url_exists(url): Esta función verifica si una URL ya existe en la base de datos.

La función principal del script es "main", que acepta una URL opcional como argumento. Si se proporciona una URL, la función comprueba si la URL ya existe en la base de datos y, si no es así, la inserta. Luego, el script entra en un bucle que se ejecuta mientras haya URLs sin abrir en la base de datos. Dentro del bucle, el script obtiene una lista de URLs sin abrir de la base de datos y las recorre una por una.

Para cada URL, el script comprueba si ha pasado un minuto desde que comenzó la ejecución. Si se ha alcanzado el límite de tiempo de un minuto, el script sale del bucle y se detiene. De lo contrario, el script abre la URL utilizando Pyppeteer, extrae los enlaces (hrefs) de la página y los filtra para incluir solo aquellos que contienen la cadena "basketball" y tienen entre 5 y 7 barras (/) en la URL (esto es específico para el sitio web de FlashScore). Luego, el script comprueba si cada uno de los enlaces extraídos ya existe en la base de datos. Si no existe, se inserta en la base de datos. Si ya existe, se muestra un mensaje en la consola.

Finalmente, el script actualiza el estado de la URL original a "abierta" en la base de datos y continúa con la siguiente URL en la lista de URLs sin abrir.

El script utiliza el módulo "argparse" para aceptar una URL opcional como argumento de línea de comandos. Si no se proporciona ninguna URL, el script simplemente comienza a buscar enlaces en la base de datos.
```

## fixtures.py

```python
Este script realiza lo siguiente paso a paso:

Importa los módulos necesarios, tales como asyncio, csv, pyppeteer, datetime, urllib, glob, os, mysql.connector, resultsMatch, config.database, sys y fixtures_init.
Define una función main(uri) que recibe una URL como parámetro.
Verifica si existe una carpeta llamada "csv". Si no existe, la crea.
Crea una subcarpeta llamada "basketball" dentro de la carpeta "csv". Si no existe, la crea.
Crea una subcarpeta llamada "fixtures" dentro de la subcarpeta "basketball". Si no existe, la crea.
Inicia el navegador mediante la función launch() de pyppeteer, sin que sea visible en la pantalla (headless=False).
Abre una nueva página mediante la función newPage() del navegador.
Navega a la URL especificada en el parámetro mediante la función goto() de la página.
Obtiene todos los elementos que contienen la clase CSS "event" mediante la función querySelectorAll().
Extrae el identificador de cada elemento mediante la función getProperty() y lo almacena en una lista llamada ids.
Obtiene todos los elementos que contienen la clase CSS "event__time" y los almacena en una variable llamada events.
Obtiene todos los elementos que contienen la clase CSS "event__participant--home" y los almacena en una variable llamada eventHome.
Obtiene todos los elementos que contienen la clase CSS "event__participant--away" y los almacena en una variable llamada awayHome.
Crea una lista vacía llamada data.
Extrae el nombre de la competición, la temporada y la categoría de la URL, y los combina en una cadena de texto que almacena en la variable text.
Genera una marca de tiempo actual y la almacena en la variable time_str.
Itera sobre los elementos en la variable events, y para cada uno extrae el identificador, la fecha y hora del evento, el nombre del equipo local y el nombre del equipo visitante.
Agrega el identificador, la fecha y hora del evento, el nombre del equipo local y el nombre del equipo visitante a la lista data.
Extrae el nombre de dominio de la URL y lo usa como el nombre del archivo CSV que se va a crear.
Abre el archivo CSV en modo de escritura y crea un objeto escritor CSV con la función writer().
Escribe las filas en el archivo CSV utilizando el objeto escritor CSV.
Cierra el archivo CSV.
Cierra el navegador.
Si se ejecuta el archivo directamente, extrae la URL del primer argumento de la línea de comandos y llama a la función main() con esa URL.
```
## resultados_init.py

```python
Este script realiza lo siguiente:

Importa los módulos necesarios: mysql.connector, asyncio, resultsMatch, config.database, sys, os y fixtures_init.
Define una función main que acepta tres argumentos: url, country y competition.
Establece una conexión a una base de datos MySQL utilizando la información de conexión almacenada en el archivo config/database.py.
Crea un objeto cursor para ejecutar consultas en la base de datos.
Ejecuta una consulta SELECT en la tabla urls para buscar filas que contengan la cadena de texto especificada en los argumentos url, country y competition.
Recupera los resultados de la consulta y los almacena en la variable myresult.
Si el argumento url contiene la cadena "results" y la variable myresult contiene al menos una fila, ejecuta la función resultsMatch.main para cada una de las filas recuperadas de la base de datos. Esta función se encarga de extraer los resultados de un partido a partir de la URL especificada y almacenarlos en la base de datos.
Si el argumento url contiene la cadena "fixtures" y la variable myresult contiene al menos una fila, ejecuta la función fixtures_init.main para cada una de las filas recuperadas de la base de datos. Esta función se encarga de extraer la información de los próximos partidos a partir de la URL especificada y almacenarlos en la base de datos.
Si el argumento url no contiene la cadena "results" ni la cadena "fixtures" o si la variable myresult está vacía, muestra un mensaje indicando que la URL no cumple con los criterios de búsqueda.
En el bloque if __name__ == '__main__':, obtiene los argumentos de línea de comando utilizando la función sys.argv y llama a la función asyncio.run para ejecutar la función main con los argumentos especificados.
```

## archive_init.py

```python



```

[MIT](https://choosealicense.com/licenses/mit/)