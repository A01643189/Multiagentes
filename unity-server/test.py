import agentpy as ap
from owlready2 import *
from matplotlib import pyplot as plt
import IPython.display as display  # Import IPython display
from IPython.display import JSON  # Import IPython JSON display
import heapq
import numpy as np
import json

# Load the ontology
onto = get_ontology("file://ontologia.owl")

with onto:
    class Robot(Thing):
        pass

    class RobotList(Thing):
        pass

    class Box(Thing):
        pass

    class Obstacle(Thing):
        pass

    class Place(Thing):
        pass

    class has_place(ObjectProperty, FunctionalProperty):
        domain = [Robot, Box]
        range = [Place]

    class has_obstacle(ObjectProperty):
        domain = [Robot]
        range = [Obstacle]

    class has_box(ObjectProperty):
        domain = [Robot]
        range = [Box]

    class Hole(Thing):
        pass

    class hole_capacity(DataProperty, FunctionalProperty):
        domain = [Hole]
        range = [int]

    class position_x(DataProperty, FunctionalProperty):
        domain = [Robot]
        range = [int]

    class position_y(DataProperty, FunctionalProperty):
        domain = [Robot]
        range = [int]

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
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, goal, grid):
    start_node = Node(start)
    end_node = Node(goal)

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

            if node_position in closed_list or grid[node_position[0], node_position[1]] == 1:
                continue

            new_node = Node(node_position, parent=current_node)
            new_node.g = current_node.g + 1
            new_node.h = manhattan_distance(new_node.position, goal)
            new_node.f = new_node.g + new_node.h

            if new_node.position not in [node.position for node in open_list]:
                heapq.heappush(open_list, new_node)
            else:
                open_node = next(node for node in open_list if node.position == new_node.position)
                if new_node.g < open_node.g:
                    open_list.remove(open_node)
                    heapq.heappush(open_list, new_node)

    # Return an empty list if no path found
    return []


class RobotAgent(ap.Agent):

    def see(self, e):
        self.per = []
        neighbors = e.neighbors(self)

        for neighbor in neighbors:
            neighbor_pos = e.positions[neighbor]
            if isinstance(neighbor, BoxAgent):
                perception = {
                    'agent': self.owl_instance,
                    'perception': Box(has_place=Place(has_position=str(neighbor_pos))),
                }
            elif isinstance(neighbor, HoleAgent):
                is_full = self.is_hole_full(neighbor)
                perception = {
                    'agent': self.owl_instance,
                    'perception': Hole(has_place=Place(has_position=str(neighbor_pos)), is_full=is_full),
                }
            elif isinstance(neighbor, ObstacleAgent):
                perception = {
                    'agent': self.owl_instance,
                    'perception': Obstacle(has_place=Place(has_position=str(neighbor_pos))),
                }
            elif isinstance(neighbor, RobotAgent):
                perception = {
                    'agent': self.owl_instance,
                    'perception': Robot(has_place=Place(has_position=str(neighbor_pos))),
                }
            else:
                continue

            self.per.append(perception)


    def drop_off_box(self, hole):
        self.carrying_box = False
        hole.dropped = True
        hole.box_count += 1

        # Update the hole’s capacity status
        if hole.box_count >= hole.owl_instance.hole_capacity:
            hole.owl_instance.is_full = True
            print(f"Hole {hole.name} is full.")

        if self.owl_instance.has_box:
            box_to_remove = self.owl_instance.has_box[0]
            self.owl_instance.has_box.remove(box_to_remove)

        self.path = []


    def is_hole_full(self, hole):
        # Check if the current hole has reached its capacity
        return hole.box_count >= hole.owl_instance.hole_capacity




    def setup(self):
        self.agentType = 1
        self.carrying_box = False
        self.path = []

        self.name = f"Drone_{self.id}"
        self.owl_instance = onto.Robot(self.name)

        self.position_x = None
        self.position_y = None

    def step(self):
        self.update_position_in_ontology()

        if not self.path:
            if not self.carrying_box:
                boxes = [agent for agent in self.model.boxList if not agent.picked_up]
                if boxes:
                    agent_pos = self.model.grid.positions[self]
                    nearest_box = min(boxes, key=lambda box: manhattan_distance(agent_pos, self.model.grid.positions[box]))
                    self.path = a_star(agent_pos, self.model.grid.positions[nearest_box], self.model.grid_array)
                    print(f"Robot {self.name} path to box: {self.path}")
                else:
                    print(f"Robot {self.name}: No boxes left to pick up.")
                    return
            else:
                holes = [agent for agent in self.model.holeList if not self.is_hole_full(agent)]
                if holes:
                    agent_pos = self.model.grid.positions[self]
                    nearest_hole = min(holes, key=lambda hole: manhattan_distance(agent_pos, self.model.grid.positions[hole]))
                    self.path = a_star(agent_pos, self.model.grid.positions[nearest_hole], self.model.grid_array)
                    print(f"Robot {self.name} path to hole: {self.path}")
                else:
                    print(f"Robot {self.name}: No valid holes left to drop off boxes.")
                    return

        if self.path:
            next_position = self.path.pop(0)
            self.model.grid.move_to(self, next_position)
            print(f"Robot {self.name} moved to {next_position}.")

            if not self.carrying_box:
                box_here = next((box for box in self.model.boxList if self.model.grid.positions[box] == next_position and not box.picked_up), None)
                if box_here:
                    self.pick_up_box(box_here)
            else:
                hole_here = next((hole for hole in self.model.holeList if self.model.grid.positions[hole] == next_position), None)
                if hole_here:
                    self.drop_off_box(hole_here)
                    print(f"Robot {self.name} dropped box at hole {hole_here.name}.")



    def pick_up_box(self, box):
        self.carrying_box = True
        box.picked_up = True
        self.model.grid.remove_agents(box)
        self.model.boxList.remove(box)
        self.owl_instance.has_box.append(box.owl_instance)
        self.path = []

    def update_position_in_ontology(self):
        current_position = self.model.grid.positions[self]
        self.owl_instance.position_x = current_position[0]
        self.owl_instance.position_y = current_position[1]

        position_json = json.dumps({
            "robot_id": self.id,
            "position": {
                "x": self.owl_instance.position_x,
                "y": self.owl_instance.position_y
            }
        })

        # Use IPython to display JSON in a formatted way
        display.display(JSON(position_json))

