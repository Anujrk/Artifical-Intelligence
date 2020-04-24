import math
import sys
import turtle

from PIL import Image
import turtle as t


class Pixels:
    # Node class for pixels

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = None
        self.elevation = None
        self.initial = None


# Type of terrains mapped to there pixel
terrainName = ["openland","roughMeadow","easyMoveForest","slowRunForest","walkForest","impassible",
               "lake","pavedRoad","footpath","outOfBounds","mud","ice"]

terrainType = {(248, 148, 18): "openLand", (255, 192, 0): "roughMeadow",
               (255, 255, 255): "easyMoveForest", (2, 208, 60): "slowRunForest", (2, 136, 40): "walkForest"
    , (5, 73, 24): "impassible", (0, 0, 255): "lake", (71, 51, 3): "pavedRoad"
    , (0, 0, 0): "footpath", (205, 0, 101): "outOfBounds", (143, 75, 3): "mud", (132, 255, 240): "ice"}

# mapping speed to the season
summerSpeed = {"openLand": 10, "roughMeadow": 1.25, "easyMoveForest": 6.25, "slowRunForest": 5,
               "walkForest": 5, "impassible": 0, "lake": 0, "pavedRoad": 10, "footpath": 10,
               "outOfBounds": 0}
springSpeed = {"openLand": 10, "roughMeadow": 1.25, "easyMoveForest": 6.25, "slowRunForest": 5,
               "walkForest": 4.75, "impassible": 0, "lake": 0, "pavedRoad": 10, "footpath": 10,
               "outOfBounds": 0, "mud": 0.5}
fallSpeed = {"openLand": 10, "roughMeadow": 1.25, "easyMoveForest": 4, "slowRunForest": 5,
             "walkForest": 4, "impassible": 0, "lake": 0, "pavedRoad": 10, "footpath": 10,
             "outOfBounds": 0}
winterSpeed = {"openLand": 10, "roughMeadow": 1.25, "easyMoveForest": 6.25, "slowRunForest": 5,
               "walkForest": 3.75, "impassible": 0, "lake": 0, "pavedRoad": 10, "footpath": 10,
               "outOfBounds": 0, "ice": 0.5}

path = []
r = 500
c = 395


def isValid(start, destination, speed):
    # validates if the start point and the end point are valid
    if speed[start.type] == 0 or speed[destination.type] == 0:
        return False
    return True


def euclideanDist(e1, e2):
    """"
    euclidean Distance formula
    """
    dist = ((e1.x - e2.x) ** 2) + ((e1.y - e2.y) ** 2)
    return dist


def elevationDist(e1, e2):
    """"
    finding elevation distance
    """
    dist = (e1.elevation - e2.elevation) ** 2
    return dist


def scoreCalculate(current, successor, destinationNode, speed):
    """
    calculates heuristic and cost to travel from point1 to point2
    score : heuristic + cost
    heuristic : Euclidean formula to find the distance (D=√((Long1-Long2)²+(Lat1-Lat2)²+(Alt1-Alt2)²))
    cost : Total Distance / Speed  (the total distance travelled is sqrt(d**2 + h**2)
            where h is the change in elevation)
    """
    score = float("inf")
    heuristic = float("inf")
    cost = float("inf")
    if current.x != successor.x:
        heuristic = math.sqrt(
            euclideanDist(successor, destinationNode) + elevationDist(successor, destinationNode))
        cost = (math.sqrt((7.55 ** 2) + elevationDist(successor, current))) / (speed[current.type])

    elif current.x == successor.x:
        heuristic = math.sqrt(
            euclideanDist(successor, destinationNode) + elevationDist(successor, destinationNode))
        cost = (math.sqrt((10.29 ** 2) + elevationDist(successor, current))) / (speed[current.type])
    else:
        pass

    score = heuristic + cost

    return score


