from mesa import Agent

class Robot(Agent):
    def __init__(self, unique_id, model, pos, init_stack):
        super().__init__(unique_id, model)
        self.pos = pos
        self.next_pos = pos
        self.caja = 0 # 0 = no caja, 1 = caja
        self.stacks = [init_stack]
        self.trigger = False
    
    def step(self):
        cell = self.model.grid.get_cell_list_contents(self.pos)

        if self.trigger:
            neighbors = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)

            op1 = None
            for neighbor in neighbors:
                test = self.model.grid.get_cell_list_contents(neighbor)
                temp = None
                for item in test:
                    if isinstance(item, Cell):
                        temp = item
                        break
                if temp.pos not in self.stacks and not temp.road:
                    temp.num_cajas += 1
                    self.caja = 0
                    self.trigger = False
                    self.stacks.append(temp.pos)
                    break

        if self.caja == 1:
            neighbors = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
            op1 = None
            for neighbor in neighbors:
                if neighbor in self.stacks:
                    op1 = neighbor
        
            if op1 != None:
                # si el stack ya tiene 5 cajas agregar al stack la siguiente celda que no sea calle
                content = self.model.grid.get_cell_list_contents(op1)
                temp = None
                for item in content:
                    if isinstance(item, Cell):
                        temp = item
                        break
                if temp.num_cajas > 4:
                    self.trigger = True
                    
                    cell = self.model.grid.get_cell_list_contents(self.pos)

                    next = None
                    current = None
                    for c in cell:
                        if isinstance(c, Cell):
                            next = (self.pos[0]+c.dir[0], self.pos[1]+c.dir[1])
                            current = c

                    cell = self.model.grid.get_cell_list_contents(next)
                    temp2 = None
                    for c in cell:
                        if isinstance(c, Cell):
                            temp2 = c
                            break
                    
                    if temp2.num_cajas == 0:
                        if not temp2.visited:
                            current.visited = False
                            self.next_pos = next
                            temp2.visited = True
                else:
                    temp.num_cajas += 1
                    self.caja = 0
            else:
                next = None
                for c in cell:
                    if isinstance(c, Cell):
                        next = (self.pos[0]+c.dir[0], self.pos[1]+c.dir[1])
                        break
                
                cell = self.model.grid.get_cell_list_contents(next)
                temp = None
                for c in cell:
                    if isinstance(c, Cell):
                        temp = c
                        break
                
                # agregar evitar el camino extra cuando ya se tiene una caja
                if temp.num_cajas == 0:
                    if not temp.visited:
                        temp.visited = True
                            
                        cell = self.model.grid.get_cell_list_contents(self.pos)
                        for c in cell:
                            if isinstance(c, Cell):
                                c.visited = False
                                break
                                
                        self.next_pos = next
                else:
                    # agregar evitar el camino extra cuando ya se tiene una caja
                    neighbors = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
                    posible = None
                    for neighbor in neighbors:
                        cell = self.model.grid.get_cell_list_contents(neighbor)
                        temp = None
                        for c in cell:
                            if isinstance(c, Cell):
                                temp = c
                                break
                        
                        if not temp.road:
                            posible = temp
                            break
                    
                    if posible != None:
                        posible.num_cajas += 1
                        self.caja = 0
                    else:
                        cell = self.model.grid.get_cell_list_contents(self.pos)
                        temp = None
                        for c in cell:
                            if isinstance(c, Cell):
                                temp = c
                                break
    
                        if self.pos[1] == 2 and temp.dir != (0,-1):
                            cell = self.model.grid.get_cell_list_contents((self.pos[0], 1))
                            for c in cell:
                                if isinstance(c, Cell):
                                    c.num_cajas += 1
                                    self.caja = 0
                                    break
                        
                        elif self.pos[0] == 0:
                            if temp.dir != (1,0):
                                cell = self.model.grid.get_cell_list_contents((self.pos[0]+1, self.pos[1]))
                                for c in cell:
                                    if isinstance(c, Cell):
                                        c.num_cajas += 1
                                        self.caja = 0
                                        break
                            else:
                                cell = self.model.grid.get_cell_list_contents((self.pos[0], self.pos[1]-1))
                                for c in cell:
                                    if isinstance(c, Cell):
                                        c.num_cajas += 1
                                        self.caja = 0
                                        break
                        else:
                            cell = self.model.grid.get_cell_list_contents((self.pos[0]-1, self.pos[1]))
                            for c in cell:
                                if isinstance(c, Cell):
                                    c.num_cajas += 1
                                    self.caja = 0
                                    break
        else:
            # if robot doesn't have a box
            now = None
            for c in cell:
                if isinstance(c, Cell):
                    now = (self.pos[0]+c.dir[0], self.pos[1]+c.dir[1])
                    break
            
            cell = self.model.grid.get_cell_list_contents(now)

            temp = None

            for c in cell:
                if isinstance(c, Cell):
                    temp = c
                    break

            if temp.num_cajas == 0:
                neighbors = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
                for neighbor in neighbors:
                    cell = self.model.grid.get_cell_list_contents(neighbor)
                    temp = None
                    for c in cell:
                        if isinstance(c, Cell):
                            temp = c
                            break
                    
                    if temp.num_cajas > 0 and temp.pos not in self.stacks:
                        self.caja = 1
                        temp.num_cajas -= 1
                        break

                    if self.caja == 1:
                        break
                
                if self.caja == 0:
                    cell = self.model.grid.get_cell_list_contents(now)
                    temp = None
                    for c in cell:
                        if isinstance(c, Cell):
                            temp = c
                            break
                            
                    if not temp.visited:
                        temp.visited = True

                        cell = self.model.grid.get_cell_list_contents(self.pos)
                        for c in cell:
                            if isinstance(c, Cell):
                                c.visited = False
                                break
                            
                        self.next_pos = now
            else:
                if temp not in self.stacks:
                    self.caja = 1
                    temp.num_cajas -= 1
                

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