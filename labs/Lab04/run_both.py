import threading

from attacker_app import create_app as create_attacker_app
from victim_app import create_app as create_victim_app


def _run(app, port):
    app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)


if __name__ == "__main__":
    print("Victim: http://127.0.0.1:5004")
    print("Attacker same-site: http://127.0.0.1:9004")
    print("Attacker cross-site: http://localhost:9004")
    victim = threading.Thread(target=_run, args=(create_victim_app(), 5004), daemon=True)
    victim.start()
    _run(create_attacker_app(), 9004)
