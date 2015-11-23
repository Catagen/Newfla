import os
import click

@click.command()
@click.option('--name', default="FlaskApp", help="The name of your project")
def new_project(name):
    
    if not os.path.isdir(name):

        os.mkdir(name)
        os.chdir(name)

        open('run.py', 'w').write("from app import app\napp.run(debug = True)")
        open('config.py', 'w').write("import os\nbasedir = os.path.abspath(os.path.dirname(__file__))\n\nCSRF_ENABLED = True\nSECRET_KEY = 'superSecret'")

        os.mkdir("app")
        os.chdir("app")

        open('__init__.py', 'w').write("from flask import Flask\nfrom flask.ext.bootstrap import Bootstrap\nfrom flask.ext.moment import Moment\nfrom redis import StrictRedis\n\napp = Flask(__name__)\napp.config.from_object('config')\n\nbootstrap = Bootstrap(app)\nmoment = Moment(app)\nredis = StrictRedis(decode_responses = True)\n\nfrom app import views")
        open('views.py', 'w').write("from flask import render_template, redirect, url_for, request\nfrom app import app, redis\n\n@app.errorhandler(404)\ndef not_found_error(e):\n    return render_template('404.html', e=e), 404\n\n@app.errorhandler(500)\ndef internal_server_error(e):\n    return render_template('500.html', e=e), 500\n\n@app.route('/')\ndef index():\n    return render_template('index.html')\n")

        os.mkdir("templates")
        os.chdir("templates")

        open('404.html', 'w').write("{{ e }}")
        open('500.html', 'w').write("{{ e }}")
        open('base.html', 'w').write("{% extends 'bootstrap/base.html' %}\n\nv{% block html_attribs %} lang='en' {% endblock %}\n\n{% block head %}\n{{ super() }}\n<title>" + name + "</title>\n{% endblock %}\n\n{% block content %}\n<div class='container'>\n{% block container %}\n{% endblock -%}\n</div>\n{% endblock %}\n\n{% block scripts %}\n{{ super() }}\n{{ moment.include_moment() }}\n{{ moment.lang('en') }}\n{% endblock %}")
        open('index.html', 'w').write("{% extends 'base.html' %}\n\n{% block container %}\n<h1 class='text-center'>" + name +  "</h1>\n{% endblock %}\n")

        return print("Success! Use the 'cd " + str(name) + " && python run.py' command to run the application.")

    else:
        return print("A directory named '" + name + "' already exists.")

if __name__ == "__main__":
    new_project()
