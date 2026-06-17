from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
SRC_FILE = ROOT / "src" / "api.py"

spec = spec_from_file_location("spicytech_api", SRC_FILE)
if spec is None or spec.loader is None:
    raise RuntimeError(f"No se pudo cargar la aplicación Flask desde {SRC_FILE}")

module = module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

app = module.app
application = app
handler = app
