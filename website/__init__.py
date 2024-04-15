from flask import Flask, Blueprint
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']= 'hehehe'
    from .views import views
    from .auth import auth
    from .webapi import web_api
    app.register_blueprint(views,url_prefix ='/')
    app.register_blueprint(auth,url_prefix ='/')
    app.register_blueprint(web_api,url_prefix ='/')
    return app