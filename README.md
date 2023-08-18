# Smart Warehouse

> Alejandro Melendez Torres - A00832494

## Description

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; This project intends to develop a program where 5 agents (that can be increased) search and organize a room, the room needs to be scalable. For the program to start the user needs to input the width and height of the room, n amount of boxes and the time limit. All the boxes need to be stacked in stacks with a max number of 5 boxes, once the simulation is over we can create a visual representation using a graph.

### Libraries
> Mesa\
> Matplotlib

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Install the libraries using pip `pip install mesa`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; While analyzing the problem, I realized that there are three main scenarios for navigating the grid. There are two styles when the grid's height is even, and a single style when it's odd. Below, you can see the representation of the aforementioned styles.

<img alt="Caso 1" src="https://i.imgur.com/G2UEDUh.png">

<img alt="Caso 2" src="https://i.imgur.com/bpsknmS.png">

<img alt="Caso 3" src="https://i.imgur.com/FVLTzor.png">



### Agents

- Cell

          It represents all the cells in the grid, its has multiple attributes. This agents
          contains the boxes and gives directions to the Robots.

- Robot

          The robots are able to pick up the boxes and place them in a stack, at the
          same it this agent is able to move in the grid.
