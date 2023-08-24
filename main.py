from mesa import Agent, Model
from mesa.model import Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

# mathplotlib lo usamos para graficar/visualizar como evoluciona el autómata celular.
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
plt.rcParams["animation.html"] = "jshtml"
matplotlib.rcParams['animation.embed_limit'] = 2**128

import numpy as np
import pandas as pd

import time
import datetime
import random

from agents import Cell, Robot

'''
def get_grid(model):
    grid = np.zeros((model.grid.width, model.grid.height))
    for cell in model.grid.coord_iter():
      cell_content, (x, y) = cell
      for obj in cell_content:
        if isinstance(obj, Cell):
            grid[x][y] = obj.num_cajas
        elif isinstance(obj, Robot):
            if obj.caja == 0:
                grid[x][y] = 7
            else:
                grid[x][y] = 6
    return grid
'''

def get_grid(model):
    grid = np.zeros((model.grid.width, model.grid.height))
    for cell in model.grid.coord_iter():
      cell_content, (x, y) = cell
      for obj in cell_content:
        if isinstance(obj, Cell):
            if obj.road and obj.num_cajas==0:
                grid[x][y] = 8
            else:
                grid[x][y] = obj.num_cajas
                
                
        elif isinstance(obj, Robot):
            if obj.caja == 0:
                grid[x][y] = 7
            else:
                grid[x][y] = 6
    return grid

