# Obstacle Avoidance Robot

## Overview
- This project simulates an obstacle avoidance robot using Python.
- The robot is equipped with an ultrasonic sensor to detect obstacles and navigate its environment.
- The simulation uses `pygame` for graphical representation and `numpy` for mathematical calculations.

## Features
- **Obstacle Detection**: The robot uses an ultrasonic sensor to detect obstacles within a certain range.
- **Obstacle Avoidance**: The robot adjusts its movement based on the detected obstacles to avoid collisions.
- **Simulation Graphics**: Visual representation of the robot, its environment, and sensor data using `pygame`.

## Files
- `Robot.py`: Contains the main logic for the robot's movement, obstacle avoidance, and kinematics.
- `main.py`: The entry point of the simulation, which initializes the graphics, robot, and sensor, and runs the simulation loop.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/obstacle-avoidance-robot.git
   cd obstacle-avoidance-robot
   ```
2. Install the required dependencies:
   ```bash
   pip install pygame numpy
   ```

## Usage
1. Place your images (`DDR.png` and `ObstacleMap.png`) in the same directory as `main.py`.
2. Run the simulation:
   ```bash
   python main.py
   ```
   The simulation window will open, displaying the robot and its environment. The robot will attempt to avoid obstacles as it moves.

## Code Overview
### `Robot.py`
- `Robot` class: Manages the robot's position, speed, heading, and obstacle avoidance logic.
- `Graphics` class: Handles the rendering of the robot and sensor data.
- `Ultrasonic` class: Simulates the ultrasonic sensor's detection of obstacles.

### `main.py`
- Initializes the graphics, robot, and ultrasonic sensor.
- Runs the simulation loop, updating the robot's position and rendering the environment and sensor data.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements
- `pygame`: For graphical rendering and event handling.
- `numpy`: For mathematical operations.

## Contact
For any questions or suggestions, please contact chinmayymulgund@gmail.com or create an issue on the GitHub repository.
