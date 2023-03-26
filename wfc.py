
import numpy as np
import js
import binascii
import uuid

class ColorScale():
    def __init__(self, minimum, maximum):
        self._domain_minimum = minimum
        self._domain_maximum = maximum 

    def gray(self, value):
        assert value >= self._domain_minimum and value <= self._domain_maximum
        value = ((value-self._domain_minimum) / self._domain_maximum) * 255
        color = "#" + binascii.hexlify(bytearray([int(value) for _ in range(3)])).decode()
        return color

class MatrixDisplay():
    def __init__(self, width, height, document, parent_element):
        self._canvas = document.createElement("canvas")
        self._canvas_id = uuid.uuid4()
        self._canvas.width = width
        self._canvas.height = height

        parent_element.appendChild(self._canvas)

    @property
    def _width(self):
        return float(self._canvas.width)

    @property
    def _height(self):
        return float(self._canvas.height)

    @property
    def _context(self):
        return self._canvas.getContext("2d")

    def _set_color(self, color):
        self._context.fillStyle = color

    def clear(self):
        self._set_color("#fab")
        self._context.fillRect(0,0,self._width,self._height)

    def _rect(self,x ,y, width, height, color):
        self._set_color(color)
        self._context.fillRect(x,y,width,height)

    def blit(self,matrix):
        scale = ColorScale(matrix.min(), matrix.max())
        self.clear()
        rows,cols = matrix.shape
        xunit, yunit = self._width/rows, self._height/cols
        for x,row in enumerate(matrix):
            for y,value in enumerate(row):
                self._rect(x*xunit, y*yunit, xunit, yunit, scale.gray(value))

class Wfc():

    @staticmethod
    def neighborhood(idx,mat):
        x,y = idx
        center = [1,1]
        if x==0:
            center[0] = 0
        if y==0:
            center[1] = 0

        return center, mat[max(x-1,0):min(x+1,mat.shape[0]), max(x-1,0):min(y+1,mat.shape[1])]

    @staticmethod
    def neighboring_indices(idx,mat):
        x,y = idx
        all_indices = [(i,j) for i,j in zip(range(max(x-1,0),min(x+1,mat.shape[0])), range(max(y-1,0),min(y+1,mat.shape[1])))]
        return [idx for idx in all_indices if idx != (x,y)]

    @staticmethod
    def collapse(idx, matrix):
        """Collapse the center (index) of a matrix."""
        to_collapse = matrix[idx]
        center, neighborhood = Wfc.neighborhood(idx, mat)

    @staticmethod
    def update_entropy(idx, matrix, entropy):
        """Gets a neighbor of a newly collapsed cell, needs to figure out new entropy."""
        ...

    @staticmethod
    def generate(x,y):
        matrix = np.zeros((x,y))
        entropy = np.ones(matrix.shape)

        initial = random.randint(0, matrix.shape[0]), random.randint(0, matrix.shape[1])

        while not matrix.min == 0:
            to_collapse = random.choice([(i,j) for i,j in zip(*np.where(entropy == entropy.min))])
            Wfc.collapse(idx,matrix)
            for neighbor in Wfc.neighboring_indices(idx,mat):
                Wfc.update_entropy(idx, mat, entropy)
