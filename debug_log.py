# debug_log.py — GuardiánClima ITBA
# Escribe mensajes de debug en debug.log (visible fuera de la TUI)
# Para ver en tiempo real: en otra terminal ejecutar:
#   Windows CMD:  type debug.log  (o abrir el archivo con Notepad mientras corre la app)
#   PowerShell:   Get-Content debug.log -Wait

import os
import traceback
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "debug.log")


def _write(level: str, msg: str) -> None:
    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    line = f"[{ts}] [{level}] {msg}\n"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass   # nunca romper la app por culpa del logger


def info(msg: str)  -> None: _write("INFO ", msg)
def ok(msg: str)    -> None: _write("OK   ", msg)
def warn(msg: str)  -> None: _write("WARN ", msg)
def error(msg: str) -> None: _write("ERROR", msg)


def exc(msg: str, e: Exception) -> None:
    """Loguea excepción con traceback completo."""
    tb = traceback.format_exc()
    _write("ERROR", f"{msg}: {type(e).__name__}: {e}\n{tb}")


def clear() -> None:
    """Borra el log al iniciar la app (llamar desde main.py)."""
    try:
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write(f"=== GuardiánClima debug log — {datetime.now()} ===\n")
    except Exception:
        pass
