# database.py
import sqlite3
from sqlite3 import Error

class Database:
    """
    Clase encargada de la conexión y operaciones con la base de datos del hotel.
    Cumple con el modelo de datos definido en la SRS del proyecto Hotel Transilvania.
    """

    def __init__(self, db_name="hotel.db"):
        self.db_name = db_name
        self.conn = None

    def conectar(self):
        """Establece la conexión con la base de datos."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            return self.conn
        except Error as e:
            print(f" Error al conectar con la base de datos: {e}")
            return None

    def cerrar(self):
        """Cierra la conexión activa."""
        if self.conn:
            self.conn.close()

    def ejecutar(self, query, params=()):
        """
        Ejecuta una consulta SQL con parámetros opcionales.
        """
        try:
            cur = self.conn.cursor()
            cur.execute(query, params)
            self.conn.commit()
            return cur
        except Error as e:
            print(f" Error al ejecutar la consulta: {e}")
            return None

    def crear_tablas(self):
        """Crea todas las tablas necesarias según la SRS."""
        tablas = {
            "clientes": """
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellidos TEXT NOT NULL,
                    documento TEXT UNIQUE NOT NULL,
                    correo TEXT,
                    telefono TEXT,
                    direccion TEXT,
                    estado TEXT DEFAULT 'activo'
                )
            """,
            "habitaciones": """
                CREATE TABLE IF NOT EXISTS habitaciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero TEXT UNIQUE NOT NULL,
                    tipo TEXT NOT NULL,
                    tarifa REAL NOT NULL,
                    estado TEXT DEFAULT 'disponible'
                )
            """,
            "reservas": """
                CREATE TABLE IF NOT EXISTS reservas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id INTEGER NOT NULL,
                    habitacion_id INTEGER NOT NULL,
                    fecha_entrada TEXT NOT NULL,
                    fecha_salida TEXT NOT NULL,
                    total REAL NOT NULL,
                    estado TEXT DEFAULT 'activa',
                    FOREIGN KEY (cliente_id) REFERENCES clientes (id),
                    FOREIGN KEY (habitacion_id) REFERENCES habitaciones (id)
                )
            """,
            "pagos": """
                CREATE TABLE IF NOT EXISTS pagos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    reserva_id INTEGER NOT NULL,
                    monto REAL NOT NULL,
                    metodo TEXT NOT NULL,
                    estado TEXT DEFAULT 'pendiente',
                    fecha TEXT DEFAULT (datetime('now')),
                    FOREIGN KEY (reserva_id) REFERENCES reservas (id)
                )
            """,
            "logs": """
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT,
                    accion TEXT NOT NULL,
                    descripcion TEXT,
                    fecha TEXT DEFAULT (datetime('now'))
                )
            """
        }

        for nombre, query in tablas.items():
            self.ejecutar(query)
            print(f" Tabla '{nombre}' verificada o creada.")

        print("\n Base de datos inicializada correctamente.\n")

# --- Ejecución directa (solo si se ejecuta este archivo) ---
if __name__ == "__main__":
    db = Database()
    db.conectar()
    db.crear_tablas()
    db.cerrar()
