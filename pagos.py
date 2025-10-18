# pagos.py
import time
import threading
from database import Database
from reservas import Reserva

class Pago:
    """
    Clase encargada del procesamiento de pagos.
    Cumple con los RF-07 y RF-08 definidos en la SRS.
    """

    def __init__(self, reserva_id, monto, metodo):
        self.reserva_id = reserva_id
        self.monto = monto
        self.metodo = metodo.lower()
        self.estado = "pendiente"

    # --- Métodos principales ---
    @staticmethod
    def validar_metodo(metodo):
        metodos_validos = ["efectivo", "tarjeta", "transferencia"]
        return metodo.lower() in metodos_validos

    def procesar(self):
        """Procesa el pago de forma simulada (asincrónica)."""
        db = Database()
        conn = db.conectar()

        # Validar reserva
        cur = db.ejecutar("SELECT id, total, estado FROM reservas WHERE id=?", (self.reserva_id,))
        reserva = cur.fetchone()
        if not reserva:
            print(" La reserva no existe.")
            db.cerrar()
            return

        if reserva[2] != "activa":
            print(" No se puede pagar una reserva que no está activa.")
            db.cerrar()
            return

        # Validar monto
        if self.monto < reserva[1]:
            print(f" El monto pagado (${self.monto:,.0f}) es inferior al total (${reserva[1]:,.0f}).")
            db.cerrar()
            return

        # Validar método
        if not Pago.validar_metodo(self.metodo):
            print(" Método de pago no válido. Use: efectivo, tarjeta o transferencia.")
            db.cerrar()
            return

        # Insertar el pago en estado 'pendiente'
        db.ejecutar("""
            INSERT INTO pagos (reserva_id, monto, metodo, estado)
            VALUES (?, ?, ?, 'pendiente')
        """, (self.reserva_id, self.monto, self.metodo))

        print(f"💳 Procesando pago de ${self.monto:,.0f} por {self.metodo}...")

        # Simular procesamiento asíncrono
        threading.Thread(target=self.confirmar_pago, args=(self.reserva_id,)).start()

        db.cerrar()

    def confirmar_pago(self, reserva_id):
        """Simula la confirmación del pago después de unos segundos."""
        time.sleep(3)  # Simula espera del procesamiento del banco

        db = Database()
        conn = db.conectar()

        # Confirmar el pago
        db.ejecutar("""
            UPDATE pagos SET estado='confirmado' 
            WHERE reserva_id=? AND estado='pendiente'
        """, (reserva_id,))

        # Cambiar estado de la reserva a 'pagada'
        db.ejecutar("UPDATE reservas SET estado='pagada' WHERE id=?", (reserva_id,))

        db.cerrar()

        print(f" Pago de la reserva {reserva_id} confirmado correctamente.")
        Pago.registrar_log("confirmacion_pago", f"Pago de la reserva {reserva_id} confirmado.")

    @staticmethod
    def listar():
        db = Database()
        conn = db.conectar()
        cur = db.ejecutar("""
        SELECT p.id, r.id, p.monto, p.metodo, p.estado, p.fecha
        FROM pagos p
        JOIN reservas r ON p.reserva_id = r.id
        ORDER BY p.id DESC
        """)
        pagos = cur.fetchall()
        db.cerrar()

        print("\n HISTORIAL DE PAGOS:")
        if not pagos:
            print("No se han realizado pagos.\n")
            return

        for p in pagos:
            print(f"Pago ID: {p[0]} | Reserva: {p[1]} | Monto: ${p[2]:,.0f} | "
                  f"Método: {p[3]} | Estado: {p[4]} | Fecha: {p[5]}")
        print()

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
    # Crear un pago de ejemplo (para la reserva 1)
    pago = Pago(1, 540000, "tarjeta")
    pago.procesar()
    time.sleep(5)
    Pago.listar()

