"""Chequeo manual para validar la configuración de Resend de SpicyTech.

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
    print("RESEND_API_KEY configured:", bool(os.environ.get("RESEND_API_KEY")))
    print("EMAIL_FROM:", os.environ.get("EMAIL_FROM", "SpicyTech Coworking <onboarding@resend.dev>"))
    print("CONTACT_EMAIL:", os.environ.get("CONTACT_EMAIL", "info@spicytech.com"))

    if os.environ.get("SEND_SMOKE_EMAIL") != "1":
        print("Smoke test in dry-run mode. Set SEND_SMOKE_EMAIL=1 to attempt a real delivery.")
        return

    notifier = EmailNotifier()
    notifier._send_email(
        # En modo sandbox (sin dominio verificado), Resend solo entrega a la
        # casilla con la que te registraste en Resend.
        to=os.environ.get("SMOKE_TO_EMAIL", "santi481manrique@gmail.com"),
        subject="Prueba Resend SpicyTech",
        html_body="<html><body><h1>Prueba Resend SpicyTech</h1><p>Si recibís esto, el envío funciona.</p></body></html>",
    )


if __name__ == "__main__":
    main()
