'''
This file is used to run the app
'''
from flaskblog import create_app

app = create_app()

if __name__ == '__main__' :
    # App runs on default addressa and port in debug mode
    # Debug mode supports hot loading
    app.run(debug=True)