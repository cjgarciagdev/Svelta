"""
backup.py — Script de respaldo automático de la base de datos INCES
Uso:
    python backup.py          → Crea un backup con timestamp
    python backup.py --list   → Lista los backups existentes
    python backup.py --clean  → Elimina backups con más de 30 días

Se puede programar en el Programador de Tareas de Windows para que corra diariamente.
"""

import shutil
import os
import sys
from datetime import datetime, timedelta

DB_SOURCE = "inces.sqlite"
BACKUP_DIR = "backups"

def crear_backup():
    if not os.path.exists(DB_SOURCE):
        print(f"[ERROR] No se encontró la base de datos '{DB_SOURCE}'.")
        sys.exit(1)

    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    dest = os.path.join(BACKUP_DIR, f"inces_backup_{timestamp}.sqlite")

    shutil.copy2(DB_SOURCE, dest)
    size_kb = os.path.getsize(dest) / 1024
    print(f"[OK] Backup creado: {dest}  ({size_kb:.1f} KB)")
    return dest

def listar_backups():
    if not os.path.exists(BACKUP_DIR):
        print("[INFO] No hay backups aún.")
        return
    archivos = sorted(
        [f for f in os.listdir(BACKUP_DIR) if f.endswith(".sqlite")],
        reverse=True
    )
    if not archivos:
        print("[INFO] No hay backups aún.")
        return
    print(f"\n{'Archivo':<45} {'Tamaño':>10}  {'Fecha'}")
    print("-" * 75)
    for f in archivos:
        path = os.path.join(BACKUP_DIR, f)
        size_kb = os.path.getsize(path) / 1024
        mtime = datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M")
        print(f"{f:<45} {size_kb:>8.1f} KB  {mtime}")
    print(f"\nTotal: {len(archivos)} backup(s)\n")

def limpiar_viejos(dias=30):
    if not os.path.exists(BACKUP_DIR):
        print("[INFO] No hay backups para limpiar.")
        return
    limite = datetime.now() - timedelta(days=dias)
    eliminados = 0
    for f in os.listdir(BACKUP_DIR):
        if not f.endswith(".sqlite"):
            continue
        path = os.path.join(BACKUP_DIR, f)
        mtime = datetime.fromtimestamp(os.path.getmtime(path))
        if mtime < limite:
            os.remove(path)
            print(f"[ELIMINADO] {f}")
            eliminados += 1
    if eliminados == 0:
        print(f"[INFO] No hay backups con más de {dias} días.")
    else:
        print(f"[OK] {eliminados} backup(s) eliminado(s).")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--list":
            listar_backups()
        elif sys.argv[1] == "--clean":
            limpiar_viejos(dias=30)
        else:
            print(f"[ERROR] Argumento desconocido: {sys.argv[1]}")
            print("Uso: python backup.py [--list | --clean]")
    else:
        crear_backup()
