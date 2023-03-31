Multiples Scripts Working

py search.py

El código se encarga de abrir URLs de una tabla en una base de datos MySQL, tomar capturas de pantalla para obtener todos los enlaces que contienen la palabra "basketball" y "/5", "/6" o "/7" en su URL, insertar los enlaces filtrados en la base de datos, actualizar el estado de la URL a "T" en la base de datos y guardar los enlaces insertados y los que generaron errores en archivos CSV.

Primero, se conecta a la base de datos especificada y verifica si existe la carpeta "csv" en el directorio actual, si no existe la crea. Luego crea una subcarpeta llamada "basketball" dentro de la carpeta "csv" y otra subcarpeta llamada "urls" dentro de la carpeta "basketball".

Después, el código entra en un bucle y ejecuta una consulta SQL en la tabla "urls" para obtener la primera URL que tenga un estado de "F" (no abierta). Si no hay URL con estado "F", el bucle se detiene y el programa espera 10 segundos antes de volver a intentar.

Luego, el código toma una captura de pantalla de la URL y obtiene todos los enlaces en la página. Se filtran los enlaces que contienen "basketball" y "/5", "/6" o "/7" en su URL.

A continuación, se insertan los enlaces filtrados en la base de datos y se actualiza el estado de la URL a "T". Si se genera un error al insertar un enlace, se guarda el enlace y el mensaje de error en una lista para ser guardado en un archivo CSV más tarde.

Finalmente, se imprimen estadísticas sobre la cantidad total de enlaces, la cantidad de enlaces insertados correctamente y la cantidad de enlaces que generaron errores. Los enlaces insertados y los que generaron errores se guardan en archivos CSV en la subcarpeta "urls" de la carpeta "basketball".

Luego, se crea una carpeta llamada "basketball" dentro de la carpeta "csv" si no existe aún.
Después, se crea una subcarpeta llamada "urls" dentro de la carpeta "basketball" si no existe aún.
Se inicia un bucle infinito que se detiene cuando no hay más URLs por abrir en la base de datos.
Se obtiene la siguiente URL por abrir de la base de datos. La consulta se realiza con la ayuda de un cursor de MySQL. La consulta selecciona la primera URL que tenga el estado "F" (no abierta) de la tabla "urls".
Se toma una captura de pantalla de la página correspondiente a la URL obtenida para obtener todos los enlaces que contienen la palabra "basketball" y que tienen 5, 6 o 7 barras después del dominio en su dirección URL. Se utiliza la biblioteca pyppeteer para automatizar un navegador web y realizar esta tarea.
Se filtran los enlaces obtenidos para que solo contengan la palabra "basketball" y tengan 5, 6 o 7 barras después del dominio en su dirección URL. Estos enlaces se insertan en la tabla "urls" de la base de datos, marcándolos como no abiertos ("F").
Se guardan los enlaces insertados con éxito y los enlaces con errores en dos archivos CSV diferentes en la subcarpeta "urls" de la carpeta "basketball".
Se actualiza el estado de la URL obtenida inicialmente en la base de datos a "T" (abierta).
Se imprimen algunas estadísticas, como la cantidad total de enlaces que se intentaron insertar y la cantidad de enlaces insertados correctamente y con errores.