#!/usr/bin/env python

class PresetManager:
    """
    This class manages all the presets. It loads all the presets in the
    current directory into memory to be later be called by the VizManager.

    """

    def __init__(self):

        # Keeps all presets in memory with an integer key to access them.
        self.presets = {}
        self.load_presets()

    def get_preset(self, preset_id):
        """
        Returns preset with id as the key.

        :param preset_id: int
            Key of the preset.
        :return: Preset
            Preset of matching key.
        """
        return self.presets[preset_id]

    def load_presets(self):
        """
        Loads all presets into storage.

        """

        pass

    def load_preset_from_path(self, path):
        """
        Load preset .py file from given path to the preset dictionary.

        """

        pass

    def add_preset(self, preset):
        pass
