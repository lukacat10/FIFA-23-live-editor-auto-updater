from datetime import datetime
from pathlib import Path
import shutil
from github import Github
from github.GitRelease import GitRelease
from platformdirs import PlatformDirs
from packaging import version
import tempfile
import zipfile
import ctypes

from settings import Installation, Settings
import urllib.request

import win32com.client

PLATFORM_DIRS = PlatformDirs("fifa 23 live editor auto updater", "lukacat10")

REPO = "xAranaktu/FIFA-23-Live-Editor"

SETTINGS_PATH = PLATFORM_DIRS.user_config_path / "settings.json"

FIFA_EDITORS_PATH = PLATFORM_DIRS.user_downloads_path / "fifa editors"


def message_box(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


def load_settings() -> Settings:
    if SETTINGS_PATH.exists():
        with open(SETTINGS_PATH, "r") as f:
            settings_json = f.read()
            return Settings.from_json(settings_json)
    else:
        return Settings()


def save_settings(settings: Settings):
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        f.write(settings.to_json())


def init_fifa_editors_folder():
    FIFA_EDITORS_PATH.mkdir(parents=True, exist_ok=True)
    for item in FIFA_EDITORS_PATH.iterdir():
        if item.is_dir():
            shutil.rmtree(str(item), ignore_errors=True)
        else:
            item.unlink()
    return FIFA_EDITORS_PATH


def download_and_extract(download_url: str, fifa_editors_folder=FIFA_EDITORS_PATH):
    download_url_path = Path(download_url)
    with tempfile.TemporaryDirectory() as folder:
        folder_path = Path(folder)
        downloaded_file_name = download_url_path.name
        downloaded_zip_file = folder_path / downloaded_file_name

        urllib.request.urlretrieve(download_url, str(downloaded_zip_file))

        with zipfile.ZipFile(downloaded_zip_file, "r") as zip_ref:
            extracted = folder_path / download_url_path.stem
            zip_ref.extractall(extracted)

        final_dir_path = fifa_editors_folder / extracted.name

        shutil.copytree(extracted, final_dir_path)
    return final_dir_path


def install(release: GitRelease):
    asset = list(release.get_assets())[0]
    download_url = asset.browser_download_url

    fifa_editors_folder = init_fifa_editors_folder()

    editor_dir_path = download_and_extract(download_url, fifa_editors_folder)

    launcher_exe = editor_dir_path / "Launcher.exe"

    link = PLATFORM_DIRS.user_desktop_path / "Launcher.exe.lnk"

    if link.exists():
        link.unlink()

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(str(link))
    shortcut.Targetpath = str(launcher_exe)
    shortcut.save()

    return launcher_exe


def main():
    github_api = Github()

    repo = github_api.get_repo(REPO)
    releases = repo.get_releases()

    latest_release = sorted(
        releases, key=lambda release: release.created_at, reverse=True
    )[0]

    latest_version = version.parse(latest_release.tag_name)

    settings = load_settings()

    if (
        settings.current_installation is None
        or settings.current_installation.version < latest_version
    ):
        installation_path = install(latest_release)
        settings.version_installation_history[datetime.now()] = Installation(
            str(latest_version), str(installation_path)
        )
        save_settings(settings)
        message_box("Update successful", "Successfully updated the launcher", 0)
    else:
        message_box("Up to date", "Version already up to date!", 0)


if __name__ == "__main__":
    main()
