from flaskdss import app
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    app.run(debug=False)
