from .Values import Values


class SetValues(Values):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__translate = {
            "Nível": ("level", "float"),
            "Nível*": ("raw_level", "float"),
            "Dist₍₀₎": ("distance", "float"),
            "T0": ("t0", "float"),
            "T1": ("t1", "float"),
            "V0": ("v0", "float"),
            "V1": ("v1", "float"),
            "SNR": ("snr", "int"),
            "RSSI": ("rssi", "int"),
            "SNR(gw)": ("snr_gw", "int"),
            "RSSI(gw)": ("rssi_gw", "int"),
            "Δd/Δt₍₋₁₎": ("speed1", "int"),
            "Δd/Δt₍₋₂₎": ("speed2", "int"),
        }

    def set_value(self, key, value):
        translated_key = self.__translate.get(key)
        if translated_key:
            value_type = translated_key[1]
            new_value = float(value) if value_type == "float" else int(value)
            setattr(self, translated_key[0], new_value)
