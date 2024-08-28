import agentpy as ap
from owlready2 import *
from matplotlib import pyplot as plt
import IPython
import heapq
import numpy as np
import json  # Import JSON module

onto = get_ontology("file://ontologia.owl")

with onto:
    class Drone(Thing):
        pass

    class DroneList(Thing):
        pass

    class Box(Thing):
        pass

    class Obstacle(Thing):
        pass
    
    class Place(Thing):
        pass
    
    class has_place(ObjectProperty, FunctionalProperty):
        domain = [Drone, Box]
        range = [Place]

    class has_obstacle(ObjectProperty):
        domain = [Drone]
        range = [Obstacle]

    class has_box(ObjectProperty):
        domain = [Drone]
        range = [Box]

    class Hole(Thing):
        pass

    # Definir capacidad del agujero como atributo
    Hole.hole_capacity = 5

    # Add a data property to track the robot's position in JSON format
    class position_x(DataProperty, FunctionalProperty):
        domain = [Drone]
        range = [int]

    class position_y(DataProperty, FunctionalProperty):
        domain = [Drone]
        range = [int]

class Node():
    def __init__(self, position, g=0, h=0, parent=None):  # Fixed __init__ method
        self.position = position
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent

    def __lt__(self, other):  # Fixed __lt__ method
        return self.f < other.f

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Corrected manhattan distance function

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

