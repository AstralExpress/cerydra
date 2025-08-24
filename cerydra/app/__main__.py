import os
from pathlib import Path
from dotenv import load_dotenv

from app.plugin_orchestrator import PathstriderOrchestrator
from core.logging import logger

load_dotenv()
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
CONFIG_PATH = Path(os.environ.get("CONFIG_PATH"))
PLUGINS_DIR = Path(os.environ.get("PLUGINS_DIR"))

if __name__ == "__main__":
    orchestrator = PathstriderOrchestrator(logger=logger)
    orchestrator.load_plugins(
        config_path=CONFIG_PATH,
        plugins_dir=PLUGINS_DIR,
        github_token=GITHUB_TOKEN,
    )