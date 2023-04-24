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

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)