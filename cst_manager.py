from settings import *

class CstManager:
    def __init__(self):
        self.SCREENDIMS = SCREENDIMS
        self.cell_dims = (
            self.SCREENDIMS[0] // 8,
            self.SCREENDIMS[1] // 8
        )
        
        self.old_dims_mem = self.SCREENDIMS

    @property
    def cell_width(self):
        return self.cell_dims[0]

    @property
    def cell_height(self):
        return self.cell_dims[1]
    
    @staticmethod
    def compare_sizes(size1, size2) -> int:
        """
        -1 : size1 is smaller
        0 : same size or one side is larger/the other is smaller
        1 : size1 is bigger
        """
        if size1[0] < size2[0] or size1[1] < size2[1]:
            return -1
        if size1[0] > size2[0] or size1[1] > size2[1]:
            return 1
        return 0
    
    def go_fullscreen(self, new_size):
        self.old_dims_mem = self.SCREENDIMS
        self.SCREENDIMS = new_size
        self.cell_dims = (
            self.SCREENDIMS[0] // 8,
            self.SCREENDIMS[1] // 8
        )

        

    def update_screen_dimensions(self, new_dims, shift=False):
        if shift:
            old_cell_dims = self.cell_dims
        self.cell_dims = (
            new_dims[0] // 8,
            new_dims[1] // 8
        )
        self.SCREENDIMS = (self.cell_width * 8, self.cell_height * 8)
        if shift:
            compare_value = self.compare_sizes(old_cell_dims, self.cell_dims)
            if compare_value == -1:
                new_cell_dims = max(self.cell_width, self.cell_height)
            if compare_value == 1:
                new_cell_dims = min(self.cell_width, self.cell_height)
            if compare_value == 0:
                new_cell_dims = (self.cell_width + self.cell_height) // 2
            self.cell_dims = (new_cell_dims, new_cell_dims)
            self.SCREENDIMS = (self.cell_width * 8, self.cell_height * 8)