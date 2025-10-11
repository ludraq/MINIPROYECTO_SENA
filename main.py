# main.py
from clientes import Cliente
from habitaciones import Habitacion
from reservas import Reserva
from pagos import Pago
import time

class SistemaHotel:
    """
    Sistema de gestión del Hotel Transilvania.
    Integra los módulos de Clientes, Habitaciones, Reservas y Pagos.
    """

    @staticmethod
    def menu_principal():
        while True:
            print("\n===== 🏨 SISTEMA DE GESTIÓN HOTEL TRANSILVANIA =====")
            print("1. Gestión de Clientes")
            print("2. Gestión de Habitaciones")
            print("3. Gestión de Reservas")
            print("4. Pagos")
            print("0. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                SistemaHotel.menu_clientes()
            elif opcion == "2":
                SistemaHotel.menu_habitaciones()
            elif opcion == "3":
                SistemaHotel.menu_reservas()
            elif opcion == "4":
                SistemaHotel.menu_pagos()
            elif opcion == "0":
                print("👋 Gracias por usar el sistema. Hasta pronto.")
                break
            else:
                print("❌ Opción no válida.")

    # --- MENÚ CLIENTES ---
    @staticmethod
    def menu_clientes():
        while True:
            print("\n📂 GESTIÓN DE CLIENTES")
            print("1. Registrar cliente")
            print("2. Listar clientes")
            print("3. Consultar cliente por documento")
            print("4. Actualizar datos de cliente")
            print("5. Desactivar cliente")
            print("0. Volver al menú principal")
            op = input("Seleccione una opción: ")

            if op == "1":
                nombre = input("Nombre: ")
                apellidos = input("Apellidos: ")
                documento = input("Documento: ")
                correo = input("Correo: ")
                telefono = input("Teléfono: ")
                direccion = input("Dirección: ")
                nuevo = Cliente(nombre, apellidos, documento, correo, telefono, direccion)
                Cliente.registrar(nuevo)

            elif op == "2":
                Cliente.listar()

            elif op == "3":
                doc = input("Documento del cliente: ")
                Cliente.consultar_por_documento(doc)

            elif op == "4":
                doc = input("Documento del cliente: ")
                nuevo_correo = input("Nuevo correo (Enter para omitir): ") or None
                nuevo_telefono = input("Nuevo teléfono (Enter para omitir): ") or None
                nueva_direccion = input("Nueva dirección (Enter para omitir): ") or None
                Cliente.actualizar(doc, nuevo_correo, nuevo_telefono, nueva_direccion)

            elif op == "5":
                doc = input("Documento del cliente a desactivar: ")
                Cliente.desactivar(doc)

            elif op == "0":
                break
            else:
                print("❌ Opción no válida.")

    # --- MENÚ HABITACIONES ---
    @staticmethod
    def menu_habitaciones():
        while True:
            print("\n🛏️ GESTIÓN DE HABITACIONES")
            print("1. Registrar habitación")
            print("2. Listar habitaciones")
            print("3. Actualizar habitación")
            print("4. Eliminar habitación")
            print("0. Volver al menú principal")
            op = input("Seleccione una opción: ")

            if op == "1":
                numero = input("Número de habitación: ")
                tipo = input("Tipo: ")
                tarifa = float(input("Tarifa: "))
                nueva = Habitacion(numero, tipo, tarifa)
                Habitacion.registrar(nueva)

            elif op == "2":
                Habitacion.listar()

            elif op == "3":
                numero = input("Número de habitación: ")
                nuevo_tipo = input("Nuevo tipo (Enter para omitir): ") or None
                nueva_tarifa = input("Nueva tarifa (Enter para omitir): ")
                nueva_tarifa = float(nueva_tarifa) if nueva_tarifa else None
                nuevo_estado = input("Nuevo estado (disponible/ocupado/mantenimiento) o Enter para omitir: ") or None
                Habitacion.actualizar(numero, nuevo_tipo, nueva_tarifa, nuevo_estado)

            elif op == "4":
                numero = input("Número de habitación a eliminar: ")
                Habitacion.eliminar(numero)

            elif op == "0":
                break
            else:
                print("❌ Opción no válida.")

    # --- MENÚ RESERVAS ---
    @staticmethod
    def menu_reservas():
        while True:
            print("\n📅 GESTIÓN DE RESERVAS")
            print("1. Crear reserva")
            print("2. Listar reservas")
            print("3. Modificar reserva")
            print("4. Cancelar reserva")
            print("0. Volver al menú principal")
            op = input("Seleccione una opción: ")

            if op == "1":
                cliente_id = int(input("ID del cliente: "))
                habitacion_id = int(input("ID de la habitación: "))
                fecha_entrada = input("Fecha de entrada (YYYY-MM-DD): ")
                fecha_salida = input("Fecha de salida (YYYY-MM-DD): ")
                nueva = Reserva(cliente_id, habitacion_id, fecha_entrada, fecha_salida)
                Reserva.crear(nueva)

            elif op == "2":
                Reserva.listar()

            elif op == "3":
                id_r = int(input("ID de la reserva a modificar: "))
                nueva_entrada = input("Nueva fecha de entrada (Enter para omitir): ") or None
                nueva_salida = input("Nueva fecha de salida (Enter para omitir): ") or None
                Reserva.modificar(id_r, nueva_entrada, nueva_salida)

            elif op == "4":
                id_r = int(input("ID de la reserva a cancelar: "))
                Reserva.cancelar(id_r)

            elif op == "0":
                break
            else:
                print("❌ Opción no válida.")

    # --- MENÚ PAGOS ---
    @staticmethod
    def menu_pagos():
        while True:
            print("\n💳 GESTIÓN DE PAGOS")
            print("1. Registrar pago")
            print("2. Listar pagos")
            print("0. Volver al menú principal")
            op = input("Seleccione una opción: ")

            if op == "1":
                reserva_id = int(input("ID de la reserva: "))
                monto = float(input("Monto del pago: "))
                metodo = input("Método (efectivo / tarjeta / transferencia): ")
                pago = Pago(reserva_id, monto, metodo)
                pago.procesar()
                time.sleep(4)  # Permitir que el hilo confirme el pago

            elif op == "2":
                Pago.listar()

            elif op == "0":
                break
            else:
                print("❌ Opción no válida.")


# --- Ejecución principal ---
if __name__ == "__main__":
    SistemaHotel.menu_principal()


