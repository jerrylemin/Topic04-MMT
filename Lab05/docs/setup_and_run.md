# Setup and run

Su dung Python 3.11 tro len. Ung dung luon bind `127.0.0.1:5005`; khong doi sang
dia chi toan mang.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe seed.py
.\.venv\Scripts\python.exe app.py
```

Mo `http://127.0.0.1:5005`. Kiem thu bang
`.\.venv\Scripts\python.exe -m pytest -q`; tao evidence bang
`.\.venv\Scripts\python.exe scripts\export_evidence.py`; tao bao cao bang
`.\.venv\Scripts\python.exe scripts\generate_report.py`. Chup anh thu cong theo
`HUONG_DAN_CHUP_ANH.md`, roi chay `scripts\check_screenshots.py`.

Docker chi nen chay khi Docker Desktop daemon san sang: `docker compose up
--build`. Compose chi publish cong tren loopback host.