def pathAlgo(startNode, destinationNode, terrain, speed):
    """
    Performing A* algorithm (Algorithm pseudocode inspired from wikipedia)
    :param startNode: current Node
    :param destinationNode: Final Node
    :param terrain: data of the terrain
    :param speed: speed for the terrain
    :return: quickest path between nodes
    """

    if not isValid(startNode, destinationNode, speed):
        print("Invalid source or destination")
        return

    if (startNode == destinationNode):
        print("We are already at the destination")
        return

    toVisit = []  # Open list
    visited = []  # Closed list
    startNode.score = 0  # Initialising score of source
    current = startNode
    toVisit.append(current)  # put the starting node on the open list
    # print(toVisit)
    # testing = []
    while toVisit is not None:
        bestNode = None
        score = float("inf")  # initiating score to max
        for node in toVisit:  # Finding the bestNode from the openList
            if node.score >= score:
                pass
            else:
                score = node.score
                bestNode = node
        current = bestNode
        if current != destinationNode:
            visited.append(current)  # found the bestNode added to closed list
            toVisit.remove(current)
            # print("tovisit",toVisit)
            # print("visited",visited)
            successors = []  # getting q's successors
            x = current.x
            y = current.y
            if speed[terrain[x][y + 1].type] != 0:
                successors.append(terrain[x][y + 1])
            if speed[terrain[x + 1][y].type] != 0:
                successors.append(terrain[x + 1][y])
            if speed[terrain[x][y - 1].type] != 0:
                successors.append(terrain[x][y - 1])
            if speed[terrain[x - 1][y].type] != 0:
                successors.append(terrain[x - 1][y])
        for successor in successors:
            if current == destinationNode:
                while current.initial:
                    paths = [current.x, current.y]
                    path.append(paths)
                    current = current.initial
                paths2 = [current.x, current.y]
                path.append(paths2)
                return path
            else:
                if successor in visited:
                    pass
                else:
                    if successor not in toVisit:
                        successor.score = scoreCalculate(current, successor, destinationNode, speed)
                        successor.initial = current
                        toVisit.append(successor)
                    else:
                        score = scoreCalculate(current, successor, destinationNode, speed)
                        if score >= successor.score:
                            pass
                        else:
                            successor.score = score
                            successor.initial = current

    print("Path unavailable ")


