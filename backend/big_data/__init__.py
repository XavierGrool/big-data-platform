import os

from flask import Flask
from flask_cors import CORS

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'big-data.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # cors config
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import test
    app.register_blueprint(test.bp)

    from . import login
    app.register_blueprint(login.bp)

    from . import user
    app.register_blueprint(user.bp)

    from . import project
    app.register_blueprint(project.bp)

    from . import help
    app.register_blueprint(help.bp)

    from . import dataset
    app.register_blueprint(dataset.bp)

    from . import model
    app.register_blueprint(model.bp)

    from . import addModel
    app.register_blueprint(addModel.bp)

    from . import prediction
    app.register_blueprint(prediction.bp)

    return app