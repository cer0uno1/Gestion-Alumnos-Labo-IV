import mysql.connector
from datetime import datetime

# Conexión a DB
conectar = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="gestionalumnos"
)
cursor = conectar.cursor()

# Función para chequear si el legajo existe
def legajoExiste():
    cursor.execute("SELECT * FROM alumnos WHERE legajo = %s", (legajo,))
    return cursor.fetchone() is not None

# Función para insertar datos
def ingresoDatos():
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    
    # El número de DNI debe ser menor a 8 y, obviamente, un número
    while True:
        documento = input("Número de documento (máximo 8 dígitos): ")
        if documento.isdigit() and len(documento) <= 8:
            break
        else:
            print("El DNI debe contener solo números y tener un máximo de 8 caracteres.")
            
    # Se busca que la fecha tenga el formato correcto, y que no sea mayor al día actual
    while True:
        fecha_nacimiento = input("Fecha de nacimiento (AAAA-MM-DD): ")
        try:
            fecha_nac = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
            if fecha_nac < datetime.now():
                break
            else:
                print("La fecha de nacimiento no puede ser mayor a la fecha actual.")
        except ValueError:
            print("Formato de fecha incorrecto. Usa AAAA-MM-DD.")
            
            
    # Chequea que el número de télefono sea un número menor a diez dígitos
    while True:
        telefono = input("Teléfono (máximo 10 dígitos): ")
        if telefono.isdigit() and len(telefono) <= 10:
            break
        else:
            print("El teléfono debe contener solo números y tener un máximo de 10 caracteres.")
    
    domicilio = input("Domicilio: ")

# Inserta todo lo ingresado en la base de datos de alumnos
    query = "INSERT INTO alumnos (nombre, apellido, dni, fechaNacimiento, telefono, domicilio) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (nombre, apellido, documento, fecha_nacimiento, telefono, domicilio)
    
    cursor.execute(query, values)
    conectar.commit()
    print("Datos ingresados correctamente.\n")

# Función para consultar datos
def consultaDatos():
    cursor.execute("SELECT * FROM alumnos")
    for (legajo, nombre, apellido, dni, fechaNacimiento, telefono, domicilio) in cursor.fetchall():
        print(f"Legajo: {legajo}\n Nombre y Apellido: {nombre} {apellido}\n Documento: {dni}\n Fecha de nacimiento: {fechaNacimiento}\n Num. Telefono: {telefono}\n Domicilio: {domicilio}\n")
        query = "SELECT cursos.nombrecurso FROM cursos JOIN alumno_toma_curso ON cursos.idcursos = alumno_toma_curso.idCurso WHERE alumno_toma_curso.legajoAlumno = %s"
        # Une la tabla de cursos con la de inscripción de alumnos a cursos, filtra solo las inscripciones del alumno requerido.
        cursor.execute(query, (legajo,))
        cursos = cursor.fetchall()
        
        # Si el alumno está inscripto al menos a un curso, lo muestra
        if cursos:
            print("Cursos del alumno:")
            for(nombrecurso) in cursos:
                print(f"- {nombrecurso}")
        
        else:
            print("Sin cursos asignados")
            
print("--------------------")

# Función para eliminar datos, elimina solo los datos del alumno cuyo legajo es ingresado
def eliminacionDatos():
    alumnoEliminar = input("Ingrese el Legajo del alumno a eliminar: ")
    
    # Verificar si el legajo existe
    cursor.execute("SELECT * FROM alumnos WHERE legajo = %s", (alumnoEliminar,))
    alumno = cursor.fetchone()  # Recupera una fila
    
    if alumno:  # Si se encuentra el alumno
        print(f"Se encontró el alumno: {alumno}")
        confirmacion = input("¿Está seguro de que desea eliminar este alumno? (s/n): ").strip().lower()
        
        if confirmacion == 's':
            cursor.execute("DELETE FROM alumnos WHERE legajo = %s", (alumnoEliminar,))
            conectar.commit()
            print("Alumno eliminado correctamente.")
        else:
            print("Operación cancelada.")
    else:
        print("No se encontró un alumno con ese legajo. Verifique el número ingresado.")

     
