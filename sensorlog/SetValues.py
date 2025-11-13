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
            "Contador": ("counter", "int"),
            "Entrada Digital": ("digital_input", "digital"),
        }

    def set_value(self, key, value):
        translation = self.__translate.get(key)
        if translation:
            key, value_type = translation
            new_value = None

            if value_type == "float":
                new_value = float(value)
            elif value_type == "int":
                new_value = int(value)
            elif value_type == "digital":
                state = str(value).strip()
                if state:
                    if state[0] == "A":  # Aberta
                        new_value = int(1)
                    elif state[0] == "F":  # Fechada
                        new_value = int(0)
            else:
                new_value = str(value).strip()
            if new_value is not None:
                setattr(self, key, new_value)
