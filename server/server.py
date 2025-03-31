from flask import Flask, request, Response
from jsonrpcserver import method, dispatch, Success


app = Flask(__name__)

@method
def hello():
    msg = "Hello :D"
    print(msg)
    return Success(msg)

@app.route("/rpc", methods=["POST"])
def index():
    req = request.get_data().decode()
    response = dispatch(req)

    print(response)
    return Response(str(response), 200, mimetype="application/json")

if __name__ == "__main__":
    server_address = 'localhost'
    port = 5000
    print(f"Starting JSON-RPC server on http://{server_address}:{port}...")
    app.run(host=server_address, port=port, debug=True) # Set debug=True for development