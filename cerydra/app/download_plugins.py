import subprocess
from pathlib import Path

import yaml


def clone_or_update_plugin(repo_url: str, branch: str, target_dir: Path, github_token: str, logger):
    """Clone a repo if it doesn't exist; pull latest if it does."""

    if target_dir.exists():
        logger.log(f"Updating plugin in {target_dir}...")
        subprocess.run(["git", "-C", str(target_dir), "pull"], check=True)
    else:
        logger.log(f"Cloning plugin from {repo_url} into {target_dir}...")
        # Inject token if private repo
        if github_token and repo_url.startswith("https://github.com/"):
            repo_url = repo_url.replace("https://github.com/", f"https://{github_token}@github.com/")
        subprocess.run(["git", "clone", "--branch", branch, repo_url, str(target_dir)], check=True)


def download_plugins(config_path, plugins_dir, github_token, logger):
    plugins_dir.mkdir(exist_ok=True)
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
        plugins = config.get("plugins", {})

    for plugin_name, plugin in plugins.items():
        name = plugin_name
        url = plugin["url"]
        branch = plugin["branch"]
        target = plugins_dir / name
        clone_or_update_plugin(url, branch, target, github_token, logger)

    logger.log("All plugins successfully downloaded!")
