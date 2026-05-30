import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.app import GuardianClimaApp

def main():
    app = GuardianClimaApp()
    app.run()

if __name__ == '__main__':
    main()
