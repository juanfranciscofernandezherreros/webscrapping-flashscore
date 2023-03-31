Multiples Scripts Working

1 python script.py https://www.example.com/basketball/ 3 basketball_urls

El código que proporcionaste utiliza pyppeteer para extraer los atributos href de las etiquetas "a" de una página web y luego guardar los datos extraídos en un archivo CSV.

Así es como funciona el código:

La función get_hrefs() utiliza pyppeteer para lanzar un navegador sin cabeza y navegar hasta la URL especificada. Luego utiliza page.querySelectorAllEval() para encontrar todas las etiquetas "a" de la página y sus atributos href. La función set() se utiliza para eliminar los href duplicados. Finalmente, los href se filtran para incluir solo aquellos que contienen la palabra "basketball" y tienen un número específico de barras diagonales en la ruta de la URL (según lo especificado por num_slashes).

La función export_to_csv() llama a get_hrefs() para obtener los href filtrados y luego los guarda en un archivo CSV utilizando el objeto csv.writer y el método writerow(). El archivo CSV se crea en una carpeta llamada csv en el directorio de trabajo actual. Si la carpeta no existe, se crea con os.makedirs().

El bloque if __name__ == '__main__': llama a export_to_csv() con la URL, el número de barras diagonales y el nombre de archivo especificados.

Es importante tener en cuenta que el código utiliza el módulo asyncio de Python para ejecutar las funciones get_hrefs() y export_to_csv() de manera asíncrona. La función asyncio.run() se utiliza para ejecutar la función export_to_csv().

