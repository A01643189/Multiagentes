import agentpy as ap
from owlready2 import *
from matplotlib import pyplot as plt
import IPython
import heapq
import numpy as np

onto = get_ontology("file://ontologia.owl")

# with onto:

#   class Robot(Thing):
#     pass

#   class RobotList(Thing):
#     pass

#   class Box(Thing):
#     pass

#   class Obstacle(Thing):
#     pass

#   class has_obstacle(ObjectProperty):
#     domain = [Robot]
#     range = [Obstacle]

#   class has_box(ObjectProperty):
#     domain = [Robot]
#     range = [Box]

#   class Hole(Thing):
#     pass

#   class hole_capacity(ObjectProperty):
#     domain = [Hole]
#     range = [int]

class Node():
    def __init__(self, position, g=0, h=0, parent=None):
        self.position = position
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent

    def __lt__(self, other):
        return self.f < other.f

def manhattan_distance(a, b):
    return abs(a[0] - a[1]) + abs(b[0] - b[1])

def a_star(start, goal, grid):
    start_node = Node(start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(goal)
    end_node.g = end_node.h = end_node.f = 0

    open_list = []
    closed_list = set()

    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)

        if current_node.position == goal:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        closed_list.add(current_node.position)

        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if (node_position[0] < 0 or node_position[0] >= grid.shape[0] or
                node_position[1] < 0 or node_position[1] >= grid.shape[1]):
                continue

            if node_position in closed_list:
                continue

            # If the position is occupied by an obstacle, skip it
            if grid[node_position[0], node_position[1]] == 1:
                continue

            new_node = Node(node_position, parent=current_node)
            new_node.g = current_node.g + 1
            new_node.h = manhattan_distance(new_node.position, goal)
            new_node.f = new_node.g + new_node.h

            if new_node not in open_list:
                heapq.heappush(open_list, new_node)
            else:
                open_node = next(node for node in open_list if node.position == new_node.position)
                if new_node.g < open_node.g:
                    open_list.remove(open_node)
                    heapq.heappush(open_list, new_node)

    return None  # No path found

class VacuumAgent(ap.Agent):
    def setup(self):
        self.agentType = 1
        self.carrying_box = False
        self.path = []

    def step(self):
        if not self.path:
            if not self.carrying_box:
              # Find the nearest box
              boxes = [agent for agent in self.model.boxList if not agent.picked_up]
              if boxes:
                agent_pos = self.model.grid.positions[self]
                nearest_box = min(boxes, key=lambda box: manhattan_distance(agent_pos, self.model.grid.positions[box]))
                self.path = a_star(agent_pos, self.model.grid.positions[nearest_box], self.model.grid_array)
              else:
                return  # No more boxes to pick up
            else:
                # Find the nearest hole
                holes = [agent for agent in self.model.holeList if not agent.dropped]
                if holes:
                  self.path = []
                  agent_pos = self.model.grid.positions[self]
                  nearest_hole = min(holes, key=lambda hole: manhattan_distance(agent_pos, self.model.grid.positions[hole]))
                  self.path = a_star(agent_pos, self.model.grid.positions[nearest_hole], self.model.grid_array)
                else:
                    return  # No holes available

        if self.path:
            next_position = self.path.pop(0)
            self.model.grid.move_to(self, next_position)

            if not self.carrying_box:
                # Check if we've reached a box
                box_here = next((box for box in self.model.boxList if self.model.grid.positions[box] == next_position and not box.picked_up), None)
                if box_here:
                    self.pick_up_box(box_here)
            else:
                # Check if we've reached a hole
                hole_here = next((hole for hole in self.model.holeList if self.model.grid.positions[hole] == next_position), None)
                if hole_here:
                    self.drop_off_box(hole_here)

    def pick_up_box(self, box):
      self.carrying_box = True
      box.picked_up = True
      self.model.grid.remove_agents(box)  # Remove the box from the grid
      self.model.boxList.remove(box)  # Remove the box from the box list
      self.path = []  # Clear the path after picking up a box

    def drop_off_box(self, hole):
        self.carrying_box = False
        hole.dropped = True
        self.path = []  # Clear the path after dropping off the box

