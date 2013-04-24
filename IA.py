from pathfinder import PathFinder
from gridmap import GridMap

class IA(object):
    def __init__(self, x, y, gameMap):

        self.gridMap = GridMap(gameMap.sizeX+1, gameMap.sizeY+1)
        
        for b in gameMap.collidable:
            self.gridMap.set_blocked(b)
            
        self.pf = PathFinder(self.gridMap.successors, self.gridMap.move_cost, 
        self.gridMap.move_cost)
        
    def _recompute_path(self, xPlayer, yPlayer, xEnt, yEnt):
        self.goal_pos = xPlayer/64,yPlayer/64
        self.start_pos = xEnt, yEnt

        self.path = list(self.pf.compute_path(self.start_pos, self.goal_pos))
