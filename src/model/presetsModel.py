from configparser import ConfigParser, DuplicateSectionError

from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex

presets_filepath = "assets/respiration_presets.ini"

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


class PresetsTableModel(QAbstractTableModel):
    """
    PresetTableModel serves as a PyQt table data model based on QAbstractTableModel which can be easily integrated
    into a PyQt TableView. The methods of QAbstractTableModel are implemented in this class. The model in this class
    is based on the "pure" RespiratorPresetsModel.
    """

    _raw_model = RespirationPresetsModel
    _lang = str
    _table_model_rows = []
    _table_headers_horizontal = []

    def __init__(self, presets_model: RespirationPresetsModel, language: str = "de"):
        """
        PresetsTableModel needs the base RespirationPresetsModel and the language_abbreviation for the table headers

        :param presets_model:
        :param language: Identifier for translation language (e.g. "de" for German, "en" for English)
        """
        super(PresetsTableModel, self).__init__()

        self._raw_model = presets_model  # This is not the model which is consumed by the TableView!
        self._lang = language

        # Transform raw RespirationPresetsModel to two dimensional array and set the horizontal table headers
        self._transform_model_to_data_array()
        self._set_horizontal_table_headers()

    def _transform_model_to_data_array(self) -> None:
        """
        Transforms the dict like presets model into a table like, two dimensional array, which can be accessed by the
        TableView. The first element of each array row represents the table's vertical header entry.
        """
        for preset_name in self._raw_model.presets.sections():
            # Append the vertical header (preset title) to the table row
            table_row = [preset_name]
            for preset_identifier in self._raw_model.presets[preset_name]:
                # Append the preset values, which come in a fixed order (see RespirationPresetsModel or .ini file)
                table_row.append(self._raw_model.presets[preset_name][preset_identifier])
            # Append row to all table rows
            self._table_model_rows.append(table_row)

    def _set_horizontal_table_headers(self) -> None:
        """
        Sets the table headers on the basis of the RespirationPresetsModel preset identifiers according to the chosen
        language.
        """
        # Get the first preset identifiers from the first preset (since all preset identifiers are the same for all
        # presets)
        preset_identifiers = self._raw_model.presets[self._raw_model.presets.sections()[0]]
        for preset_id in preset_identifiers:
            # Get the corresponding translation of the key-like preset value identifier
            header = preset_key_translations[preset_id][self._lang]
            self._table_headers_horizontal.append(header)

    """Implementation of QAbstractTableModel methods which are being called by Qt itself (arguments are also supplied
    by Qt when methods are being called/table is being built)."""

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        """
        This method is being called by the TableView to get the data to be displayed, including other data display
        information if the data role is accordingly set and queried. The data is supposed to be returned as a two
        dimensional array, and is accessed by the index parameter, representing a table cell.

        :param index: Table cell index
        :param role: Qt role with which the data information can be queried by the TableView (here only data to be
        displayed)
        :return: Data at the queried table cell index
        """
        if role == Qt.DisplayRole:
            # Access the column data with offset of + 1, because the first column of each row represents the vertical
            # header data which is returned by the headerData() method
            return self._table_model_rows[index.row()][index.column() + 1]

        if role == Qt.TextAlignmentRole:
            # Align data in the middle of the cell
            return Qt.AlignHCenter + Qt.AlignVCenter

    def rowCount(self, parent: QModelIndex = ...) -> int:
        """
        Return the data/table row count.

        :param parent: Object's parent
        :return: Table row count
        """
        return len(self._table_model_rows)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        """
        Returns the data/table column count, without considering the vertical header column.

        :param parent: Object's parent
        :return: Table column count (without vertical header column).
        """
        return len(self._table_model_rows[0]) - 1

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        """
        Returns the data/table headers, according to the queried orientation.

        :param section: Table section (row/column index)
        :param orientation: Orientation of the header to be returned (vertical/horizontal)
        :param role: Qt role for display
        """
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._table_headers_horizontal[section]
            elif orientation == Qt.Vertical:
                # Return the first entry of the table rows, which contains the vertical header data
                return self._table_model_rows[section][0]

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        """
        Overridden method which returns item flags, with which data behaviour can be set (e.g. make table cell be
        selectable, draggable, enabled, editable, etc.).

        :param index: Index of the item for which the flags are valid
        :return: Qt ItemFlags for data at the specified table index
        """
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable
