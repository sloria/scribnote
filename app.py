
from werkzeug.wsgi import DispatcherMiddleware

from server.app.settings import DevConfig
from server.app.factory import create_app as create_api
from client.app import create_app

app = create_app()
api = create_api(DevConfig)
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/api': api
})

if __name__ == '__main__':
    app.run(debug=True)
