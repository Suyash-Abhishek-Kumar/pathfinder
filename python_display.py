import pygame
from os import environ
from math import dist
from Graph import Graph
from node import Button
import setLayout
from random import randint

pygame.init()


def scale(lst, num):
    lst_new = []
    for i in lst: lst_new.append(i * num)
    return lst_new


def ask():
    while True:
        l = []
        name = input("Name: ")
        try:
            num = int(input("no. of Connections: "))
            for i in range(num):
                l.append(input("Node: "))
        except ValueError:
            num = int(input("no. of Connections (number): "))
        return name, l


environ['SDL_VIDEO_WINDOW_POS'] = "300, 200"


class Display:
    def __init__(self):
        self.screen = pygame.display.set_mode((300, 200))
        pygame.display.set_caption("Shopping Cart PathFinder")
        self.layout = pygame.image.load('.\\graphics\\layout.jpeg').convert()
        self.layout_size = list(self.layout.get_size())
        self.screen = pygame.display.set_mode(scale(self.layout_size, 1.3))
        self.layout = pygame.transform.scale(self.layout, scale(self.layout_size, 1.3))
        self.pathfinder = Graph({})
        self.graph = {}
        self.selected_nodes = []
        self.shortest_path = []
        self.next_node = 'A'
        self.shifted = False
        self.all = False
        self.can_press = True
        self.key_cooldown = 1000
        self.last_key_press = pygame.time.get_ticks()
        self.cur_pos = [0, 0]
        self.clock = pygame.time.Clock()

    def run(self):
        self.add_graph()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        node = self.select_node()
                        if node:
                            if node.selected:
                                node.selected = False
                                self.selected_nodes.remove(node.name)
                            else:
                                self.remove_node(node)
                    elif event.button == 1:
                        if not self.select_node() and self.shifted:
                            name, args = ask()
                            self.add_node(pygame.mouse.get_pos(), name, args)
                        else:
                            node = self.select_node()
                            if node and not node.selected:
                                if len(self.selected_nodes) == 2:
                                    unselect = self.selected_nodes.pop()
                                    for i in self.graph:
                                        if self.graph[i].name == unselect:
                                            self.graph[i].selected = False
                                node.selected = True
                                self.selected_nodes.append(node.name)
                                if len(self.selected_nodes) == 2:
                                    self.pathFind()

            self.screen.blit(self.layout, (0, 0))
            if self.all:
                self.draw_all_connections()
            else:
                self.display_path()
            self.controller()
            for i in self.graph: self.graph[i].display()
            self.check_temp()
            self.cooldown()
            pygame.display.update()
            self.clock.tick(60)

    def check_temp(self):
        if 'temp' not in self.graph:
            self.add_node((-5, -5), 'temp', None)

    def get_all_coords(self):
        for i in self.graph:
            node = self.graph[i]
            print(node.name, node.coords)

    def controller(self):
        if self.can_press:
            flag = True
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.cur_pos[1] -= 5
            elif keys[pygame.K_a]:
                self.cur_pos[0] -= 5
            elif keys[pygame.K_s]:
                self.cur_pos[1] += 5
            elif keys[pygame.K_d]:
                self.cur_pos[0] += 5
            elif keys[pygame.K_p]:
                self.get_all_coords()
            elif keys[pygame.K_o]:
                self.all = not self.all
            elif keys[pygame.K_SPACE]:
                self.add_node(self.cur_pos.copy(), *ask())
                print(self.pathfinder.print_graph(), end='\n')
            elif keys[pygame.K_LSHIFT]:
                self.shifted = True
            elif not keys[pygame.K_LSHIFT]:
                self.shifted = False
            else:
                flag = False
            if flag:
                self.last_key_press = pygame.time.get_ticks()
                self.can_press = False

    def add_graph(self):
        for i in setLayout.l:
            self.add_node(setLayout.l[i], i, [k for k in setLayout.graph[i]])

    def add_node_alpha(self, coords, args):
        node = (self.next_node, coords)
        self.graph[self.next_node] = Button(self.screen, self.next_node, coords)
        self.next_node = chr(ord(self.next_node) + 1)
        for i in args:
            self.connect_node(node[0], i)

    def add_node(self, coords, name, args):
        node = (name, coords)
        self.graph[name] = Button(self.screen, name, coords)
        for i in args:
            if i in self.graph: self.connect_node(node[0], i)

    def connect_node(self, node1, node2):
        try:
            n1 = self.graph[node1]
            n2 = self.graph[node2]
            weight = dist(n1.coords, n2.coords)
            self.pathfinder.add_edge(n1.name, n2.name, weight)
        except KeyError:
            print("KeyError: Restart Data Input for the Node")
            node2 = ask()[1]

    def remove_node(self, node):
        try:
            if node.name in self.graph:
                self.pathfinder.remove_edge(node.name)
                del self.graph[node.name]
        except AttributeError:
            pass

    def select_node(self):
        for i in self.graph:
            if self.graph[i].mouse_touched():
                return self.graph[i]

    def draw_connection(self, node1, node2):
        n1 = self.graph[node1]
        n2 = self.graph[node2]
        pygame.draw.line(self.screen, (255, 165, 0), n1.coords, n2.coords, 3)

    def pathFind(self):
        self.shortest_path = self.pathfinder.shortest_path(self.selected_nodes[0], self.selected_nodes[1])

    def display_path(self):
        if len(self.selected_nodes) == 2:
            for i in range(len(self.shortest_path) - 1):
                self.draw_connection(self.shortest_path[i], self.shortest_path[i + 1])

    def draw_all_connections(self):
        ignoreList = []
        for i in self.pathfinder.graph:
            for j in self.pathfinder.graph[i]:
                if j not in ignoreList:
                    self.draw_connection(i, j)
            ignoreList.append(i)

    def strobe_light_run(self):
        colors = [0, 0, 0]
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.screen.fill((colors[0], colors[1], colors[2]))
            colors[0] = randint(colors[0] - 16, colors[0] + 16)
            colors[1] = randint(colors[1] - 16, colors[1] + 16)
            colors[2] = randint(colors[2] - 16, colors[2] + 16)
            for i in range(3):
                if colors[i] > 255:
                    colors[i] = 255
                elif colors[i] < 0:
                    colors[i] = 0
            print("a = {}; b = {}, c = {}".format(colors[0], colors[1], colors[2]))
            pygame.display.update()
            self.clock.tick(60)

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_key_press > self.key_cooldown:
            self.can_press = True


x = Display()
x.run()
