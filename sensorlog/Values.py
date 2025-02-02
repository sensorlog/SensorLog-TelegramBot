from .Id import Id
from typing import Optional


class Values(Id):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Passing additional arguments to the parent class
        self.level: Optional[float] = None
        self.raw_level: Optional[float] = None
        self.distance: Optional[float] = None
        self.t0: Optional[float] = None
        self.t1: Optional[float] = None
        self.v0: Optional[float] = None
        self.v1: Optional[float] = None
        self.snr: Optional[int] = None
        self.rssi: Optional[int] = None
        self.snr_gw: Optional[int] = None
        self.rssi_gw: Optional[int] = None
        self.speed1: Optional[int] = None
        self.speed2: Optional[int] = None

    def __str__(self):
        return (
            f"{super().__str__()}"
            f"  level: {self.level}\n"
            f"  raw_level: {self.raw_level}\n"
            f"  distance: {self.distance}\n"
            f"  t0: {self.t0}\n"
            f"  t1: {self.t1}\n"
            f"  v0: {self.v0}\n"
            f"  v1: {self.v1}\n"
            f"  snr: {self.snr}\n"
            f"  rssi: {self.rssi}\n"
            f"  snr_gw: {self.snr_gw}\n"
            f"  rssi_gw: {self.rssi_gw}\n"
            f"  speed1: {self.speed1}\n"
            f"  speed2: {self.speed2}"
        )