class Room(Model):
    def __init__ (self, width, height, num_cajas):
        self.num_cajas = num_cajas
        self.grid = MultiGrid(width, height, False)
        self.schedule = SimultaneousActivation(self)
        self.width = width
        self.height = height
        self.stacks = []

        # Create cells
        for x in range(width):
            for y in range(height):
                cell = Cell((x, y), self, 0, (x, y))
                self.grid.place_agent(cell, (x, y))
                self.schedule.add(cell)

        current = (0,2)
        
        if (self.width % 2 == 0):
            if (self.width/2)%2 == 0:
                cell = self.grid.get_cell_list_contents(current)
                cell[0].dir = (1,0)
                cell[0].road = True
                current = (current[0]+1, current[1])
                for i in range(int((self.width-1)/4)):
                    for j in range(2):
                        if j == 0:
                            for i in range(2, self.height):
                                cell = self.grid.get_cell_list_contents(current)
                                for c in cell:
                                    if isinstance(c, Cell):
                                        if i == self.height-1:
                                            c.dir = (1, 0)
                                            current = (current[0]+1, current[1])
                                        else:
                                            c.dir = (0,1)
                                            current = (current[0], current[1]+1)
                                        c.road = True
                                        break
                        elif j == 1:
                            for i in range(self.height-1, 1, -1):
                                cell = self.grid.get_cell_list_contents(current)
                                for c in cell:
                                    if isinstance(c, Cell):
                                        if i == 2:
                                            c.dir = (1, 0)
                                            current = (current[0]+1, current[1])
                                        else:
                                            c.dir = (0,-1)
                                            current = (current[0], current[1]-1)
                                        c.road = True
                                        break
                        else:
                            pass
                    
                    for i in range(2):
                        cell = self.grid.get_cell_list_contents(current)
                        for c in cell:
                            if isinstance(c, Cell):
                                c.dir = (1,0)
                                current = (current[0]+1, current[1])
                                c.road = True
                                break
                
                for i in range(2):
                    if i == 0:
                        for j in range(2, self.height):
                            cell = self.grid.get_cell_list_contents(current)
                            for c in cell:
                                if isinstance(c, Cell):
                                    if j == self.height-1:
                                        c.dir = (1, 0)
                                        current = (current[0]+1, current[1])
                                    else:
                                        c.dir = (0,1)
                                        current = (current[0], current[1]+1)
                                    c.road = True
                                    break
                    elif i == 1:
                        for j in range(self.height-1, 1, -1):
                            cell = self.grid.get_cell_list_contents(current)
                            for c in cell:
                                if isinstance(c, Cell):
                                    if j == 2:
                                        c.dir = (1, 0)
                                        current = (current[0]+1, current[1])
                                    else:
                                        c.dir = (0,-1)
                                        current = (current[0], current[1]-1)
                                    c.road = True
                                    break
                
                cell = self.grid.get_cell_list_contents(current)
                cell[0].dir = (0,-1)
                cell[0].road = True
                current = (current[0], current[1]-1)
            else:
                for i in range(int(self.width/4)):
                    for j in range(2):
                        if j == 0:
                            for i in range(2, self.height):
                                cell = self.grid.get_cell_list_contents(current)
                                for c in cell:
                                    if isinstance(c, Cell):
                                        if i == self.height-1:
                                            c.dir = (1, 0)
                                            current = (current[0]+1, current[1])
                                        else:
                                            c.dir = (0,1)
                                            current = (current[0], current[1]+1)
                                        c.road = True
                                        break
                        elif j == 1:
                            for i in range(self.height-1, 1, -1):
                                cell = self.grid.get_cell_list_contents(current)
                                for c in cell:
                                    if isinstance(c, Cell):
                                        if i == 2:
                                            c.dir = (1, 0)
                                            current = (current[0]+1, current[1])
                                        else:
                                            c.dir = (0,-1)
                                            current = (current[0], current[1]-1)
                                        c.road = True
                                        break
                        else:
                            pass
                    
                    for i in range(2):
                        cell = self.grid.get_cell_list_contents(current)
                        for c in cell:
                            if isinstance(c, Cell):
                                c.dir = (1,0)
                                current = (current[0]+1, current[1])
                                c.road = True
                                break
                
                for i in range(2):
                    if i == 0:
                        for j in range(2, self.height):
                            cell = self.grid.get_cell_list_contents(current)
                            for c in cell:
                                if isinstance(c, Cell):
                                    if j == self.height-1:
                                        c.dir = (1, 0)
                                        current = (current[0]+1, current[1])
                                    else:
                                        c.dir = (0,1)
                                        current = (current[0], current[1]+1)
                                    c.road = True
                                    break
                    elif i == 1:
                        for j in range(self.height-1, 1, -1):
                            cell = self.grid.get_cell_list_contents(current)
                            for c in cell:
                                if isinstance(c, Cell):
                                    c.dir = (0,-1)
                                    current = (current[0], current[1]-1)
                                    c.road = True
                                    break
        else:
            if int(self.width/2)%2 == 0:
                cell = self.grid.get_cell_list_contents(current)
                cell[0].dir = (1,0)
                cell[0].road = True
                current = (current[0]+1, current[1])

                for i in range(int(self.width/4)-1):
                    for j in range(2):
                        if j == 0:
                            for i in range(2, self.height):
                                cell = self.grid.get_cell_list_contents(current)
                                for c in cell:
                                    if isinstance(c, Cell):
                                        if i == self.height-1:
                                            c.dir = (1, 0)
                                            current = (current[0]+1, current[1])
                                        else:
                                            c.dir = (0,1)
                                            current = (current[0], current[1]+1)
                                        c.road = True
                                        break
                        elif j == 1:
                            for i in range(self.height-1, 1, -1):
                                cell = self.grid.get_cell_list_contents(current)
                                for c in cell:
                                    if isinstance(c, Cell):
                                        if i == 2:
                                            c.dir = (1, 0)
                                            current = (current[0]+1, current[1])
                                        else:
                                            c.dir = (0,-1)
                                            current = (current[0], current[1]-1)
                                        c.road = True
                                        break
                        else:
                            pass
                    
                    for i in range(2):
                        cell = self.grid.get_cell_list_contents(current)
                        for c in cell:
                            if isinstance(c, Cell):
                                c.dir = (1,0)
                                current = (current[0]+1, current[1])
                                c.road = True
                                break
                
                for i in range(2, self.height):
                    cell = self.grid.get_cell_list_contents(current)
                    for c in cell:
                        if isinstance(c, Cell):
                            if i == self.height-1:
                                c.dir = (1, 0)
                                current = (current[0]+1, current[1])
                            else:
                                c.dir = (0,1)
                                current = (current[0], current[1]+1)
                            c.road = True
                            break
                
                cell = self.grid.get_cell_list_contents(current)
                cell[0].dir = (1,0)
                cell[0].road = True
                current = (current[0]+1, current[1])

                for i in range(self.height-1, 1, -1):
                    cell = self.grid.get_cell_list_contents(current)
                    for c in cell:
                        if isinstance(c, Cell):
                            if i == 2:
                                c.dir = (1, 0)
                                current = (current[0]+1, current[1])
                            else:
                                c.dir = (0,-1)
                                current = (current[0], current[1]-1)
                            c.road = True
                            break
                
                cell = self.grid.get_cell_list_contents(current)
                cell[0].dir = (0,-1)
                cell[0].road = True
                
                cell = self.grid.get_cell_list_contents((current[0]-2, current[1]))
                cell[0].dir = (1,0)
                cell[0].road = True
            else:
                for i in range(int(self.width/4)):
                    for j in range(2):
                        if j == 0:
                            for i in range(2, self.height):
                                cell = self.grid.get_cell_list_contents(current)
                                for c in cell:
                                    if isinstance(c, Cell):
                                        if i == self.height-1:
                                            c.dir = (1, 0)
                                            current = (current[0]+1, current[1])
                                        else:
                                            c.dir = (0,1)
                                            current = (current[0], current[1]+1)
                                        c.road = True
                                        break
                        elif j == 1:
                            for i in range(self.height-1, 1, -1):
                                cell = self.grid.get_cell_list_contents(current)
                                for c in cell:
                                    if isinstance(c, Cell):
                                        if i == 2:
                                            c.dir = (1, 0)
                                            current = (current[0]+1, current[1])
                                        else:
                                            c.dir = (0,-1)
                                            current = (current[0], current[1]-1)
                                        c.road = True
                                        break
                        else:
                            pass
                    
                    for i in range(2):
                        cell = self.grid.get_cell_list_contents(current)
                        for c in cell:
                            if isinstance(c, Cell):
                                c.dir = (1,0)
                                current = (current[0]+1, current[1])
                                c.road = True
                                break
                    
                for i in range(2):
                    if i == 0:
                        for j in range(2, self.height):
                            cell = self.grid.get_cell_list_contents(current)
                            for c in cell:
                                if isinstance(c, Cell):
                                    if j == self.height-1:
                                        c.dir = (1, 0)
                                        current = (current[0]+1, current[1])
                                    else:
                                        c.dir = (0,1)
                                        current = (current[0], current[1]+1)
                                    c.road = True
                                    break
                    elif i == 1:
                        for j in range(self.height-1, 1, -1):
                            cell = self.grid.get_cell_list_contents(current)
                            for c in cell:
                                if isinstance(c, Cell):
                                    if j == 2:
                                        c.dir = (1, 0)
                                        current = (current[0]+1, current[1])
                                    else:
                                        c.dir = (0,-1)
                                        current = (current[0], current[1]-1)
                                    c.road = True
                                    break
                
                cell = self.grid.get_cell_list_contents(current)
                cell[0].dir = (0,-1)
                cell[0].road = True
                current = (current[0], current[1]-1)

        
        # Create cajas
        for i in range(num_cajas):
            while True:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                cell = self.grid.get_cell_list_contents((x, y))
                temp = None
                for c in cell:
                    if not c.num_cajas:
                        temp = c
                        break
                
                if temp != None:
                    temp.num_cajas = 1
                    break
        
        
        # Create robot
        for i in range(1, 21):
            while True:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                cell = self.grid.get_cell_list_contents((x, y))
                temp = None
                if len(cell) == 1:
                    for c in cell:
                        if not c.num_cajas:
                            temp = c
                            break
                
                if temp != None:
                    temp.visited = True
                    robot = Robot(i+(self.width*self.height)+20, self, (x, y), (self.width-1, 0))
                    self.grid.place_agent(robot, (x, y))
                    self.schedule.add(robot)
                    break

        # initialize datacollector
        self.datacollector = DataCollector(
            model_reporters={"Grid": get_grid})

    def step(self):
        # Takes a step and collect data.
        self.datacollector.collect(self)
        self.schedule.step()

