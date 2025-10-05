# main.py
from habitaciones import crear_habitacion, listar_habitaciones, modificar_habitacion, eliminar_habitacion
from reservas import crear_reserva, listar_reservas, modificar_reserva, cancelar_reserva

def menu():
    while True:
        print("\n===== SISTEMA DE RESERVAS - HOTEL =====")
        print("1. Crear habitación")
        print("2. Listar habitaciones")
        print("3. Modificar habitación")
        print("4. Eliminar habitación")
        print("5. Crear reserva")
        print("6. Listar reservas")
        print("7. Modificar reserva")
        print("8. Cancelar reserva")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            numero = input("Número de habitación: ")
            tipo = input("Tipo de habitación: ")
            tarifa = float(input("Tarifa: "))
            crear_habitacion(numero, tipo, tarifa)

        elif opcion == "2":
            listar_habitaciones()

        elif opcion == "3":
            id_h = int(input("ID de la habitación a modificar: "))
            nuevo_tipo = input("Nuevo tipo: ")
            nueva_tarifa = float(input("Nueva tarifa: "))
            modificar_habitacion(id_h, nuevo_tipo, nueva_tarifa)

        elif opcion == "4":
            id_h = int(input("ID de la habitación a eliminar: "))
            eliminar_habitacion(id_h)

        elif opcion == "5":
            cliente = input("Nombre del cliente: ")
            habitacion_id = int(input("ID de la habitación: "))
            fecha = input("Fecha (YYYY-MM-DD): ")
            crear_reserva(cliente, habitacion_id, fecha)

        elif opcion == "6":
            listar_reservas()

        elif opcion == "7":
            id_r = int(input("ID de la reserva a modificar: "))
            nueva_fecha = input("Nueva fecha (YYYY-MM-DD): ")
            modificar_reserva(id_r, nueva_fecha)

        elif opcion == "8":
            id_r = int(input("ID de la reserva a cancelar: "))
            cancelar_reserva(id_r)

        elif opcion == "0":
            print("👋 Saliendo del sistema...")
            break
        else:
            print("❌ Opción no válida.")

if __name__ == "__main__":
    menu()
