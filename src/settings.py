from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import packaging.version
from packaging.version import Version

from dataclass_wizard import JSONWizard, property_wizard


@dataclass
class Installation(metaclass=property_wizard):
    version: str
    path: str

    @property
    def path(self) -> Path:
        return Path(self._path)

    @path.setter
    def path(self, new_path: str | Path):
        if type(new_path) is Path:
            self._path = str(new_path)
            return
        self._path = new_path

    @property
    def version(self) -> Version:
        return packaging.version.parse(self._version)

    @version.setter
    def version(self, new_version: str | Version):
        if type(new_version) is Version:
            self._version = str(new_version)
            return
        self._version = new_version


@dataclass
class Settings(JSONWizard):
    version_installation_history: dict[datetime, Installation] = field(
        default_factory=dict
    )

    @property
    def current_installation_time(self) -> datetime | None:
        sorted_keys = sorted(self.version_installation_history, reverse=True)
        if len(sorted_keys) == 0:
            return None
        return sorted_keys[0]

    @property
    def current_installation(self) -> Installation | None:
        time = self.current_installation_time
        if time is None:
            return None
        return self.version_installation_history[time]
