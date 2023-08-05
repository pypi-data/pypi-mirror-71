import os

from fogstone.app import create_app

host = os.getenv('HOST')
port = os.getenv('PORT')
debug = 'DEBUG' in os.environ

app = create_app()

if __name__ == '__main__':
    app.run(debug=debug, host=host, port=port)