class DroneAgent(ap.Agent):
    
    def see(self, e):
        self.per = []
        neighbors = e.neighbors(self)
        
        for neighbor in neighbors:
            neighbor_pos = e.positions[neighbor]
            if isinstance(neighbor, BoxAgent):
                perception = {
                    'agent': self.owl_instance,  # The drone agent itself
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
            else:
                continue
            
            # Append the perception to the drone's perception list
            self.per.append(perception)
        
    
    def drop_off_box(self, hole):
        self.carrying_box = False
        hole.dropped = True
        hole.box_count += 1  # Increment box count

        # Check if the hole is now full
        if hole.box_count >= hole.owl_instance.hole_capacity[0]:
            hole.owl_instance.is_full = True  # Mark the hole as full in the ontology
            print(f"Hole {hole.name} is full.")

        if self.owl_instance.has_box:
            box_to_remove = self.owl_instance.has_box[0]  # Get the first box (if any)
            self.owl_instance.has_box.remove(box_to_remove)  # Remove the box

        self.path = []

    def is_hole_full(self, hole):
        """ Check if a hole is full """
        return hole.box_count >= hole.owl_instance.hole_capacity[0]
        
    
    def setup(self):
        self.agentType = 1
        self.carrying_box = False
        self.path = []

        # Assign a unique name to the agent
        self.name = f"Drone_{self.id}"

        # Associate this agent with the Robot class in the ontology
        self.owl_instance = onto.Robot(self.name)

        # Initialize position attributes, but don't update in ontology yet
        self.position_x = None
        self.position_y = None

    def step(self):
        # Update position in ontology at the start of each step
        self.update_position_in_ontology()

        if not self.path:
            if not self.carrying_box:
                # Search for the nearest box and associate with the ontology
                boxes = [agent for agent in self.model.boxList if not agent.picked_up]
                if boxes:
                    agent_pos = self.model.grid.positions[self]
                    nearest_box = min(boxes, key=lambda box: manhattan_distance(agent_pos, self.model.grid.positions[box]))

                    # Associate the box with the robot in the ontology
                    self.owl_instance.has_box.append(nearest_box.owl_instance)

                    self.path = a_star(agent_pos, self.model.grid.positions[nearest_box], self.model.grid_array)
                else:
                    return
            else:
                # Search for the nearest hole and associate with the ontology
                holes = [agent for agent in self.model.holeList if not agent.dropped]
                if holes:
                    agent_pos = self.model.grid.positions[self]
                    nearest_hole = min(holes, key=lambda hole: manhattan_distance(agent_pos, self.model.grid.positions[hole]))

                    # Here you could use the hole capacity defined in the ontology
                    if nearest_hole.owl_instance.hole_capacity and nearest_hole.owl_instance.hole_capacity[0] > 0:
                        self.owl_instance.hole_capacity = [nearest_hole.owl_instance.hole_capacity[0] - 1]
                        self.path = a_star(agent_pos, self.model.grid.positions[nearest_hole], self.model.grid_array)
                    else:
                        return
        if self.path:
            next_position = self.path.pop(0)
            self.model.grid.move_to(self, next_position)

            if not self.carrying_box:
                box_here = next((box for box in self.model.boxList if self.model.grid.positions[box] == next_position and not box.picked_up), None)
                if box_here:
                    self.pick_up_box(box_here)
                    box_here.owl_instance.estaEn = [str(next_position)]
            else:
                hole_here = next((hole for hole in self.model.holeList if self.model.grid.positions[hole] == next_position), None)
                if hole_here:
                    self.drop_off_box(hole_here)
                    hole_here.owl_instance.estaEn = [str(next_position)]

    def pick_up_box(self, box):
        self.carrying_box = True
        box.picked_up = True
        self.model.grid.remove_agents(box)
        self.model.boxList.remove(box)
        self.owl_instance.has_box.append(box.owl_instance)
        self.path = []

    def drop_off_box(self, hole):
        self.carrying_box = False
        hole.dropped = True
        if self.owl_instance.has_box:
            box_to_remove = self.owl_instance.has_box[0]  # Get the first box (if any)
            self.owl_instance.has_box.remove(box_to_remove)  # Remove the box
        self.path = []

    def update_position_in_ontology(self):
        # Get current position from the model
        current_position = self.model.grid.positions[self]
        # Update the position in the ontology
        self.owl_instance.position_x = current_position[0]
        self.owl_instance.position_y = current_position[1]

        # Convert to JSON format
        position_json = json.dumps({
            "robot_id": self.id,
            "position": {
                "x": self.owl_instance.position_x,
                "y": self.owl_instance.position_y
            }
        })

        # Print the JSON string (or handle it as needed)
        print(position_json)

class BoxAgent(ap.Agent):
    def setup(self):
        self.agentType = 3
        self.picked_up = False

        # Asignar un nombre único al agente
        self.name = f"Box_{self.id}"

        # Asociar con la ontología
        self.owl_instance = onto.Box(self.name)

class HoleAgent(ap.Agent):
    def setup(self):
        self.agentType = 2
        self.dropped = False
        self.box_count = 0  # Track how many boxes are in the hole

        # Assign a unique name to the agent
        self.name = f"Hole_{self.id}"

        # Associate with the ontology
        self.owl_instance = onto.Hole(self.name)

        # Set initial capacity
        self.owl_instance.hole_capacity = [5]  # Note: assigned as a list

class ObstacleAgent(ap.Agent):
    def setup(self):
        self.agentType = 4
        self.name = f"Obstacle_{self.id}"
        # Asociar con la ontología
        self.owl_instance = onto.Obstacle(self.name)

class DroneModel(ap.Model):
    def setup(self):
        self.grid = ap.Grid(self, (self.p.M, self.p.N), track_empty=True)
        self.agents = ap.AgentList(self, self.p.agents, DroneAgent)
        self.holeList = ap.AgentList(self, self.p.holes, HoleAgent)
        self.boxList = ap.AgentList(self, self.p.boxes, BoxAgent)
        self.obstaclesList = ap.AgentList(self, self.p.obstacles, ObstacleAgent)
        
        # Place agents randomly
        self.grid.add_agents(self.agents, random=True, empty=True)
        self.grid.add_agents(self.holeList, random=True, empty=True)
        self.grid.add_agents(self.boxList, random=True, empty=True)
        self.grid.add_agents(self.obstaclesList, random=True, empty=True)
        
        # Initialize grid array for A* algorithm
        self.grid_array = np.zeros((self.p.M, self.p.N), dtype=int)
        for obstacle in self.obstaclesList:
            pos = self.grid.positions[obstacle]
            self.grid_array[pos[0], pos[1]] = 1  # Mark obstacle positions as occupied

    def step(self):
        self.agents.step()

# Simulation parameters
parameters = {
    'M': 10,
    'N': 10,
    'agents': 1,
    'boxes': 2,
    'holes': 1,
    'obstacles': 2,
    'steps': 20
}

# Run the simulation
model = DroneModel(parameters)
results = model.run()

# Visualize the final positions of the agents
plt.figure(figsize=(8, 8))
plt.imshow(model.grid_array, cmap='Greys', origin='upper', extent=[0, parameters['M'], 0, parameters['N']])
agent_positions = np.array(list(model.grid.positions.values()))
plt.scatter(agent_positions[:, 1], parameters['M'] - agent_positions[:, 0], c='blue', label='Drone Agents')
plt.legend()
plt.show()
