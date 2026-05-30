import sqlite3
from database.db import init_db, get_all_estudiantes
from utils.report_generator import generate_estudiantes_report, generate_estudiantes_xlsx_report

init_db()

try:
    # 1. Obtener estudiantes de la base de datos
    data = get_all_estudiantes()
    data_list = list(data)
    print(f"Estudiantes encontrados en la base de datos: {len(data_list)}")
    
    # Si no hay datos, crear datos de prueba mock
    if len(data_list) == 0:
        print("La base de datos está vacía. Usando datos mock para la prueba...")
        data_list = [
            {
                "id": 1,
                "cedula": "12345678",
                "nombres": "Pedro Jose",
                "apellidos": "Perez Lopez",
                "perfil_nombre": "Herreria",
                "telefono": "+58 4121234567",
                "estado_inscripcion": "INSCRITO",
                "genero": "MASCULINO",
                "fecha_censo": "15/02/2026 10:00:00" # Trimestre 1
            },
            {
                "id": 2,
                "cedula": "87654321",
                "nombres": "Maria Gomez",
                "apellidos": "Rodriguez Diaz",
                "perfil_nombre": "Costura",
                "telefono": "+58 4169876543",
                "estado_inscripcion": "CENSADO",
                "genero": "FEMENINO",
                "fecha_censo": "20/05/2026 14:30:00" # Trimestre 2
            },
            {
                "id": 3,
                "cedula": "23456789",
                "nombres": "Carlos Alberto",
                "apellidos": "Martinez Ruiz",
                "perfil_nombre": "Computacion",
                "telefono": None,
                "estado_inscripcion": "RETIRADO",
                "genero": "MASCULINO",
                "fecha_censo": "10/08/2026 09:15:00" # Trimestre 3
            }
        ]

    # 2. Probar generación de PDF
    print("\nGenerando reporte PDF...")
    pdf_path = generate_estudiantes_report(data_list)
    print(f"[OK] Reporte PDF generado correctamente en: {pdf_path}")

    # 3. Probar generación de Excel
    print("\nGenerando reporte Excel...")
    xlsx_path = generate_estudiantes_xlsx_report(data_list)
    print(f"[OK] Reporte Excel generado correctamente en: {xlsx_path}")
    
    print("\n¡Verificación completada con éxito!")

except Exception as e:
    print(f"\n[ERROR] Ocurrió un fallo durante la verificación: {e}")
    import traceback
    traceback.print_exc()