def main():
    # reading Terrain image
    img = Image.open(sys.argv[1])
    terrainList = []
    data = list(img.getdata())
    i = 0
    j = []
    for pixel in data:
        j.append(pixel)
        i += 1
        if i == 395:
            i = 0
            terrainList.append(j)
            j = []

    # print(terrainList)        #sample o/p : (255, 255, 255, 255), (255, 255, 255, 255)

    # Reading elevation file
    elevationFile = open(sys.argv[2])
    elevation = []
    for line in elevationFile:
        line = line.strip()
        lines = line.split()
        for x in range(len(lines)):
            lines[x] = float(lines[x])
        elevation.append(lines)

    # print(elevation)              #sample o/p : 210.13574, 210.74799, 211.22212
    # Reading path file
    pathFile = open(sys.argv[3])
    newpath = []
    for line in pathFile:
        path_temp = []
        line = line.strip()
        lines = line.split(" ")
        path_temp.append(int(lines[1]))
        path_temp.append(int(lines[0]))
        newpath.append(path_temp)

    # print(newpath)        #Sample o/p : [327, 230], [279, 276], [240, 303]

    # print(len(terrainData))           #o/p is object with len:500
    outputPath = sys.argv[5]

    season = sys.argv[4]
    if season == "spring":  # For spring weather
        speed = springSpeed
        for row in range(r):
            for column in range(c):
                if terrainType[terrainList[row][column][0:3]] == "lake":
                    sides = 0
                    if (row - 1 >= 0 and (terrainType[terrainList[row - 1][column][0:3]] != "lake")) or\
                        (row + 1 < r and (terrainType[terrainList[row + 1][column][0:3]] != "lake")) or\
                        (column - 1 >= 0 and (terrainType[terrainList[row][column - 1][0:3]] != "lake")) or\
                        (column + 1 < c and (terrainType[terrainList[row][column + 1][0:3]] != "lake")):
                        sides = 1
                        if sides == 1:
                            for index in range(15):
                                if row - index < 0 or (elevation[row - index][column] - elevation[row][column]) > 1 or \
                                        terrainType[terrainList[row - index][column][0:3]] != "lake":
                                    break
                                else:
                                    img.putpixel((column, row - index), (143, 75, 3))
                            for index in range(15):
                                if row + index > 499 or (elevation[row + index][column] - elevation[row][column]) > 1 or \
                                        terrainType[terrainList[row + index][column][0:3]] != "lake":
                                    break
                                else:
                                    img.putpixel((column, row + index), (143, 75, 3))
                            for index in range(15):
                                if column - index < 0 or (elevation[row][column - index] - elevation[row][column]) > 1 or \
                                        terrainType[terrainList[row][column - index][0:3]] != "lake":
                                    break
                                else:
                                    img.putpixel((column - index, row), (143, 75, 3))
                            for index in range(15):
                                if column + index > 394 or (elevation[row][column + index] - elevation[row][column]) > 1 or \
                                        terrainType[terrainList[row][column + index][0:3]] != "lake":
                                    break
                                else:
                                    img.putpixel((column + index, row), (143, 75, 3))
        img.save(outputPath)
        image = Image.open(outputPath)
        terrainList = []
        data = list(image.getdata())
        i = 0
        j = []
        for pixel in data:
            j.append(pixel)
            i += 1
            if i == c:
                i = 0
                terrainList.append(j)
                j = []
        for i in range(len(newpath) - 1):
            start = newpath[i]
            destination = newpath[i + 1]
            terrainData = []
            for row in range(r):  # MAP size is 500X395
                data = []
                for col in range(c):
                    t1 = Pixels(row, col)
                    t1.elevation = elevation[row][col]
                    t1.type = terrainType[terrainList[row][col][0:3]]
                    data.append(t1)
                terrainData.append(data)
            # calling the path finding algorithm
            pathAlgo(terrainData[start[0]][start[1]], terrainData[destination[0]][destination[1]], terrainData, speed)

    elif season == "winter":  # For winter weather
        speed = winterSpeed
        for row in range(r):
            for column in range(c):
                if terrainType[terrainList[row][column][0:3]] == "ice" or \
                        terrainType[terrainList[row][column][0:3]] == "lake":
                    sides = 0
                    if (row - 1 >= 0 and (terrainType[terrainList[row - 1][column][0:3]] != "lake"
                                         and terrainType[terrainList[row - 1][column][0:3]] != "ice")) or \
                            (row + 1 < r and (terrainType[terrainList[row + 1][column][0:3]] != "lake"
                                            and terrainType[terrainList[row + 1][column][0:3]] != "ice")) or\
                            (column - 1 >= 0 and (terrainType[terrainList[row][column - 1][0:3]] != "lake"
                                              and terrainType[terrainList[row][column - 1][0:3]] != "ice")) or(
                            column + 1 < c and (terrainType[terrainList[row][column + 1][:3]] != "lake"
                                               and terrainType[terrainList[row][column + 1][0:3]] != "ice")):
                        sides = 1
                    if sides == 1:
                        for index in range(7):
                            if row - index < 0 or (terrainType[terrainList[row - index][column][0:3]] != "ice" and
                                                   terrainType[terrainList[row - index][column][0:3]] != "lake"):
                                break
                            else:
                                img.putpixel((column, row - index), (132, 255, 240))
                        for index in range(7):
                            if row + index > 499 or (terrainType[terrainList[row + index][column][0:3]] != "ice" and
                                                     terrainType[terrainList[row + index][column][0:3]] != "lake"):
                                break
                            else:
                                img.putpixel((column, row + index), (132, 255, 240))
                        for index in range(7):
                            if column - index < 0 or (terrainType[terrainList[row][column - index][0:3]] != "ice" and
                                                      terrainType[terrainList[row][column - index][0:3]] != "lake"):
                                break
                            else:
                                img.putpixel((column - index, row), (132, 255, 240))

                        for index in range(7):
                            if column + index > 394 or (terrainType[terrainList[row][column + index][0:3]] != "ice" and
                                                        terrainType[terrainList[row][column + index][0:3]] != "lake"):
                                break
                            else:
                                img.putpixel((column + index, row), (132, 255, 240))
        img.save(outputPath)  # saving the changes to map for winter
        img = Image.open(outputPath)
        terrainList = []
        data = list(img.getdata())
        i = 0
        j = []
        for pixel in data:
            j.append(pixel)
            i += 1
            if i == c:
                i = 0
                terrainList.append(j)
                j = []
        for i in range(len(newpath) - 1):
            start = newpath[i]
            destination = newpath[i + 1]
            terrainData = []
            for row in range(r):  # MAP size is 500X395
                data = []
                for col in range(c):
                    t1 = Pixels(row, col)
                    t1.elevation = elevation[row][col]
                    t1.type = terrainType[terrainList[row][col][0:3]]
                    data.append(t1)
                terrainData.append(data)
            # calling the path finding algorithm
            pathAlgo(terrainData[start[0]][start[1]], terrainData[destination[0]][destination[1]], terrainData, speed)

    elif season == "fall":  # Fall season change
        speed = fallSpeed
        for i in range(len(newpath) - 1):
            start = newpath[i]
            destination = newpath[i + 1]
            terrainData = []
            for row in range(r):  # MAP size is 500X395
                data = []
                for col in range(c):
                    t1 = Pixels(row, col)
                    t1.elevation = elevation[row][col]
                    t1.type = terrainType[terrainList[row][col][0:3]]
                    data.append(t1)
                terrainData.append(data)
            # calling the path finding algorithm
            pathAlgo(terrainData[start[0]][start[1]], terrainData[destination[0]][destination[1]], terrainData, speed)

    else:
        speed = summerSpeed
        for i in range(len(newpath) - 1):
            start = newpath[i]
            destination = newpath[i + 1]
            terrainData = []
            for row in range(r):  # MAP size is 500X395
                data = []
                for col in range(c):
                    t1 = Pixels(row, col)
                    t1.elevation = elevation[row][col]
                    t1.type = terrainType[terrainList[row][col][0:3]]
                    data.append(t1)
                terrainData.append(data)
            # calling the path finding algorithm
            pathAlgo(terrainData[start[0]][start[1]], terrainData[destination[0]][destination[1]], terrainData, speed)

            # print(len(path))
    for ce in newpath:
        img.putpixel((ce[1], ce[0]), (87, 27, 160))
        path.remove(ce)
    img.save(outputPath)
    print(len(path))
    print(len(newpath))
    for cd in path:
        img.putpixel((cd[1], cd[0]), (166, 110, 184))
    img.save(outputPath)


main()
