"""
Main entry point for the Lorean application.
"""

import multiprocessing


if __name__ == "__main__":
    multiprocessing.freeze_support()

BANNER = """
Lorean is starting as packaged standalone.
"""

try:
    from .app import create_app
except ImportError:
    from app import create_app

def main():
    """
    Main function for Lorean to start the server.
    """

    print(BANNER)    

    app = create_app(standalone = True)
    app.run()

if __name__ == "__main__":
    main()
