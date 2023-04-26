from pathlib import Path
import shutil.copy

import pluggy._manager
manager_path = Path(pluggy._manager.__file__)

shutil.copy(Path(__file__).parent / "patch/_manager.py", manager_path)
