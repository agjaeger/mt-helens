


class HeightMap:
    def __init__ (self, mapfilepath):
        self.size = {
            "rows": 512,
            "cols": 512
        }
        self.data = self._loadMapFile(mapfilepath)

    def getValue (self, r, c):
        return self.data[r][c]

    def _loadMapFile (self, filepath):
        """
            File Format
                - List of Pixels representing a 512x512 map
                - Each pixel is an unsigned 8bit height value
                - The pixels are stored in row major order
        """

        data = [[0] * self.size["cols"]] * self.size["rows"]

        return data


preExplosion = HeightMap("pre.data")
postExplosion = HeightMap("pre.data")


print(preExplosion.getValue(0,0), preExplosion.getValue(511, 511))
