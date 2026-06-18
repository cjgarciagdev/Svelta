#!/bin/bash
# Este script inicia el servidor web de INCES automáticamente
# y abre el navegador por defecto

cd "$(dirname "$0")"

# Activar el entorno virtual
source venv/bin/activate

# Iniciar el servidor
python3 main.py
