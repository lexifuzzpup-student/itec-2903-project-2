from flask import Flask, render_template, request, send_from_directory

# create the app, labeled using the current filename
app = Flask(__name__)

# define webpage route and callback
@app.route("/")
def homepage():
    return 'hello!'

# run the server if the file is directly executed
if __name__ == "__main__":
    app.run(debug = True)