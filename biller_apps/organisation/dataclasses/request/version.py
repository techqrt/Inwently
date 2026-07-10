from dataclasses import dataclass
from datetime import date
from typing import List, Optional

@dataclass
class VersionDetail:
    version: str
    build: int

@dataclass
class Version:
    # Required fields (no defaults) must come first
    minimum_version: VersionDetail
    latest_stable_version: VersionDetail
    previous_stable_version: VersionDetail
    changes_in_latest_stable: VersionDetail    
    # Optional fields (with defaults) must come after
    repo_url: Optional[str] = None
    file_name: Optional[str] = None
    beta_version: Optional[VersionDetail] = None
    other_versions: Optional[List[VersionDetail]] = None
