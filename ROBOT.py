import pygame
import math
import numpy as np

def distance(point1, point2):
    point1 = np.array(point1)
    point2 = np.array(point2)
    return np.linalg.norm(point1 - point2)

class Robot:
    def __init__(self, startpos, width):
        self.m2p = 3779.52
        self.w = width
        self.x = startpos[0]
        self.y = startpos[1]
        self.heading = 0

        self.vl = 0.01 * self.m2p
        self.vr = 0.01 * self.m2p

        self.maxspeed = 0.02 * self.m2p
        self.minspeed = 0.01 * self.m2p

        self.min_obs_dist = 100
        self.count_down = 5
        self.angular_velocity = 0.01  # Initial angular velocity
        self.angular_velocity_multiplier = 2  # Multiplier for angular velocity when avoiding obstacles
        self.angular_velocity_timeout = 1.0  # Duration for increased angular velocity (in seconds)
        self.angular_velocity_timer = 0.0

    def avoid_obstacles(self, point_cloud, dt):
        closest_obs = None
        dist = np.inf

        if len(point_cloud) > 1:
            for point in point_cloud:
                curr_dist = distance([self.x, self.y], point)
                if curr_dist < dist:
                    dist = curr_dist
                    closest_obs = (point, dist)

            if closest_obs[1] < self.min_obs_dist and self.count_down > 0:
                self.count_down -= dt
                self.angular_velocity_timer = self.angular_velocity_timeout
                self.update_angular_velocity()
                self.move_backward()
            else:
                # reset count down and angular velocity
                self.count_down = 5
                self.angular_velocity = 0.01
                self.move_forward()

        if self.angular_velocity_timer > 0:
            self.angular_velocity_timer -= dt
            self.update_angular_velocity()

    def update_angular_velocity(self):
        self.angular_velocity = self.angular_velocity_multiplier * self.maxspeed

    def move_backward(self):
        self.vr = -self.minspeed  # Reverse the robot
        self.vl = -self.minspeed / 2

    def move_forward(self):
        self.vr = self.minspeed
        self.vl = self.minspeed

    def kinematics(self, dt):
        cos_heading = math.cos(self.heading)
        sin_heading = math.sin(self.heading)
        v_avg = (self.vl + self.vr) / 2
        self.x += v_avg * cos_heading * dt
        self.y -= v_avg * sin_heading * dt
        self.heading += self.angular_velocity * (self.vr - self.vl) / self.w * dt

        if self.heading > 2 * math.pi or self.heading < -2 * math.pi:
            self.heading = 0

        self.vr = max(min(self.maxspeed, self.vr), self.minspeed)
        self.vl = max(min(self.maxspeed, self.vl), self.minspeed)


class Graphics:
    def __init__(self, dimensions, robot_img_path, map_img_path):
        pygame.init()
        # COLORS
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        self.yel = (255, 255, 0)

        # load imgs
        self.robot = pygame.image.load(robot_img_path)
        self.map_img = pygame.image.load(map_img_path)

        # dimensions
        self.height, self.width = dimensions

        # window settings
        pygame.display.set_caption("Obstacle Avoidance")
        self.map = pygame.display.set_mode((self.width, self.height))
        self.map.blit(self.map_img, (0, 0))

    def draw_robot(self, x, y, heading):
        rotated = pygame.transform.rotozoom(self.robot, math.degrees(heading), 1)
        rect = rotated.get_rect(center=(x, y))
        self.map.blit(rotated, rect)

    def draw_sensor_data(self, point_cloud):
        for point in point_cloud:
            pygame.draw.circle(self.map, self.red, point, 3, 0)

class Ultrasonic:
    def __init__(self, sensor_range, map):
        self.sensor_range = sensor_range
        self.map_width, self.map_height = pygame.display.get_surface().get_size()
        self.map = map

    def sense_obstacles(self, x, y, heading):
        obstacles = []
        x1, y1 = x, y
        start_angle = heading - self.sensor_range[1]
        finish_angle = heading + self.sensor_range[1]
        for angle in np.linspace(start_angle, finish_angle, 10, endpoint=False):
            x2 = x1 + self.sensor_range[0] * math.cos(angle)
            y2 = y1 - self.sensor_range[0] * math.sin(angle)
            for i in range(0, 100):
                u = i / 100
                x = int(x2 * u + x1 * (1 - u))
                y = int(y2 * u + y1 * (1 - u))
                if 0 < x < self.map_width and 0 < y < self.map_height:
                    color = self.map.get_at((x, y))
                    self.map.set_at((x, y), (0, 208, 255))
                    if color == (0, 0, 0):
                        obstacles.append([x, y])
                        break
        return obstacles