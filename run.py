from flaskblog import app


# This is used to run the app by: python filename.py
if __name__ == '__main__' :
    # App runs on default addressa and port in debug mode
    # Debug mode supports hot loading
    app.run(debug=True)