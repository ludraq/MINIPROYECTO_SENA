# habitaciones.py
from database import Database

class Habitacion:
    """
    Clase que gestiona las habitaciones del hotel.
    Cumple con los requisitos RF-03 y RF-04 de la SRS.
    """

    def __init__(self, numero, tipo, tarifa, estado="disponible"):
        self.numero = numero.strip()
        self.tipo = tipo.strip().title()
        self.tarifa = tarifa
        self.estado = estado.strip().lower()

    # --- Métodos principales (CRUD) ---
    @staticmethod
    def registrar(habitacion):
        db = Database()
        conn = db.conectar()

        # Validar duplicado
        cur = db.ejecutar("SELECT id FROM habitaciones WHERE numero=?", (habitacion.numero,))
        if cur.fetchone():
            print("⚠️ Ya existe una habitación con ese número.")
            db.cerrar()
            return

        query = """
        INSERT INTO habitaciones (numero, tipo, tarifa, estado)
        VALUES (?, ?, ?, ?)
        """
        db.ejecutar(query, (habitacion.numero, habitacion.tipo, habitacion.tarifa, habitacion.estado))
        print(f"✅ Habitación {habitacion.numero} registrada correctamente.")
        Habitacion.registrar_log("registro", f"Habitación {habitacion.numero} creada.")
        db.cerrar()

    @staticmethod
    def listar():
        db = Database()
        conn = db.conectar()
        cur = db.ejecutar("SELECT id, numero, tipo, tarifa, estado FROM habitaciones ORDER BY numero ASC")
        habitaciones = cur.fetchall()
        db.cerrar()

        print("\n🏨 LISTA DE HABITACIONES:")
        if not habitaciones:
            print("No hay habitaciones registradas.\n")
            return

        for h in habitaciones:
            print(f"ID: {h[0]} | Nº {h[1]} | Tipo: {h[2]} | Tarifa: ${h[3]:,.0f} | Estado: {h[4]}")
        print()

    @staticmethod
    def actualizar(numero, nuevo_tipo=None, nueva_tarifa=None, nuevo_estado=None):
        db = Database()
        conn = db.conectar()

        cur = db.ejecutar("SELECT id FROM habitaciones WHERE numero=?", (numero,))
        habitacion = cur.fetchone()

        if not habitacion:
            print("❌ No existe una habitación con ese número.")
            db.cerrar()
            return

        query = """
        UPDATE habitaciones
        SET tipo = COALESCE(?, tipo),
            tarifa = COALESCE(?, tarifa),
            estado = COALESCE(?, estado)
        WHERE numero = ?
        """
        db.ejecutar(query, (nuevo_tipo, nueva_tarifa, nuevo_estado, numero))
        print(f"✅ Habitación {numero} actualizada correctamente.")
        Habitacion.registrar_log("actualizacion", f"Habitación {numero} modificada.")
        db.cerrar()

    @staticmethod
    def eliminar(numero):
        db = Database()
        conn = db.conectar()

        cur = db.ejecutar("SELECT id FROM habitaciones WHERE numero=?", (numero,))
        habitacion = cur.fetchone()

        if not habitacion:
            print("❌ No existe una habitación con ese número.")
            db.cerrar()
            return

        db.ejecutar("DELETE FROM habitaciones WHERE numero=?", (numero,))
        print(f"🗑️ Habitación {numero} eliminada del sistema.")
        Habitacion.registrar_log("eliminacion", f"Habitación {numero} eliminada.")
        db.cerrar()

    @staticmethod
    def cambiar_estado(identificador, nuevo_estado):
        """
        Cambia el estado de la habitación.
        - Si 'identificador' es int o puede convertirse a int -> busca por id.
        - Si es texto -> busca por numero.
        """
        db = Database()
        conn = db.conectar()
        try:
            # Intentar tratar identificador como id (int)
            id_val = int(identificador)
            db.ejecutar("UPDATE habitaciones SET estado=? WHERE id=?", (nuevo_estado, id_val))
        except (ValueError, TypeError):
            # No es int -> usar numero
            db.ejecutar("UPDATE habitaciones SET estado=? WHERE numero=?", (nuevo_estado, identificador))
        Habitacion.registrar_log("cambio_estado", f"Habitación {identificador} cambió a '{nuevo_estado}'.")
        db.cerrar()


    @staticmethod
    def obtener_disponibles():
        """Devuelve una lista de habitaciones disponibles (para futuras reservas)."""
        db = Database()
        conn = db.conectar()
        cur = db.ejecutar("SELECT id, numero, tipo, tarifa FROM habitaciones WHERE estado='disponible'")
        disponibles = cur.fetchall()
        db.cerrar()
        return disponibles

    # --- Registro de logs ---
    @staticmethod
    def registrar_log(accion, descripcion):
        db = Database()
        conn = db.conectar()
        db.ejecutar("INSERT INTO logs (usuario, accion, descripcion) VALUES (?, ?, ?)",
                    ("admin", accion, descripcion))
        db.cerrar()


# --- Ejemplo de uso (solo si se ejecuta directamente) ---
if __name__ == "__main__":
    # Crear y registrar una habitación
    nueva_habitacion = Habitacion("101", "Suite", 180000)
    Habitacion.registrar(nueva_habitacion)

    # Listar habitaciones
    Habitacion.listar()

    # Actualizar habitación
    Habitacion.actualizar("101", nueva_tarifa=200000, nuevo_estado="ocupado")

    # Ver habitaciones disponibles
    print("\nHabitaciones disponibles:")
    for h in Habitacion.obtener_disponibles():
        print(h)

    # Eliminar habitación
    # Habitacion.eliminar("101")

