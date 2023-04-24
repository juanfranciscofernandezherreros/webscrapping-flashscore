import csv
import mysql.connector

# Conexión a la base de datos MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="user_bigdataetl",
    password="password_bigdataetl",
    database="bigdataetl"
)

if mydb.is_connected():
    # Crear cursor
    mycursor = mydb.cursor()

    # Crear tabla
    mycursor.execute("CREATE TABLE IF NOT EXISTS usuarios (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(255), email VARCHAR(60))")

    # Leer datos del archivo CSV
    ya_existe = []
    insertados = []
    errores = []
    with open('csv/datos.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader) # Saltar la primera fila que contiene los nombres de las columnas
        for row in csv_reader:
            nombre = row[0]
            email = row[1]
            # Consultar si ya existe el registro
            sql = "SELECT * FROM usuarios WHERE nombre = %s AND email = %s"
            val = (nombre, email)
            mycursor.execute(sql, val)
            result = mycursor.fetchone()
            if result:
                ya_existe.append(f"El registro '{nombre}, {email}' ya existe en la base de datos.")
            else:
                # Insertar el registro si no existe
                sql = "INSERT INTO usuarios (nombre, email) VALUES (%s, %s)"
                val = (nombre, email)
                try:
                    mycursor.execute(sql, val)
                    mydb.commit()
                    insertados.append(f"El registro '{nombre}, {email}' se ha insertado correctamente.")
                except Exception as e:
                    mydb.rollback() # Revertir la transacción
                    errores.append(f"Error al insertar el registro '{nombre}, {email}': {str(e)}")
                    
    # Imprimir resultados
    print("Resultados de las inserciones:")
    for resultado in insertados:
        print(resultado)
        
    if len(ya_existe) > 0:
        print("\nRegistros que ya existen en la base de datos:")
        for registro in ya_existe:
            print(registro)
    
    if len(errores) > 0:
        print("\nErrores de inserción:")
        for error in errores:
            print(error)

else:
    print("No se pudo conectar a la base de datos MySQL")
