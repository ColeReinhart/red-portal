from flask import Flask, render_template, request


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DB_NAME='portal',
        DB_USER='portal_user',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from . import db
    db.init_app(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/courses', methods=['GET', 'POST'])
    def courses():
        sub = request.form['Submit']
        if sub:
            print(request.method)
        return render_template('courses.html')



    return app

