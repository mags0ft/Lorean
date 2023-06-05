import multiprocessing

if __name__ == "__main__":
    multiprocessing.freeze_support()

BANNER = '''
Lorean is starting as packaged standalone.
'''

try:
    from .app import create_app
except ImportError:
    from app import create_app
    
if __name__ == "__main__":
    print(BANNER)    

    app = create_app(standalone = True)
    app.run()