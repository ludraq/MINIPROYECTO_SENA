# reservas.py
from database import Database
from datetime import datetime
from habitaciones import Habitacion
from clientes import Cliente

class Reserva:
    """
    Clase que gestiona las reservas del hotel.
    Cumple con los RF-05 y RF-06 de la SRS.
    """

    def __init__(self, cliente_id, habitacion_id, fecha_entrada, fecha_salida):
        self.cliente_id = cliente_id
        self.habitacion_id = habitacion_id
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida

    # --- Métodos principales ---
    @staticmethod
    def crear(reserva):
        db = Database()
        conn = db.conectar()

        # Validar cliente
        cur = db.ejecutar("SELECT id, nombre, apellidos, estado FROM clientes WHERE id=?", (reserva.cliente_id,))
        cliente_row = cur.fetchone() if cur else None
        if not cliente_row:
            print(f" El cliente con ID {reserva.cliente_id} no existe. Primero registre y liste clientes para ver los IDs.")
            db.cerrar()
            return
        if cliente_row[3] != 'activo':
            print(" El cliente existe pero está inactivo.")
            db.cerrar()
            return


        # Validar habitación
        cur = db.ejecutar("SELECT id, tarifa, estado FROM habitaciones WHERE id=?", (reserva.habitacion_id,))
        habitacion = cur.fetchone()
        if not habitacion:
            print(" La habitación no existe.")
            db.cerrar()
            return
        if habitacion[2] != "disponible":
            print(" La habitación no está disponible actualmente.")
            db.cerrar()
            return

        # Validar fechas
        try:
            entrada = datetime.strptime(reserva.fecha_entrada, "%Y-%m-%d")
            salida = datetime.strptime(reserva.fecha_salida, "%Y-%m-%d")
            if salida <= entrada:
                print(" La fecha de salida debe ser posterior a la de entrada.")
                db.cerrar()
                return
        except ValueError:
            print(" Formato de fecha inválido (usa YYYY-MM-DD).")
            db.cerrar()
            return

        # Verificar disponibilidad en esas fechas
        query = """
        SELECT COUNT(*) FROM reservas
        WHERE habitacion_id=?
        AND estado='activa'
        AND NOT (fecha_salida <= ? OR fecha_entrada >= ?)
        """
        # params: habitacion_id, fecha_entrada, fecha_salida
        cur = db.ejecutar(query, (reserva.habitacion_id, reserva.fecha_entrada, reserva.fecha_salida))
        if cur and cur.fetchone()[0] > 0:
            print(" La habitación ya está reservada en ese rango de fechas.")
            db.cerrar()
            return


        # Calcular total (tarifa * noches)
        noches = (salida - entrada).days
        total = habitacion[1] * noches

        # Crear reserva
        query = """
        INSERT INTO reservas (cliente_id, habitacion_id, fecha_entrada, fecha_salida, total, estado)
        VALUES (?, ?, ?, ?, ?, 'activa')
        """
        db.ejecutar(query, (reserva.cliente_id, reserva.habitacion_id,
                            reserva.fecha_entrada, reserva.fecha_salida, total))

        # Cambiar estado de la habitación a ocupado
        Habitacion.cambiar_estado(reserva.habitacion_id, "ocupado")

        print(f" Reserva creada con éxito. Total: ${total:,.0f}")
        Reserva.registrar_log("creacion_reserva", f"Reserva creada para cliente {reserva.cliente_id}.")
        db.cerrar()

    @staticmethod
    def listar():
        db = Database()
        conn = db.conectar()
        cur = db.ejecutar("""
        SELECT r.id, c.nombre || ' ' || c.apellidos AS cliente,
               h.numero, r.fecha_entrada, r.fecha_salida, r.total, r.estado
        FROM reservas r
        JOIN clientes c ON r.cliente_id = c.id
        JOIN habitaciones h ON r.habitacion_id = h.id
        ORDER BY r.id DESC
        """)
        reservas = cur.fetchall()
        db.cerrar()

        print("\n LISTA DE RESERVAS:")
        if not reservas:
            print("No hay reservas registradas.\n")
            return

        for r in reservas:
            print(f"ID: {r[0]} | Cliente: {r[1]} | Habitación: {r[2]} | "
                  f"{r[3]} → {r[4]} | Total: ${r[5]:,.0f} | Estado: {r[6]}")
        print()

    @staticmethod
    def modificar(reserva_id, nueva_entrada=None, nueva_salida=None):
        db = Database()
        conn = db.conectar()

        # Verificar si la reserva existe
        cur = db.ejecutar("""
        SELECT r.id, r.fecha_entrada, r.fecha_salida, h.tarifa
        FROM reservas r
        JOIN habitaciones h ON r.habitacion_id = h.id
        WHERE r.id=?
        """, (reserva_id,))
        reserva = cur.fetchone()

        if not reserva:
            print(" No existe una reserva con ese ID.")
            db.cerrar()
            return

        # Determinar fechas a usar (si no se pasan nuevas, usar las anteriores)
        fecha_entrada = nueva_entrada or reserva[1]
        fecha_salida = nueva_salida or reserva[2]

        # Validar formato de fechas
        try:
            entrada_dt = datetime.strptime(fecha_entrada, "%Y-%m-%d")
            salida_dt = datetime.strptime(fecha_salida, "%Y-%m-%d")
            if salida_dt <= entrada_dt:
                print(" La fecha de salida debe ser posterior a la de entrada.")
                db.cerrar()
                return
        except ValueError:
            print(" Formato de fecha inválido (usa YYYY-MM-DD).")
            db.cerrar()
            return

        # Calcular nuevas noches y total
        noches = (salida_dt - entrada_dt).days
        nueva_tarifa = reserva[3]
        nuevo_total = noches * nueva_tarifa

        # Actualizar reserva con nuevas fechas y nuevo total
        query = """
        UPDATE reservas
        SET fecha_entrada=?, fecha_salida=?, total=?
        WHERE id=?
        """
        db.ejecutar(query, (fecha_entrada, fecha_salida, nuevo_total, reserva_id))

        print(f" Reserva modificada con éxito. Nuevo total: ${nuevo_total:,.0f}")
        Reserva.registrar_log("modificacion", f"Reserva {reserva_id} actualizada a nuevo total ${nuevo_total:,.0f}.")
        db.cerrar()


    @staticmethod
    def cancelar(reserva_id):
        db = Database()
        conn = db.conectar()

        # Verificar si existe
        cur = db.ejecutar("SELECT habitacion_id FROM reservas WHERE id=? AND estado='activa'", (reserva_id,))
        reserva = cur.fetchone()

        if not reserva:
            print(" No se puede cancelar: reserva inexistente o ya cancelada.")
            db.cerrar()
            return

        # Cancelar reserva
        db.ejecutar("UPDATE reservas SET estado='cancelada' WHERE id=?", (reserva_id,))
        # Liberar habitación
        Habitacion.cambiar_estado(reserva[0], "disponible")

        print(" Reserva cancelada correctamente.")
        Reserva.registrar_log("cancelacion", f"Reserva {reserva_id} cancelada.")
        db.cerrar()

    # --- Registro de logs ---
    @staticmethod
    def registrar_log(accion, descripcion):
        db = Database()
        conn = db.conectar()
        db.ejecutar("INSERT INTO logs (usuario, accion, descripcion) VALUES (?, ?, ?)",
                    ("admin", accion, descripcion))
        db.cerrar()


# --- Ejemplo de uso ---
if __name__ == "__main__":
    # Crear una reserva de ejemplo (cliente_id=1, habitacion_id=1)
    reserva = Reserva(1, 1, "2025-10-12", "2025-10-15")
    Reserva.crear(reserva)
    Reserva.listar()

