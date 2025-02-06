# **TC2008B: Multi-Agent System Modeling with Computer Graphics**

## **Integrative Activity**

### **Part 1: Multi-Agent Systems**

#### **Problem Description**
Congratulations! You are now the proud owner of five new robots and a warehouse full of scattered objects. The previous owner left the warehouse in complete disarray, and it is up to your robots to organize the objects efficiently and turn the warehouse into a successful business.

Each robot is equipped with **powerful traction systems**, allowing them to move across any terrain and rotate in any direction. They can **pick up objects** from grid cells in front of them using their manipulators, transport them, and **stack them into piles of up to five objects**.

The robots feature **advanced sensors** that provide real-time data on the **four adjacent cells**, helping them determine if a cell is:
- Empty
- A wall
- Occupied by a stack of objects (with stack height information)
- Occupied by another robot

Additionally, robots have **pressure sensors** to detect whether they are currently carrying an object. They also possess **mapping capabilities** to navigate the warehouse efficiently.

Your task is to **teach the robots how to organize the warehouse**, ensuring all objects are properly stacked into ordered piles of five.

#### **Simulation**
- **Initialization**: Objects (K) are placed randomly on the floor.
- **Agent Positioning**: Robots start at random empty positions.
- **Execution**: The simulation runs until the maximum allowed time or step limit is reached.

#### **Data Collection**
During execution, the system gathers the following data:
- Time required to organize all objects into stacks of five.
- Number of moves performed by each robot.
- Strategies to reduce execution time and optimize movements.

#### **Key Considerations**
- Robots can use **deductive reasoning, practical reasoning, or a hybrid approach**.
- Implement a **basic collision detection system** to prevent crashes (e.g., stopping before a collision and assigning priority to a robot).
- Robots **can only move forward** but can rotate in place to change direction.
- **Ontology-based agent design** is required.

---

### **Part 2: Computer Graphics**

#### **Problem Description**
This part follows the same warehouse organization concept as **Part 1**, but with a **3D simulation using Unity**.

#### **Requirements**
- **3D Modeling**:
  - Warehouse structure, shelves, objects, and at least five robots.
  - Models should include **materials (colors) and UV-mapped textures**.

- **Animation**:
  - Robots move through warehouse aisles, picking up and stacking objects.

- **Lighting**:
  - **At least one directional light source** (e.g., warehouse overhead lights).
  - **Each robot must have a moving point light** (e.g., siren-style indicator).

- **Collision Detection**:
  - Robots move along predefined paths at random speeds and detect collisions dynamically.

---

### **Part 3: Computer Vision**

#### **Problem Description**
This part follows the same warehouse organization concept as **Part 1**, incorporating **real-time object detection using YOLOv8**.

#### **Requirements**
- **Object Identification**:
  - Each robot is equipped with a **camera**, which can be positioned forward-facing or dynamically adjusted.
  - The camera **streams data to a YOLOv8-based vision model** to classify detected objects.
  - When an object is identified, the system **displays a dialogue bubble above the robot** (e.g., "This is an apple!").

---

## **Project Setup & Execution**

To **run the project**, follow these steps:

### **1. Install Dependencies**
Ensure you have **Node.js** installed, then run:
```bash
npm install
```

### **2. Start the Server**
Once dependencies are installed, start the backend server using:
```bash
npm start
```

### **3. Open the Unity Simulation**
To run the **3D warehouse simulation**, follow these steps:

1. Open **Unity Hub** and navigate to the project directory.
2. Open the Unity project and ensure all assets and dependencies are properly imported.
3. Click on **Play** in the Unity Editor to start the simulation.
4. Ensure the **Node.js server remains running** in the terminal to allow real-time agent interaction.

Once the simulation starts, the robots will autonomously navigate, detect objects, and stack them while interacting with the environment.

