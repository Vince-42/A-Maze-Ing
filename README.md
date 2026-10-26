# A-Maze-Ing
Amazing project @42 Berlin

a_maze_ing.py 
-> start()  
- initiate the program
- parse the command argument 
- inititiate the data retrieval from config.txt via config.py
- validate the data within the config.txt file

'''
            if obj.coordinate[1] == 0 and (obj.coordinate[0] != 0 or obj.coordinate[0] != self.width + 1):
                #symbol = "GG" 
                #symbol = CELL_SHAPES[(0, 0, 0, 1)]
                obj.stateN = 0
                obj.stateE = 0
                obj.stateS = 0
                obj.stateW = 1
                obj.visit = True
                symbol = " ┃ "
            elif obj.coordinate[0] == self.width and ( obj.coordinate[1] != 0 or obj.coordinate[1] != self.height):
                #symbol = "BB" 
                #symbol = CELL_SHAPES[(0, 0, 1, 0)]
                obj.stateN = 0
                obj.stateE = 0
                obj.stateS = 1
                obj.stateW = 0
                symbol = "━━━"
                obj.visit = True
            elif obj.coordinate[1] == self.height and (obj.coordinate[0] != self.width or obj.coordinate[0] != self.width):
                #symbol = "DD"
                #symbol = CELL_SHAPES[(0, 1, 0, 0)]
                obj.stateN = 0
                obj.stateE = 1
                obj.stateS = 0
                obj.stateW = 0
                symbol = " ┃ "
                obj.visit = True
            elif obj.coordinate[0] == 0 and (obj.coordinate[1] != 0 and obj.coordinate[1] != self.height):
                #symbol = "HH"
                #symbol = CELL_SHAPES[(1, 0, 0, 0)]
                obj.stateN = 1
                obj.stateE = 0
                obj.stateS = 0
                obj.stateW = 0
                symbol = "━━━"
                obj.visit = True
            if obj.coordinate[1] == 0 and obj.coordinate[0] == 0:
                #symbol = "HG" 
                symbol = CELL_SHAPES[(1, 0, 0, 1)]
                obj.visit = True
            elif obj.coordinate[0] == 0 and obj.coordinate[1] == self.height:
                #symbol = "HD"
                symbol = CELL_SHAPES[(1, 1, 0, 0)]
                obj.visit = True
            elif obj.coordinate[0] == self.width and obj.coordinate[1] == 0:
                #symbol = "BG"
                symbol = CELL_SHAPES[(0, 0, 1, 1)]
                obj.visit = True
            elif obj.coordinate[0] == self.width and obj.coordinate[1] == self.height:
                #symbol = "BD"
                symbol = CELL_SHAPES[(0, 1, 1, 0)]
                obj.visit = True


                        for obj in self._all_cells:
            if obj.coordinate[1] == 0:
                print("\n", end="")
            states = (
                    obj.stateN,
                    obj.stateE,
                    obj.stateS,
                    obj.stateW
                )
            symbol = CELL_SHAPES[states]
            if obj.coordinate == self.entry_maze:
                symbol = color.GREEN + symbol + color.RESET
            elif obj.coordinate == self.exit_maze:
                symbol = color.RED + symbol + color.RESET
            print(f"{color.YELLOW + symbol + color.RESET}", end="")
'''
