import mysql.connector
import matplotlib.pyplot as plt
from datetime import datetime


def conectar():
    # Configurar la conexión
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mnpe"
    )
    return conexion

def cerrar_conexion(conexion):
    # Cerrar la conexión
    conexion.close()

def crear_registro(datos):
    try:
        # Conectar a la base de datos
        conexion = conectar()

        # Crear un cursor para ejecutar consultas
        cursor = conexion.cursor()

        # Ejemplo de inserción
        consulta_insert = "INSERT INTO monitor (voltaje, frecuencia) VALUES (%s, %s)"
        cursor.execute(consulta_insert, datos)

        # Confirmar la transacción
        conexion.commit()
        print("Registro creado exitosamente!")

    except mysql.connector.Error as error:
        print(f"Error al crear el registro: {error}")

    finally:
        # Cerrar el cursor y la conexión
        if 'cursor' in locals():
            cursor.close()
        cerrar_conexion(conexion)

def leer_registros():
    try:
        # Conectar a la base de datos
        conexion = conectar()

        # Crear un cursor para ejecutar consultas
        cursor = conexion.cursor()

        # Ejemplo de lectura
        consulta_select = "SELECT fecha,voltaje,frecuencia FROM `monitor` ORDER BY `fecha` DESC LIMIT 40"
        cursor.execute(consulta_select)
        registros = cursor.fetchall()

        # Mostrar los registros
        for registro in registros:
            fechas = [str(registro[0]) for registro in registros]
            voltajes = [registro[1] for registro in registros]
            frecuencias = [registro[2] for registro in registros]
    
            # Convertir fechas a objetos de tipo datetime
            fechas = [datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S") for fecha in fechas]
    
            # Crear gráfico de voltajes
            plt.figure(figsize=(10, 5))
            plt.plot(fechas, voltajes, marker='o', linestyle='-', color='r')
            #plt.bar(fechas, voltajes, color='blue')
            plt.title('Gráfico de Voltaje con respecto a la Fecha')
            plt.xlabel('Fecha')
            plt.ylabel('Voltaje')
            #plt.ylim(121, 123)
            #plt.yticks(range(121, 123, 1))
            plt.grid(True)
            plt.show()
    
            # Crear gráfico de frecuencias
            # plt.figure(figsize=(10, 5))
            # plt.plot(fechas, frecuencias, marker='o', linestyle='-', color='r')
            # plt.title('Gráfico de Frecuencia con respecto a la Fecha')
            # plt.xlabel('Fecha')
            # plt.ylabel('Frecuencia')
            # plt.grid(True)
            # plt.show()
            #print(registro)

    except mysql.connector.Error as error:
        print(f"Error al leer los registros: {error}")

    finally:
        # Cerrar el cursor y la conexión
        if 'cursor' in locals():
            cursor.close()
        cerrar_conexion(conexion)

def actualizar_registro(id, voltaje, frecuencia):
    try:
        # Conectar a la base de datos
        conexion = conectar()

        # Crear un cursor para ejecutar consultas
        cursor = conexion.cursor()

        # Ejemplo de actualización
        consulta_update = f"UPDATE monitor SET {voltaje} = %s WHERE id = %s"
        datos_update = (voltaje, id)

        cursor.execute(consulta_update, datos_update)

        # Confirmar la transacción
        conexion.commit()
        print("Registro actualizado exitosamente!")

    except mysql.connector.Error as error:
        print(f"Error al actualizar el registro: {error}")

    finally:
        # Cerrar el cursor y la conexión
        if 'cursor' in locals():
            cursor.close()
        cerrar_conexion(conexion)

def eliminar_registro(id):
    try:
        # Conectar a la base de datos
        conexion = conectar()

        # Crear un cursor para ejecutar consultas
        cursor = conexion.cursor()

        # Ejemplo de eliminación
        consulta_delete = "DELETE FROM voltaje WHERE id = %s"
        cursor.execute(consulta_delete, (id,))

        # Confirmar la transacción
        conexion.commit()
        print("Registro eliminado exitosamente!")

    except mysql.connector.Error as error:
        print(f"Error al eliminar el registro: {error}")

    finally:
        # Cerrar el cursor y la conexión
        if 'cursor' in locals():
            cursor.close()
        cerrar_conexion(conexion)

'''
# Ejemplo de uso
# Crear un registro
datos_nuevo_registro = ("valor_columna1", "valor_columna2", "valor_columna3")
crear_registro(datos_nuevo_registro)

# Leer registros
leer_registros()

# Actualizar un registro (asumiendo que hay al menos un registro en la tabla)
id_registro_a_actualizar = 1
nuevo_valor_para_columna = "Nuevo Valor"
columna_a_actualizar = "nombre_columna1"
actualizar_registro(id_registro_a_actualizar, nuevo_valor_para_columna, columna_a_actualizar)

# Eliminar un registro (asumiendo que hay al menos un registro en la tabla)
id_registro_a_eliminar = 1
eliminar_registro(id_registro_a_eliminar)

# Leer registros después de las operaciones
leer_registros()
'''
