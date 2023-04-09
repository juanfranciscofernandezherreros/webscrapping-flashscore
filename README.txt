Para obtener el timestamp de hoy de las 00:00 y 23:59 en MySQL, puedes utilizar la función UNIX_TIMESTAMP() junto con las funciones DATE() y CONCAT() para obtener las fechas de inicio y fin del día actual en formato de timestamp.

Aquí te presento una posible solución a tu pregunta:

mysql
Copy code
SELECT 
    UNIX_TIMESTAMP(CONCAT(DATE(NOW()), ' 00:00:00')) as start_timestamp,
    UNIX_TIMESTAMP(CONCAT(DATE(NOW()), ' 23:59:59')) as end_timestamp
La función NOW() devuelve la fecha y hora actual en formato YYYY-MM-DD HH:MM:SS, luego se utiliza la función DATE() para obtener solo la fecha en formato YYYY-MM-DD.

Después, se concatena la fecha obtenida con la cadena ' 00:00:00' para obtener la fecha de inicio del día actual en formato YYYY-MM-DD 00:00:00, y se aplica la función UNIX_TIMESTAMP() para convertir esta fecha en un timestamp.

De manera similar, se concatena la fecha obtenida con la cadena ' 23:59:59' para obtener la fecha de fin del día actual en formato YYYY-MM-DD 23:59:59, y se aplica la función UNIX_TIMESTAMP() para convertir esta fecha en un timestamp.

El resultado de esta consulta devolverá dos columnas con los timestamps de inicio y fin del día actual en formato UNIX.