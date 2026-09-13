import os
import sys

from streamlit.web.cli import main

if __name__ == "__main__":
    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    sys.argv = ["streamlit", "run", app_path, "--global.developmentMode=false"]
    main()