if __name__ == "__main__":
    #w = int(input("Ingrese el ancho de la habitación: "))
    #h = int(input("Ingrese el alto de la habitación: "))
    #k = int(input("Ingrese el número de cajas: "))
    #t = float(input("Ingrese el tiempo limite: "))

    w = 17
    h = 17
    k = int((w*h)*.7)
    t = 2

    model = Room(w, h, k)
    start_time = time.time()

    while ((time.time() - start_time) < t):
        model.step()

    execution_time = str(datetime.timedelta(seconds=(time.time() - start_time)))
    print("Tiempo de ejecución: " + execution_time)

    all_grid = model.datacollector.get_model_vars_dataframe()

    cmap = matplotlib.colors.ListedColormap([(1, 1, 1),(0.88, 0.88, 0.88), (0.76,0.76,0.76), (0.64, 0.64, 0.64), (0.52, 0.52, 0.52), (0.4, 0.4, 0.4),(0.094, 0.18, 0.5), (0.094, 0.18, 0.9), (0,0,0)])
    #cmap = matplotlib.colors.ListedColormap([(1,1,1),(0.8,0.8,0.8),(0.6,0.6,0.6),(0.4,0.4,0.4),(0.2,0.2,0.2),(0,0,0),(0.094, 0.18, 0.5), (0.094, 0.18, 0.9)])

    fig, axs = plt.subplots(figsize=(7,7))
    axs.set_xticks([])
    axs.set_yticks([])
    patch = plt.imshow(all_grid.iloc[0][0], cmap=cmap)

    def animate(i):
        patch.set_data(all_grid.iloc[i][0])

    anim = animation.FuncAnimation(fig, animate, frames=len(all_grid))
    #anim = animation.FuncAnimation(fig, animate, frames=500)

    writergif = animation.PillowWriter(fps=20)
    anim.save('animation.gif', writer=writergif)