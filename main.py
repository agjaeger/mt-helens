
import numpy as np
from PIL import Image

class HeightMap:
    def __init__ (self, mapfilepath):
        self.size = {
            "rows": 512,
            "cols": 512
        }
        self.resolution = {
            "horizontal": 30,
            "vertical": 11
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

def lerp (start, end, t):
    return (1-t) * start + t * end

def getPointAlongLine(fromPoint, toPoint, t):
    return [
        lerp(fromPoint[0], toPoint[0], t),
        lerp(fromPoint[1], toPoint[1], t)
    ]

def euclideanDistance (startPoint, endPoint):
    return np.linalg.norm(np.array(endPoint)-np.array(startPoint))

def gridSpaceToWorldSpace(heightMap, gridPoint2D):
    return point * heightMap.resolution.horizontal

def calculateTravelDistance(heightMap, fromPoint, toPoint):
    totalDistance = 0

    previousPoint = fromPoint
    # I want to start from the beginning of the line
    # and sample the heights across it 
    NUM_SAMPLES = 100000
    for i in range(1,NUM_SAMPLES+1):
        t = i/float(NUM_SAMPLES)
        sampledPoint = getPointAlongLine(fromPoint, toPoint, t)

        totalDistance += euclideanDistance(
            sampledPoint,
            previousPoint
        )

        previousPoint = sampledPoint

    return totalDistance

startPoint = [100, 0]
endPoint = [500, 0]

preExplosion = HeightMap("pre.data")
postExplosion = HeightMap("post.data")

print(calculateTravelDistance(preExplosion, startPoint, endPoint))
print(euclideanDistance(startPoint, endPoint))
