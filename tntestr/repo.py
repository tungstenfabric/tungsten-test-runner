import logging

from typing import List

from collections import namedtuple

Repository = namedtuple("Repository", ["name", "path"])

class GitRepo(object):
    """Abstracts interactions with Git Repo"""

    def __init__(self):
        self.log = logging.getLogger("tntestr.GitRepo")
        self._parsed = False
        self._repositories = None
        self._parse_manifest()

    def _parse_manifest(self) -> None:
        self.log.debug("Parsing manifest.xml for the project")
        with open(".repo/manifest.xml", "r") as fh:
            manifest_xml = fh.read()

    @property
    def repositories(self) -> List[Repository]:
        if not self._parsed:
            self._parse_manifest()
        return self._repositories