class BoxAgent(ap.Agent):
    def setup(self):
        self.agentType = 3
        self.picked_up = False

class HoleAgent(ap.Agent):
    def setup(self):
        self.agentType = 2
        self.dropped = False

class ObstacleAgent(ap.Agent):
    def setup(self):
        self.agentType = 4

class VacuumModel(ap.Model):
    def setup(self):
        self.grid = ap.Grid(self, (self.p.M, self.p.N), track_empty=True)
        self.agents = ap.AgentList(self, self.p.vacuums, VacuumAgent)
        self.boxList = ap.AgentList(self, self.p.boxes, BoxAgent)
        self.holeList = ap.AgentList(self, self.p.holes, HoleAgent)
        self.obstacleList = ap.AgentList(self, self.p.obstacles, ObstacleAgent)

        # Define fixed positions for obstacles
        obstacle_positions = [
            (6, 4), (5, 4), (4, 4),
            (3, 4), (2, 4), (1, 4),
            (0, 4), (9, 8), (8, 8),
            (7, 8), (6, 8), (5, 8),
            (4, 8), (3, 8)
        ]

        hole_positions = [
            (9, 2), (0, 6), (9, 6),
            (0, 9), (9, 9)
        ]

        # Combine obstacle and hole positions into a set of invalid positions
        invalid_positions = set(obstacle_positions + hole_positions)

        # Add obstacles and holes to the grid
        self.grid.add_agents(self.holeList, positions=hole_positions)
        self.grid.add_agents(self.obstacleList, positions=obstacle_positions)

        # Get all valid positions on the grid that are not occupied by obstacles or holes
        all_positions = [(x, y) for x in range(self.p.M) for y in range(self.p.N)]
        valid_positions = [pos for pos in all_positions if pos not in invalid_positions]

        # Ensure that we have enough positions for agents and boxes
        assert len(valid_positions) >= len(self.agents) + len(self.boxList), "Not enough valid positions for agents and boxes."

        # Sample positions for agents and boxes
        agent_positions = self.random.sample(valid_positions, len(self.agents))
        remaining_positions = [pos for pos in valid_positions if pos not in agent_positions]
        box_positions = self.random.sample(remaining_positions, len(self.boxList))

        # Add agents and boxes to the grid at sampled positions
        self.grid.add_agents(self.agents, positions=agent_positions)
        self.grid.add_agents(self.boxList, positions=box_positions)

        # Create a numpy array to represent the grid for A* pathfinding
        self.grid_array = np.zeros((self.p.M, self.p.N))

        # Place obstacles on the grid array based on fixed positions
        for pos in obstacle_positions:
            self.grid_array[pos[0], pos[1]] = 1  # Mark obstacle positions as 1

    def step(self):
        self.agents.step()

    def update(self):
        pass

    def end(self):
        pass


parameters = {
    'vacuums': 5,
    'boxes': 10,
    'holes': 5,
    'obstacles': 14,
    'M': 10,
    'N': 10,
    'steps': 100,
    'seed': 12345,
}

model = VacuumModel(parameters)
model.run()

def animation_plot(model, ax):
    agent_type_grid = model.grid.attr_grid('agentType')
    ap.gridplot(agent_type_grid, cmap='Accent', ax=ax)
    ax.set_title(f"Vacuum Model \n Time-step: {model.t}, "
                 f"Boxes left: {sum(1 for box in model.boxList if not box.picked_up)}, ")

# SIMULATION:
fig, ax = plt.subplots()
model = VacuumModel(parameters)
animation = ap.animate(model, fig, ax, animation_plot)
IPython.display.HTML(animation.to_jshtml())

def test():
    print("Test")
    parameters={ 'vacuums': 5,
    'boxes': 10,
    'holes': 5,
    'obstacles': 14,
    'M': 10,
    'N': 10,
    'steps': 100,
    'seed': 12345,}
    model = VacuumModel(parameters)
    model.setup()
    model.step()