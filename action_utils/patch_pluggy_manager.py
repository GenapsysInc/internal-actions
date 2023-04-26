from pathlib import Path
from shutil import copy

import pluggy._manager
manager_path = Path(pluggy._manager.__file__)

copy(Path(__file__).parent / "patch/_manager.py", manager_path)
