from dataclasses import dataclass


@dataclass
class PlacesGet:
    country: str
    state: str
    country_selection: bool
