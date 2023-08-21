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

class Robot(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        self.next_pos = pos
        self.caja = 0 
        self.starting_pos = None
        self.stage = False
        
        cell = self.model.grid.get_cell_list_contents(self.pos)
        for c in cell:
            if isinstance(c, Cell):
                if c.road:
                    self.starting_pos = self.pos
    
    def step(self):
        if not self.stage:
            cell = self.model.grid.get_cell_list_contents(self.pos)
            visiting_cell = self.model.grid.get_cell_list_contents((self.pos[0] + cell[0].dir[0], self.pos[1] + cell[0].dir[1]))
            if self.starting_pos == None:
                for c in cell:
                    if isinstance(c, Cell):
                        if c.road:
                            self.starting_pos = self.pos
                        break
                
            if not visiting_cell[0].visited:
                if visiting_cell[0].num_cajas == 0:
                    self.next_pos = (self.pos[0] + cell[0].dir[0], self.pos[1] + cell[0].dir[1])
                    visiting_cell[0].visited = True
                    cell[0].visited = False
                else:
                    if self.caja == 0:
                        self.caja = 1
                        visiting_cell[0].num_cajas = 0
                        self.next_pos = self.pos
                        cell[0].visited = False
                    else:
                        # get neighbors
                        neighbors = self.model.grid.get_neighborhood(self.pos, False, False)
                        temp = []
                        for (x,y) in neighbors:
                            cell = self.model.grid.get_cell_list_contents((x,y))
                            for c in cell:
                                if isinstance(c, Cell):
                                    if not c.road:
                                        temp.append((x,y))
                        
                        if len(temp) > 0:
                            c = self.model.grid.get_cell_list_contents(temp[0])
                            c[0].num_cajas += 1
                            self.caja = 0
                        else:
                            cell = self.model.grid.get_cell_list_contents((self.pos[0], self.pos[1]-1))
                            cell[0].num_cajas += 1
                            self.caja = 0 
        else:
            pass
                        

    def advance(self):
        if (self.pos != self.next_pos):
            self.model.grid.move_agent(self, self.next_pos)
            self.pos = self.next_pos

class Cell(Agent):
    def __init__(self, unique_id, model, num_cajas, pos):
        super().__init__(unique_id, model)
        self.tipo = 'Celda'
        self.num_cajas = num_cajas
        self.pos = pos
        self.visited = False
        self.road = False


        if (self.pos[1] == 0):
            self.dir = (0,1)
        elif (self.pos[1] == 1):
            self.road = True
            if (self.pos[0] == 0):
                self.dir = (0,1)
            else:
                self.dir = (-1,0)
        else:
            if (self.pos[0] <= int(self.model.width/2)):
                self.dir = (1,0)
            else:
                self.dir = (-1,0)
        
class Room(Model):
    def __init__ (self, width, height, num_cajas):
        self.num_cajas = num_cajas
        self.grid = MultiGrid(width, height, False)
        self.schedule = SimultaneousActivation(self)
        self.width = width
        self.height = height

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
        for i in range(1, 6):
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
                    robot = Robot(i+(self.width*self.height)+20, self, (x, y))
                    self.grid.place_agent(robot, (x, y))
                    self.schedule.add(robot)
                    break

        self.datacollector = DataCollector(
            model_reporters={"Grid": get_grid})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

if __name__ == "__main__":
    #w = int(input("Ingrese el ancho de la habitación: "))
    #h = int(input("Ingrese el alto de la habitación: "))
    #k = int(input("Ingrese el número de cajas: "))
    #t = float(input("Ingrese el tiempo limite: "))

    w = 20
    h = 20
    k = 200
    t = 0.5

    model = Room(w, h, k)
    start_time = time.time()

    while ((time.time() - start_time) < t):
        model.step()

    execution_time = str(datetime.timedelta(seconds=(time.time() - start_time)))
    print("Tiempo de ejecución: " + execution_time)

    all_grid = model.datacollector.get_model_vars_dataframe()

    cmap = matplotlib.colors.ListedColormap([(1, 1, 1),(0.8, 0.8, 0.8), (0.6,0.6,0.6), (0.4, 0.4, 0.4), (0.2, 0.2, 0.2), (0,0,0),(0.094, 0.18, 0.9),(0.094, 0.18, 0.5)])

    fig, axs = plt.subplots(figsize=(7,7))
    axs.set_xticks([])
    axs.set_yticks([])
    patch = plt.imshow(all_grid.iloc[0][0], cmap=cmap)

    def animate(i):
        patch.set_data(all_grid.iloc[i][0])

    anim = animation.FuncAnimation(fig, animate, frames=len(all_grid))
    #anim = animation.FuncAnimation(fig, animate, frames=200)

    writergif = animation.PillowWriter(fps=10)
    anim.save('animation.gif', writer=writergif)