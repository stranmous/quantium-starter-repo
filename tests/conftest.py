import os
from pathlib import Path

import chromedriver_autoinstaller


os.environ.setdefault("DASH_TESTING_HEADLESS", "true")


chromedriver_path = chromedriver_autoinstaller.install()
chromedriver_directory = str(Path(chromedriver_path).parent)
os.environ["PATH"] = chromedriver_directory + os.pathsep + os.environ.get("PATH", "")