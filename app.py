from flask import Flask, render_template, request, redirect
from appinit import app
import routes

if __name__ == '__main__':  # python interpreter assigns "__main__" to the file you run
    app.run(debug=True)