class BoxAgent(ap.Agent):
    def setup(self):
        self.agentType = 3
        self.picked_up = False
        self.name = f"Box_{self.id}"
        self.owl_instance = onto.Box(self.name)

class HoleAgent(ap.Agent):
    def setup(self):
        self.agentType = 2
        self.dropped = False
        self.box_count = 0
        self.name = f"Hole_{self.id}"
        self.owl_instance = onto.Hole(self.name)
        self.owl_instance.hole_capacity = 5


class ObstacleAgent(ap.Agent):
    def setup(self):
        self.agentType = 4
        self.name = f"Obstacle_{self.id}"
        self.owl_instance = onto.Obstacle(self.name)

class DroneModel(ap.Model):
    def setup(self):
        self.grid = ap.Grid(self, (self.p.M, self.p.N), track_empty=True)
        self.agents = ap.AgentList(self, self.p.agents, RobotAgent)
        self.holeList = ap.AgentList(self, self.p.holes, HoleAgent)
        self.boxList = ap.AgentList(self, self.p.boxes, BoxAgent)
        self.obstaclesList = ap.AgentList(self, self.p.obstacles, ObstacleAgent)

        self.grid.add_agents(self.agents, random=True, empty=True)
        self.grid.add_agents(self.holeList, random=True, empty=True)
        self.grid.add_agents(self.boxList, random=True, empty=True)
        self.grid.add_agents(self.obstaclesList, random=True, empty=True)

        self.grid_array = np.zeros((self.p.M, self.p.N), dtype=int)
        for obstacle in self.obstaclesList:
            pos = self.grid.positions[obstacle]
            self.grid_array[pos[0], pos[1]] = 1

    def step(self):
        self.agents.step()

# Simulation parameters
parameters = {
    'M': 20,
    'N': 20,
    'agents': 5,
    'boxes': 20,
    'holes': 4,
    'obstacles': 2,
    'steps': 100
}

# Run the simulation
model = DroneModel(parameters)
results = model.run()

# Visualize the final positions of the agents
plt.figure(figsize=(8, 8))
plt.imshow(model.grid_array, cmap='Greys', origin='upper', extent=[0, parameters['M'], 0, parameters['N']])
agent_positions = np.array(list(model.grid.positions.values()))
plt.scatter(agent_positions[:, 1], parameters['M'] - agent_positions[:, 0], c='blue', label='Robot Agents')
plt.legend()
plt.show()
