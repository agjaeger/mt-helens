
import numpy as np
from PIL import Image

class HeightMap:
    def __init__ (self, mapfilepath):
        self.size = {
            "rows": 512,
            "cols": 512
        }
        self.data = self._loadMapFile(mapfilepath)

    def getValue (self, r, c):
        return self.data[r][c]

    def saveAsPNG (self, outfilename):
        im = Image.fromarray(self.data, "L")
        im.save(outfilename)

    def _loadMapFile (self, filepath):
        """
            File Format
                - List of Pixels representing a 512x512 map
                - Each pixel is an unsigned 8bit height value
                - The pixels are stored in row major order
        """

        data = np.zeros((self.size["rows"], self.size["cols"]), dtype=np.uint8)

        # read the file into data
        with open(filepath, "rb") as binMapFile:
            curRow = 0
            curCol = 0

            while True:
                in_byte = binMapFile.read(1)
                if not in_byte:
                    break

                heightValue = in_byte[0]
                data[curRow, curCol] = heightValue

                # handle moving the current location across the 2d array
                if curCol >= self.size["cols"]-1:
                    curCol = 0
                    curRow = curRow + 1
                else:
                    curCol = curCol + 1

        return data


preExplosion = HeightMap("pre.data")
postExplosion = HeightMap("pre.data")


preExplosion.saveAsPNG("parsed-pre.png")
print(preExplosion.getValue(0,0), preExplosion.getValue(511, 511))



