import os
import numpy as np
import collections
import matplotlib.pyplot as plt
import pickle
import pyMRAW
import datetime

from .methods import IDIMethod, SimplifiedOpticalFlow, GradientBasedOpticalFlow, LucasKanadeSc, LucasKanade
from . import tools

__version__ = '0.20'

available_method_shortcuts = [
    ('sof', SimplifiedOpticalFlow),
    ('lk', LucasKanade),
    ('lk_scipy', LucasKanadeSc)
    # ('gb', GradientBasedOpticalFlow)
    ]


class pyIDI:
    """
    The pyIDI base class represents the video to be analysed.
    """
    def __init__(self, cih_file):
        self.cih_file = cih_file
        if type(cih_file) == str:
            self.root = os.path.split(self.cih_file)[0]
        else:
            self.root = ''

        self.available_methods = dict([ 
            (key, {
                'IDIMethod': method,
                'description': method.__doc__,     
            })
            for key, method in available_method_shortcuts
        ])

        # Fill available methods into `set_method` docstring
        available_methods_doc = '\n' + '\n'.join([
            f"'{key}' ({method_dict['IDIMethod'].__name__}): {method_dict['description']}"
            for key, method_dict in self.available_methods.items()
            ])
        tools.update_docstring(self.set_method, added_doc=available_methods_doc)

        if type(cih_file) == str:
            # Load selected video
            self.mraw, self.info = pyMRAW.load_video(self.cih_file)
            self.N = self.info['Total Frame']
            self.image_width = self.info['Image Width']
            self.image_height = self.info['Image Height']
        
        elif type(cih_file) == np.ndarray:
            self.mraw = cih_file
            self.N = cih_file.shape[0]
            self.image_height = cih_file.shape[1]
            self.image_width = cih_file.shape[2]
            self.info = {}
        
        else:
            raise ValueError('`cih_file` must be either a cih filename or a 3D array (N_time, height, width)')


    def set_method(self, method, **kwargs):
        """
        Set displacement identification method on video.
        To configure the method, use `method.configure()`

        Available methods:
        ---
        [Available method names and descriptions go here.]
        ---

        :param method: the method to be used for displacement identification.
        :type method: IDIMethod or str
        """
        if isinstance(method, str) and method in self.available_methods.keys():
            self.method = self.available_methods[method]['IDIMethod'](self, **kwargs)
        elif callable(method) and hasattr(method, 'calculate_displacements'):
            try:
                self.method = method(self, **kwargs)
            except:
                raise ValueError("The input `method` is not a valid `IDIMethod`.")
        else:
            raise ValueError("method must either be a valid name from `available_methods` or an `IDIMethod`.")
        
        # Update `get_displacements` docstring
        tools.update_docstring(self.get_displacements, self.method.calculate_displacements)
        # Update `show_points` docstring
        if hasattr(self.method, 'show_points'):
            try:
                tools.update_docstring(self.show_points, self.method.show_points)
            except:
                pass


    def set_points(self, points=None, method=None, **kwargs):
        """
        Set points that will be used to calculate displacements.
        If `points` is None and a `method` has aready been set on this `pyIDI` instance, 
        the `method` object's `get_point` is used to get method-appropriate points.
        """
        if points is None:
            if not hasattr(self, 'method'):
                if method is not None:
                    self.set_method(method)
                else:
                    raise ValueError("Invalid arguments. Please input points, or set the IDI method first.")
            self.method.get_points(self, **kwargs) # get_points sets the attribute video.points                
        else:
            self.points = np.asarray(points)


    def show_points(self, **kwargs):
        """
        Show selected points on image.
        """

        if hasattr(self, 'method') and hasattr(self.method, 'show_points'):
            self.method.show_points(self, **kwargs)
        else:
            figsize = kwargs.get('figsize', (15, 5))
            cmap = kwargs.get('cmap', 'gray')
            marker = kwargs.get('marker', '.')
            color = kwargs.get('color', 'r')
            fig, ax = plt.subplots(figsize=figsize)
            ax.imshow(self.mraw[0].astype(float), cmap=cmap)
            ax.scatter(self.points[:, 1], self.points[:, 0], 
                marker=marker, color=color)
            plt.grid(False)
            plt.show()


    def show_field(self, field, scale=1., width=0.5):
        """
        Show displacement field on image.
        
        :param field: Field of displacements (number_of_points, 2)
        :type field: ndarray
        :param scale: scale the field, defaults to 1.
        :param scale: float, optional
        :param width: width of the arrow, defaults to 0.5
        :param width: float, optional
        """
        max_L = np.max(field[:, 0]**2 + field[:, 1]**2)

        fig, ax = plt.subplots(1)
        ax.imshow(self.mraw[0], 'gray')
        for i, ind in enumerate(self.points):
            f0 = field[i, 0]
            f1 = field[i, 1]
            alpha = (f0**2 + f1**2) / max_L
            if alpha < 0.2:
                alpha = 0.2
            plt.arrow(ind[1], ind[0], scale*f1, scale*f0, width=width, color='r', alpha=alpha)


    def get_displacements(self, **kwargs):
        """
        Calculate the displacements based on chosen method.

        Method docstring:
        ---
        Method is not set. Please use the `set_method` method.
        ---
        """
        if hasattr(self, 'method'):
            self.method.calculate_displacements(self, **kwargs)
            self.displacements = self.method.displacements
            
            # auto-save and clearing temp files
            if hasattr(self.method, 'process_number'):
                if self.method.process_number == 0:
                    if type(self.cih_file) == str:
                        cih_file_ = os.path.split(self.cih_file)[-1].split('.')[0]
                        auto_filename = f'{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}_{cih_file_}.pkl'
                    else:
                        auto_filename = f'{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}_displacements.pkl'
                    
                    self.save(auto_filename, root=self.root)
                    self.method.clear_temp_files()
                    
            return self.displacements
        else:
            raise ValueError('IDI method has not yet been set. Please call `set_method()` first.')


    def close_video(self):
        """
        Close the .mraw video memmap.
        """
        if hasattr(self, 'mraw'):
            self.mraw._mmap.close()
            del self.mraw


    def save(self, filename, root=''):
        """ Save computed displacements and other basic information.

        :param filename: Name of the file to save in.
        :param root: Root of the filename, defaults to ''
        """
        full_filename = os.path.join(root, filename)
        out = {
            'points': self.points,
            'disp': self.displacements,
            'first_image': self.mraw[0],
            'info': self.info,
            'cih_file': self.cih_file,
            'settings': self.method.create_settings_dict()
        }
        pickle.dump(out, open(full_filename, 'wb'), protocol=-1)

    
