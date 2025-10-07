# Sistema de Gestión de Reservas - Sprint 1

Este proyecto es un prototipo simple para gestionar habitaciones y reservas de un hotel.

## Contenido
- `src/database.py`: Crea las tablas de la base de datos (habitaciones y reservas).
- `src/reservas.py`: Funciones para crear, listar, modificar y cancelar reservas.
- `docs/`: Carpeta para documentación adicional.

## Cómo usar
1. Ejecuta `database.py` una vez para crear la base de datos:
   ```bash
   python src/database.py
   ```

2. Usa las funciones en `reservas.py` para manejar reservas:
   ```python
   from reservas import crear_reserva, listar_reservas, modificar_reserva, cancelar_reserva

   crear_reserva("Juan Perez", 1, "2025-10-01")
   listar_reservas()
   modificar_reserva(1, "2025-10-02")
   cancelar_reserva(1)
   ```

## Sprint 1 - Objetivo cumplido
- Registrar habitaciones y reservas básicas en SQLite.
- CRUD simple de reservas.
