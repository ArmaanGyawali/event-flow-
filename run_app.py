import sys
import os
import threading
import time
import webbrowser
from streamlit.web import cli as stcli

if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    app_path = os.path.join(base_path, "app.py")
    os.chdir(base_path)
    
    # Automatically open the browser tab after 2 seconds once Streamlit spins up
    def open_browser():
        time.sleep(2)
        webbrowser.open("http://localhost:8501")
        
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run Streamlit directly on the main thread (satisfies all signal thread restrictions)
    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--server.port=8501",
        "--server.headless=true",
        "--server.fileWatcherType=none",
        "--global.developmentMode=false"
    ]
    sys.exit(stcli.main())