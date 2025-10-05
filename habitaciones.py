import sqlite3

DB_NAME = "hotel.db"

def crear_habitacion(numero, tipo, tarifa):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO habitaciones (numero, tipo, tarifa) VALUES (?, ?, ?)", (numero, tipo, tarifa))
    conn.commit()
    conn.close()
    print("habitacion creada con exito")
    
def listar_habitaciones():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM habitaciones")
    habitaciones = cursor.fetchall()
    conn.close()
    for h in habitaciones:
        print(h)
        
def modificar_habitacion(habitacion_id, nuevo_tipo, nueva_tarifa):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE habitaciones SET tipo=?, tarifa=?, WHERE id=?", (nuevo_tipo, nueva_tarifa, habitacion_id))
    conn.commit()
    conn.close()
    print("habitacion modificada con exito")
    
def eliminar_habitacion(habitacion_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM habitaciones WHERE id=?", (habitacion_id,))
    conn.commit()
    conn.close()    