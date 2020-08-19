
# stdlib
from math import floor

# external modules
from scipy import interpolate
import numpy as np
from PIL import Image

def lerp (start, end, t):
    return (1-t) * start + t * end

def getPointAlongLine(fromPoint, toPoint, t):
    return Point(
        c = lerp(fromPoint.col, toPoint.col, t),
        r = lerp(fromPoint.row, toPoint.row, t)
    )

def euclideanDistance (startPoint, endPoint):
    return np.linalg.norm(endPoint.to2DNPArray()-startPoint.to2DNPArray())

class Point:
    def __init__(self, r, c, z=0):
        self.row = r
        self.col = c
        self.z = z

    def to2DArray(self):
        return [self.col, self.row]

    def to3DArray(self):
        return [self.col, self.row, self.z]

    def to2DNPArray(self):
        return np.array(self.to2DArray())

    def __str__(self):
        return ",".join([str(v) for v in self.to3DArray()])

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

    def getValue (self, point):
        return self.data[point.row][point.col]

    def getWorldSpacePoint (self, gridSpacePoint):
        tlr = floor(gridSpacePoint.row)
        tlc = floor(gridSpacePoint.col)

        gridQuad = [
            # tl, tr, bl, br
            Point(r=tlr, c=tlc),
            Point(r=tlr, c=tlc+1),
            Point(r=tlr+1, c=tlc),
            Point(r=tlr+1, c=tlc+1)
        ]

        heightFunc = interpolate.interp2d(
            [v.col for v in gridQuad],
            [v.row for v in gridQuad],
            [self.getValue(v) for v in gridQuad],
            kind="linear"
        )

        newHeight = heightFunc(*gridSpacePoint.to2DArray())[0]

        return Point(
            r = gridSpacePoint.row,
            c = gridSpacePoint.col,
            z = newHeight
        )

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
            curPoint = Point(0, 0)

            while True:
                in_byte = binMapFile.read(1)
                if not in_byte:
                    break

                heightValue = in_byte[0]
                data[curPoint.row][curPoint.col] = heightValue

                # handle moving the current location across the 2d array
                if curPoint.col >= self.size["cols"]-1:
                    curPoint.col = 0
                    curPoint.row += 1
                else:
                    curPoint.col += 1

        return data


def calculateTravelDistance(heightMap, fromPoint, toPoint):
    totalDistance = 0

    previousPoint = heightMap.getWorldSpacePoint(fromPoint)

    # I want to start from the beginning of the line
    # and sample the heights across it 
    NUM_SAMPLES = 5
    for i in range(1, NUM_SAMPLES+1):
        t = i/float(NUM_SAMPLES)

        sampledPoint = getPointAlongLine(fromPoint, toPoint, t)
        worldSpaceSampledPoint = heightMap.getWorldSpacePoint(sampledPoint)

        print(sampledPoint, worldSpaceSampledPoint)
        totalDistance += euclideanDistance(
            sampledPoint,
            previousPoint
        )

        previousPoint = sampledPoint

    return totalDistance




startPoint = Point(r=36, c=0)
endPoint = Point(r=39, c=1)

preExplosion = HeightMap("pre.data")
postExplosion = HeightMap("post.data")

print(preExplosion.getValue(startPoint))
print(preExplosion.getValue(endPoint))
preDistance = calculateTravelDistance(preExplosion, startPoint, endPoint)
#postDistance = calculateTravelDistance(postExplosion, startPoint, endPoint)

print(preDistance)
# print(postDistance - preDistance)
