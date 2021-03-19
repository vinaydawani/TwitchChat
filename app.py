import socket
import yaml
import logging
import io
from emoji import demojize

with open("config.yaml") as x:
    config = yaml.safe_load(x)

sock = socket.socket()
sock.connect((config["twitch"]["server"], config["twitch"]["port"]))
sock.send(f"PASS {config['twitch']['token']}\n".encode("utf-8"))
sock.send(f"NICK {config['twitch']['nickname']}\n".encode("utf-8"))
sock.send(f"JOIN {config['twitch']['channel']}\n".encode("utf-8"))

log_name = f"{config['twitch']['channel'].split('#')[1]}.log"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s — %(message)s",
    datefmt="%Y-%m-%d_%H:%M:%S",
    handlers=[logging.FileHandler(log_name, encoding="utf-8")],
)

log_capture_string = io.StringIO()
ch = logging.StreamHandler(log_capture_string)
ch.setLevel(logging.DEBUG)

logging.getLogger("").addHandler(ch)

# logger = logging.getLogger('basic_logger')
# logger.setLevel(logging.DEBUG)
# formatter = logging.Formatter("%(asctime)s — %(message)s")

resp = sock.recv(4096).decode("utf-8")
resp = sock.recv(4096).decode("utf-8")

while True:
    resp = sock.recv(4096).decode("utf-8")

    if resp.startswith("PING"):
        sock.send("PONG\n".encode("utf-8"))

    elif len(resp) > 0:
        logging.info(demojize(resp))
        text = log_capture_string.getvalue()
        print(text)
        log_capture_string.truncate(0)
        log_capture_string.seek(0)