# Función para actualizar datos
def actualizarDatos():
    alumnoActualizar = input("Ingrese el Legajo del alumno a actualizar: ")
    
    # Se comprueba si el alumno existe
    cursor.execute("SELECT * FROM alumnos WHERE legajo = %s", (alumnoActualizar,))
    alumno = cursor.fetchone() # fetchone() solo toma la primer fila del resultado de la consulta, 
    
    # Si existe el alumno, se pide reingresar sus datos
    if alumno:
        print("Ingrese los nuevos datos (deje en blanco para mantener el actual):")
        nombre = input(f"Nombre [{alumno[1]}]: ") or alumno[1]
        apellido = input(f"Apellido [{alumno[2]}]: ") or alumno[2]
        documento = input(f"Número de documento [{alumno[3]}]: ") or alumno[3]
        fecha_nacimiento = input(f"Fecha de nacimiento (AAAA-MM-DD) [{alumno[4]}]: ") or alumno[4]
        telefono = input(f"Teléfono [{alumno[5]}]: ") or alumno[5]
        domicilio = input(f"Domicilio [{alumno[6]}]: ") or alumno[6]
        
    # Se actualizan los datos del alumno
        query = """UPDATE alumnos 
                   SET nombre = %s, apellido = %s, dni = %s, fechaNacimiento = %s, telefono = %s, domicilio = %s 
                   WHERE legajo = %s"""
        values = (nombre, apellido, documento, fecha_nacimiento, telefono, domicilio, alumnoActualizar)
        
        cursor.execute(query, values,)
        conectar.commit()
        print("Datos actualizados correctamente.")
        
    #Si el legajo no existe, no realiza ninguna acción
    else:
        print("No se encontró un alumno con ese Legajo.")
        
# Carga de cursos
def cargaCursos():
    nombreCurso = input("Nombre del curso: ")
    
    query = "INSERT INTO cursos (nombrecurso) VALUES (%s)"
    values = (nombreCurso,)
    
    cursor.execute(query, values)
    conectar.commit()
    
    print("Curso cargado correctamente")
    
# Consulta de cursos
def consultarCursos():
    cursor.execute("SELECT * FROM cursos")
    for(idcursos, nombrecurso,) in cursor.fetchall():
        print(f"ID de curso: {idcursos} \n Nombre: {nombrecurso}")
        print("--------------------")
        

def asignarCursos():
    # Mostrar cursos disponibles
    cursor.execute("SELECT idcursos, nombrecurso FROM cursos")
    cursos = cursor.fetchall()
    

    
    # Solicitar datos de entrada
    legajoAlumno = input("\nIngresar legajo del alumno: ")
    
    # Le muestra al usuario los cursos disponibles
    print("\nCursos disponibles:")
    for curso in cursos:
        print(f"ID: {curso[0]} - Nombre: {curso[1]}")
        
    idCurso = input("Ingrese el ID del curso: ")
    
    
    # Verifica alumno existe
    cursor.execute("SELECT * FROM alumnos WHERE legajo = %s", (legajoAlumno,))
    alumno = cursor.fetchone()
    
    # Verifica si el ID del curso existe
    cursor.execute("SELECT * FROM cursos WHERE idcursos = %s", (idCurso,))
    curso = cursor.fetchone()
    
    if not alumno:
        print("No se encontró un alumno con ese legajo. Verifique el número ingresado.")
        return
    if not curso:
        print("No se encontró un curso con ese ID. Verifique el número ingresado.")
        return
    
    # Se inserta la asignación en una tabla intermedia, para permitir más de un curso por alumno
    query = "INSERT INTO alumno_toma_curso (legajoAlumno, idCurso) VALUES (%s, %s)"
    values = (legajoAlumno, idCurso)
    cursor.execute(query, values)
    conectar.commit()
    
    print("Curso asignado correctamente.")

# Menú
def menu():
    while True:
        print("\n--- Gestión de Alumnos ---")
        print("1. Ingreso de datos")
        print("2. Consulta de datos")
        print("3. Eliminación de datos")
        print("4. Modificación de datos")
        print("5. Ordenamiento numérico por Legajo y listado")
        print("6. Añadir cursos")
        print("7. Consulta de cursos")
        print("8. Asignación de cursos")
        print("9. Salida")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            ingresoDatos()
        elif opcion == '2':
            consultaDatos()
        elif opcion == '3':
            eliminacionDatos()
        elif opcion == '4':
            actualizarDatos()
        elif opcion == '5':
            consultaDatos()
        elif opcion == '6':
            cargaCursos()
        elif opcion == '7':
            consultarCursos()
        elif opcion == '8':
            asignarCursos()
        elif opcion == '9':
            # Cierra todas las conexiones y termina el programa
            print("Cerrando el sistema")
            cursor.close()
            conectar.close()
            break
        else:
            print("Opción no válida. Intente de nuevo.")

# Ejecuta el menú
menu()
