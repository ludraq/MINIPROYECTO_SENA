# clientes.py
from database import Database

class Cliente:
    """
    Clase para gestionar los clientes del sistema de reservas del hotel.
    Cumple con los RF-01 y RF-02 definidos en la SRS.
    """

    def __init__(self, nombre, apellidos, documento, correo="", telefono="", direccion=""):
        self.nombre = nombre.strip().title()
        self.apellidos = apellidos.strip().title()
        self.documento = documento.strip()
        self.correo = correo.strip()
        self.telefono = telefono.strip()
        self.direccion = direccion.strip()

    # --- Métodos de clase (interactúan con la base de datos) ---
    @staticmethod
    def registrar(cliente):
        db = Database()
        conn = db.conectar()

        # Verificar si el cliente ya existe
        cur = db.ejecutar("SELECT * FROM clientes WHERE documento=?", (cliente.documento,))
        if cur.fetchone():
            print("⚠️ Ya existe un cliente con ese documento.")
            db.cerrar()
            return

        query = """
        INSERT INTO clientes (nombre, apellidos, documento, correo, telefono, direccion)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (cliente.nombre, cliente.apellidos, cliente.documento,
                  cliente.correo, cliente.telefono, cliente.direccion)

        db.ejecutar(query, params)
        print(f"✅ Cliente '{cliente.nombre} {cliente.apellidos}' registrado correctamente.")
        Cliente.registrar_log("registro", f"Cliente {cliente.documento} registrado.")
        db.cerrar()

    @staticmethod
    def listar():
        db = Database()
        conn = db.conectar()
        cur = db.ejecutar("SELECT id, nombre, apellidos, documento, estado FROM clientes")
        clientes = cur.fetchall()
        db.cerrar()

        print("\n📋 LISTA DE CLIENTES REGISTRADOS:")
        if not clientes:
            print("No hay clientes registrados.\n")
            return

        for c in clientes:
            print(f"ID: {c[0]} | {c[1]} {c[2]} | Doc: {c[3]} | Estado: {c[4]}")
        print()

    @staticmethod
    def consultar_por_documento(documento):
        db = Database()
        conn = db.conectar()
        cur = db.ejecutar("SELECT * FROM clientes WHERE documento=?", (documento,))
        cliente = cur.fetchone()
        db.cerrar()

        if cliente:
            print("\n🔍 Cliente encontrado:")
            print(f"ID: {cliente[0]}\nNombre: {cliente[1]} {cliente[2]}\nDocumento: {cliente[3]}")
            print(f"Correo: {cliente[4]}\nTeléfono: {cliente[5]}\nDirección: {cliente[6]}\nEstado: {cliente[7]}\n")
        else:
            print("❌ No se encontró un cliente con ese documento.")

    @staticmethod
    def actualizar(documento, nuevo_correo=None, nuevo_telefono=None, nueva_direccion=None):
        db = Database()
        conn = db.conectar()
        cur = db.ejecutar("SELECT id FROM clientes WHERE documento=?", (documento,))
        cliente = cur.fetchone()

        if not cliente:
            print("❌ No existe un cliente con ese documento.")
            db.cerrar()
            return

        query = """
        UPDATE clientes
        SET correo = COALESCE(?, correo),
            telefono = COALESCE(?, telefono),
            direccion = COALESCE(?, direccion)
        WHERE documento = ?
        """
        db.ejecutar(query, (nuevo_correo, nuevo_telefono, nueva_direccion, documento))
        print(f"✅ Cliente con documento {documento} actualizado correctamente.")
        Cliente.registrar_log("actualizacion", f"Cliente {documento} actualizado.")
        db.cerrar()

    @staticmethod
    def desactivar(documento):
        db = Database()
        conn = db.conectar()
        cur = db.ejecutar("SELECT id FROM clientes WHERE documento=?", (documento,))
        cliente = cur.fetchone()

        if not cliente:
            print("❌ No existe un cliente con ese documento.")
            db.cerrar()
            return

        db.ejecutar("UPDATE clientes SET estado='inactivo' WHERE documento=?", (documento,))
        print(f"⚙️ Cliente con documento {documento} ha sido desactivado.")
        Cliente.registrar_log("desactivacion", f"Cliente {documento} desactivado.")
        db.cerrar()

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
    nuevo_cliente = Cliente("Juan", "Pérez", "123456789", "juan@example.com", "3001112233", "Calle 123")
    Cliente.registrar(nuevo_cliente)
    Cliente.listar()
    Cliente.consultar_por_documento("123456789")
    Cliente.actualizar("123456789", nuevo_correo="juanp@correo.com")
    Cliente.desactivar("123456789")
