
# stdlib
from math import floor

# external modules
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
    return np.linalg.norm(endPoint.toNPArray()-startPoint.toNPArray())

def gridSpaceToWorldSpace(heightMap, gridPoint2D):
    return point * heightMap.resolution.horizontal

class Point:
    def __init__(self, r, c, z=0):
        self.row = r
        self.col = c
        self.z = z

    def offset(self, ro, co):
        self.row += ro
        self.col += co
        return self

    def setZ (self, z):
        self.z = z
        return self

    def toNPArray(self):
        return np.array([self.col, self.row])

    def __str__(self):
        return ",".join([self.col, self.row])

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
        # most important, we need to find the height
        # this is a bit complicated because the gridSpacePoint may not lie
        # on grid intersections

        floorPoint = Point(
            r = floor(gridSpacePoint.row),
            c = floor(gridSpacePoint.col),
        )

        gridQuad = {
            "topleft": floorPoint.setZ(self.getValue(floorPoint)),
            "topright": floorPoint.offset(0,1).setZ(self.getValue(floorPoint)),
            "bottomleft": floorPoint.offset(1,0).setZ(self.getValue(floorPoint)),
            "bottomright": floorPoint.offset(1,1).setZ(self.getValue(floorPoint))
        }

        # quad interpolation
        # from http://www.reedbeta.com/blog/quadrilateral-interpolation-part-1/
        distancesFromGridQuad = {
            "topleft": euclideanDistance(gridSpacePoint, gridQuad["topleft"]),
            "topright": euclideanDistance(gridSpacePoint, gridQuad["topright"]),
            "bottomleft": euclideanDistance(gridSpacePoint, gridQuad["bottomleft"]),
            "bottomright": euclideanDistance(gridSpacePoint, gridQuad["bottomright"])
        }

        print(distancesFromGridQuad)

        return floorPoint

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
                    curPoint.offset(1,0)
                else:
                    curPoint.offset(0,1)

        return data


def calculateTravelDistance(heightMap, fromPoint, toPoint):
    totalDistance = 0

    previousPoint = heightMap.getWorldSpacePoint(fromPoint)

    # I want to start from the beginning of the line
    # and sample the heights across it 
    NUM_SAMPLES = 100000
    for i in range(1, NUM_SAMPLES+1):
        t = i/float(NUM_SAMPLES)

        sampledPoint = getPointAlongLine(fromPoint, toPoint, t)
        worldSpaceSampledPoint = heightMap.getWorldSpacePoint(sampledPoint)

        totalDistance += euclideanDistance(
            sampledPoint,
            previousPoint
        )

        previousPoint = sampledPoint

    return totalDistance

# [rows, cols]
startPoint = Point(r=100, c=0)
endPoint = Point(r=500, c=0)

preExplosion = HeightMap("pre.data")
postExplosion = HeightMap("post.data")

print(calculateTravelDistance(preExplosion, startPoint, endPoint))
print(euclideanDistance(startPoint, endPoint))
