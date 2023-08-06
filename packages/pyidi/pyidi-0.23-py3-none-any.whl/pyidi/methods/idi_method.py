import numpy as np


class IDIMethod:
    """Common functions for all methods.
    """
    
    def __init__(self, video, *args, **kwargs):
        """
        The image displacement identification method constructor.

        For more configuration options, see `method.configure()`
        """
        self.video = video
        self.configure(*args, **kwargs)
    
    
    def configure(self, *args, **kwargs):
        """
        Configure the displacement identification method here.
        """
        pass

    
    def calculate_displacements(self, video, *args, **kwargs):
        """
        Calculate the displacements of set points here.
        The result should be saved into the `self.displacements` attribute.
        """
        pass
    
    def create_temp_files(self):
        pass
    
    def clear_temp_files(self):
        pass

    def create_settings_dict(self):
        settings = dict()
        return settings