import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import debug_log as dbg
from ui.app import GuardianClimaApp

def main():
    dbg.clear()          # borra el log anterior al arrancar
    dbg.info("App iniciada")
    app = GuardianClimaApp()
    app.run()

if __name__ == '__main__':
    main()
