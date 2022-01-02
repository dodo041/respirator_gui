from configparser import ConfigParser, DuplicateSectionError

presets_filepath = "../../assets/respiration_presets.ini"

# Translations for keys in preset file
preset_key_translations = {
    "frequency": {
        "de": "Frequenz",
        "en": "Frequency"
    },
    "pressure_min": {
        "de": "Druck min.",
        "en": "Pressure min."
    },
    "pressure_max": {
        "de": "Druck max.",
        "en": "Pressure max."
    },
    "volume_min": {
        "de": "Volumen min.",
        "en": "Volume min."
    },
    "volume_max": {
        "de": "Volumen max.",
        "en": "Volume max."
    },
    "i_to_e_ratio": {
        "de": "Verhältnis I/E",
        "en": "Ratio I/E"
    }
}


class RespirationPresetsModel:
    """
    RespirationPresetsModel serves as a library for respiration presets and initially contains all presets (except
    DEFAULT) from the presets file.
    """

    # Safe presets in ConfigParser instance which makes the values accessible like in a dict
    presets = ConfigParser

    def __init__(self):
        self._load_presets_from_file(presets_filepath)

    def _load_presets_from_file(self, filepath: str) -> None:
        self.presets = ConfigParser()
        self.presets.read(filepath)

    def create_preset_entry(self, identifier: str, freq: float, p_min: float, p_max: float, vol_min: float,
                            vol_max: float, ie_ratio: float) -> bool:
        """
        Creates a new respiration preset entry to be saved in the preset file.

        :param identifier: Text identifier for the new preset (e.g. animal name)
        :param freq: Respiration frequency
        :param p_min: Min. respiration pressure
        :param p_max: Max. respiration pressure
        :param vol_min: Min. volume
        :param vol_max: Max. volume
        :param ie_ratio: Inspiration-to-expiration ratio
        :return: Success of preset entry creation
        """

        # Check if entry to be created already exists
        try:
            self.presets.add_section(identifier)
        except DuplicateSectionError:
            print(f"\nPreset could not be created: Entry {identifier} already exists in file.")
            return False
        else:
            # TODO Maybe add validation of the preset values?
            self.presets[identifier]["frequency"] = str(freq)
            self.presets[identifier]["pressure_min"] = str(p_min)
            self.presets[identifier]["pressure_max"] = str(p_max)
            self.presets[identifier]["volume_min"] = str(vol_min)
            self.presets[identifier]["volume_max"] = str(vol_max)
            self.presets[identifier]["i_to_e_ratio"] = str(ie_ratio)

        # Write preset to file
        with open(file=presets_filepath, mode="w") as presets_file:
            self.presets.write(fp=presets_file)
            return True

    # TODO Do we need this, or should presets be modified by "dict access"?
    def modify_preset_entry(self):
        pass
