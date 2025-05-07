from flask import Flask, send_file
import argparse
import os

def create_app(directory):
    app = Flask(__name__)
    app.config['DIRECTORY'] = directory
    @app.route('/<path:filename>', methods=['GET'])
    def serve_file(filename):
        file_path = os.path.join(app.config['DIRECTORY'], filename)
        if not os.path.isfile(file_path):
            return "File not found", 404
        return send_file(file_path,mimetype="text/html")

    return app

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Simple HTTP file server.')
    argparser.add_argument('directory', type=str, help='Directory to serve files from')
    argparser.add_argument('--port', type=int, default=8080, help='Port to run the server on')
    args = argparser.parse_args()
    directory = args.directory
    port = args.port
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        exit(1)
    if not os.path.isdir(directory):
        print(f"Path '{directory}' is not a directory.")
        exit(1)
    app = create_app(directory)
    print(f"Serving files from '{directory}' on http://localhost:{port}")
    
    app.run("127.0.0.1", port=port, debug=False)