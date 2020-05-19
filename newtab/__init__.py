import os

from flask import Flask


app = Flask(__name__, instance_relative_config=True)

if not os.path.isdir(app.instance_path):
    os.makedirs(app.instance_path)

app.config.from_object('config.DevelopmentConfig')
if os.path.isfile(os.path.join(app.instance_path, 'config.py')):
    app.config.from_pyfile('config.py')


import newtab.clock  # noqa: E402
import newtab.weather  # noqa: E402
import newtab.wifi  # noqa: E402
import newtab.views  # noqa: E402,F401
