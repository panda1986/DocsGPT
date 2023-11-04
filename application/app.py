import platform
import dotenv
from application.celery import celery
from flask import Flask, request, redirect
from application.core.settings import settings
from application.api.user.routes import user
from application.api.answer.routes import answer
from application.api.internal.routes import internal
import logging, pathlib

if platform.system() == "Windows":
    import pathlib
    pathlib.PosixPath = pathlib.WindowsPath

dotenv.load_dotenv()

# get current directory
current_dir = pathlib.Path(__file__).parent.absolute()
root_dir = current_dir.parent.absolute()
static_dir = pathlib.Path(root_dir, "static-dir")
logging.info("current_dir:%s, root_dir:%s, static_dir:%s" % (current_dir, root_dir, static_dir))

app = Flask(__name__, static_folder=str(static_dir))
app.register_blueprint(user)
app.register_blueprint(answer)
app.register_blueprint(internal)
app.config.update(
    UPLOAD_FOLDER="inputs",
    CELERY_BROKER_URL=settings.CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND=settings.CELERY_RESULT_BACKEND,
    MONGO_URI=settings.MONGO_URI
)
celery.config_from_object("application.celeryconfig")

# serve static-dir files
@app.route('/')
def index():
    logging.info("index, request.remote_addr:%s" % request.remote_addr)
    return app.send_static_file('index.html')
@app.route('/<path:filename>')
def send_file(filename):
    logging.info("send_file, request.remote_addr:%s, filename:%s" % (request.remote_addr, filename))
    return app.send_static_file(filename)
# @app.route("/")
# def home():
#     if request.remote_addr in ('0.0.0.0', '127.0.0.1', 'localhost', '172.18.0.1'):
#         return redirect('http://localhost:5173')
#     else:
#         return 'Welcome to DocsGPT Backend!'

@app.after_request
def after_request(response):
    print("after_request, response status_code:%s, response:%s" % (response.status_code, response))
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    return response

if __name__ == "__main__":
    app.run(debug=True, port=7091)

