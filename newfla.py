import click
import shutil
import platform
from os import path, mkdir, chdir, system, remove

def read_packages():
    packages = ""
    for package in open('packages', 'r').read().split('\n'):
        if package != '':
            packages += " " + package

    return packages

def create_app_structure(name):
    # Create run.py and config.py in the root directory
    open('run.py', 'w').write("from app import app\napp.run(debug = True)")
    open('config.py', 'w').write("import os\nbasedir = os.path.abspath(os.path.dirname(__file__))\n\nCSRF_ENABLED = True\nSECRET_KEY = 'superSecret'")
    # Create an app directory and enter it
    mkdir("app")
    chdir("app")
    # Create views.py and __init__.py in the app directory
    open('__init__.py', 'w').write("from flask import Flask\nfrom flask.ext.bootstrap import Bootstrap\nfrom flask.ext.moment import Moment\nfrom redis import StrictRedis\n\napp = Flask(__name__)\napp.config.from_object('config')\n\nbootstrap = Bootstrap(app)\nmoment = Moment(app)\nredis = StrictRedis(decode_responses = True)\n\nfrom app import views")
    open('views.py', 'w').write("from flask import render_template, redirect, url_for, request\nfrom app import app, redis\n\n@app.errorhandler(404)\ndef not_found_error(e):\n    return render_template('404.html', e=e), 404\n\n@app.errorhandler(500)\ndef internal_server_error(e):\n    return render_template('500.html', e=e), 500\n\n@app.route('/')\ndef index():\n    return render_template('index.html')\n")
    # Create template directory
    mkdir("templates")
    chdir("templates")
    # Create basic html files (404, 500, base and index)
    open('404.html', 'w').write("{{ e }}")
    open('500.html', 'w').write("{{ e }}")
    open('base.html', 'w').write("{% extends 'bootstrap/base.html' %}\n\nv{% block html_attribs %} lang='en' {% endblock %}\n\n{% block head %}\n{{ super() }}\n<title>" + name + "</title>\n{% endblock %}\n\n{% block content %}\n<div class='container'>\n{% block container %}\n{% endblock -%}\n</div>\n{% endblock %}\n\n{% block scripts %}\n{{ super() }}\n{{ moment.include_moment() }}\n{{ moment.lang('en') }}\n{% endblock %}")
    open('index.html', 'w').write("{% extends 'base.html' %}\n\n{% block container %}\n<h1 class='text-center'>" + name +  "</h1>\n{% endblock %}\n")

@click.command()
@click.option('--name', default="FlaskApp", help="The name of your project")
def new_project(name):

    if not path.isdir(name):

        # Determine the users operating system
        operating = platform.system()

        # Read the packages file
        packages = read_packages()

        # Make the new directory for the app and copy the pyvenv file to avoid browsing system differently for different operating systems
        mkdir(name)
        shutil.copy2('pyvenv.py', name + '/pyvenv.py')

        # Create a virtual environment with the pyvenv script and then delete pyvenv.py
        chdir(name)
        system("python pyvenv.py venv")
        remove('pyvenv.py')

        # Activate the venv, install all the packages listed in the package file
        system("cd venv/Scripts && activate && pip install" + packages)

        # Create the app structure (python and html files)
        create_app_structure(name)

        # Print a help message according to operating system
        if "win" in operating.lower():
            if input("\nSuccessfully set up! Would you like to run the app now? y/n: ").lower() == "y":
                system("cd.. && cd.. && " + "venv\\Scripts\\activate.bat && python " + "run.py")
            else:
                return print("Use the '" + str(name) + "\\venv\\Scripts\\activate.bat && python " + str(name) + "\\run.py' command to run the application")
        elif "os" or "linux" in operating.lower():
            return print("\nSuccess! Activate the script by going to the venv directory and then run the 'run.py' script")

    else:
        return print("A directory named '" + name + "' already exists.")

if __name__ == "__main__":
    new_project()
