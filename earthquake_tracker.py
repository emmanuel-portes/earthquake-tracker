import os

from app import create_app

from app.routes.features_route import feature
from app.exceptions.features_exception import error

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')

app.register_blueprint(feature)
app.register_blueprint(error)

if __name__ == "__main__":
    app.run()

 