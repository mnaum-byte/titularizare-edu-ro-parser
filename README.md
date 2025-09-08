# Titularizare Crawler

Basic crawler for https://titularizare.edu.ro.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run (dev)

```bash
python - <<'PY'
from src.titularizare_crawler.webapp import create_app
app = create_app()
app.run(host='127.0.0.1', port=8000, debug=True)
PY
```

## Deploy to Render

1. Create a new Web Service and connect this repo.
2. Build command:
   ```bash
   pip install -r requirements.txt
   ```
3. Start command:
   ```bash
   gunicorn 'src.titularizare_crawler.webapp:create_app()' --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 180
   ```
4. After deploy, add your custom domain in Settings → Custom domains and follow DNS instructions (HTTPS auto).

