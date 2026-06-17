"""Chequeo manual para validar la configuración SMTP de SpicyTech.

No envía correos por sí solo si no se habilita SEND_SMOKE_EMAIL=1.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from auth import EmailNotifier


def main() -> None:
    print("SMTP_USER configured:", bool(os.environ.get("SMTP_USER")))
    print("SMTP_PASS configured:", bool(os.environ.get("SMTP_PASS") or os.environ.get("GMAIL_APP_PASSWORD")))
    print("CONTACT_EMAIL:", os.environ.get("CONTACT_EMAIL", "info@spicytech.com"))

    if os.environ.get("SEND_SMOKE_EMAIL") != "1":
        print("Smoke test in dry-run mode. Set SEND_SMOKE_EMAIL=1 to attempt a real delivery.")
        return

    notifier = EmailNotifier()
    notifier._send_email(
        to=os.environ.get("SMOKE_TO_EMAIL", "cliente.prueba@spicytech.com"),
        subject="Prueba SMTP SpicyTech",
        html_body="<html><body><h1>Prueba SMTP SpicyTech</h1><p>Si recibís esto, el envío funciona.</p></body></html>",
    )


if __name__ == "__main__":
    main()
