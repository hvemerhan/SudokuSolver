psudoku = [
#  0  1  2     3  4  5      6  7  8        #
   #  #  #     #  #  #      #  #  #        |
#                                          #
#     0           1            2        
  [0, 8, 0,    6, 0, 5,     0, 0, 9],    # 0
  [0, 0, 7,    0, 0, 4,     0, 1, 0],    # 1   
  [0, 9, 0,    0, 0, 0,     3, 5, 7],    # 2
#     3           4            5
  [9, 3, 0,    7, 0, 8,     1, 4, 0],    # 3
  [0, 7, 4,    0, 1, 0,     0, 0, 5],    # 4
  [6, 0, 0,    0, 3, 0,     8, 0, 2],    # 5
#     6           7            8
  [5, 0, 1,    0, 2, 0,     0, 9, 4],    # 6 -
  [0, 0, 8,    9, 0, 7,     0, 6, 0],    # 7
  [7, 0, 0,    5, 6, 0,     2, 0, 3]     # 8
]

size_of_sudoku = len(psudoku)      # Board size 9 x 9

def printList(ListName):
    line = '---------------------------'
    for row in range(size_of_sudoku):   
        if (row % (size_of_sudoku/3) == 0) and (row != 0):
            print(line)
        
        for element in range(size_of_sudoku):
            if (element % (size_of_sudoku/3) == 0) and (element != 0):
                print(" | ", end = ' ')
            print(ListName[row][element], end = ' ')    # Print every horisontal line one after the other
            
        print("|")  

def check_vertical(x):      # Returns a set with numbers in vertical, removes 0
    vertical_content = set()
    for e in range(size_of_sudoku):
        vertical_content.add(psudoku[e][x])
    vertical_content.remove(0)
    return vertical_content 

def check_horisontal(y):    # Returns a set with numbers in horsisontal, removes 0
    horisontal_content = set()
    for e in range(size_of_sudoku):
        horisontal_content.add(psudoku[y][e])
    horisontal_content.remove(0)
    return horisontal_content

def find_group(x, y):
    if x in         {0, 1, 2}:
        group_x =   {0, 3, 6} 
    
    elif x in       {3, 4, 5}:
        group_x =   {1, 4, 7}
    
    elif x in       {6, 7, 8}:
        group_x =   {2, 5, 8}
    
    if y in         {0, 1, 2}:
        group_y =   {0, 1, 2}
    
    elif y in       {3, 4, 5}:
        group_y =   {3, 4, 5}
    
    elif y in       {6, 7, 8}:
        group_y =   {6, 7, 8}

    Group = group_x.intersection(group_y)
    for groupNumber in Group:
        int(groupNumber)

    return groupNumber  

def check_group(group_number):   # Returns a set with numbers in group, removes 0
    group_content = set() 
    #   Gir startverdi på koordinater med :     X, Y
    """GruppeIn:        0       1       2       3       4       5       6       7       8   """
    inital_groups = ((0, 0), (3, 0),(6, 0), (0, 3), (3, 3), (6, 3), (0, 6), (3, 6), (6, 6))

    x_pos = 0
    y_pos = 0
    for e in range(size_of_sudoku):
        if (x_pos == size_of_sudoku/3): # Stay inside this group
            x_pos = 0
            y_pos += 1
        group_content.add(psudoku[inital_groups[group_number] [1] + y_pos]   [inital_groups[group_number] [0] + x_pos])
        x_pos += 1
    group_content.remove(0)
    return group_content  

def group_exlusiveCoord(list, x_crd, y_crd):
    group_number = find_group(x_crd, y_crd)
    group_content = set() 
    #   Gir startverdi på koordinater med :     X, Y
    """GruppeIn:        0       1       2       3       4       5       6       7       8   """
    inital_groups = ((0, 0), (3, 0),(6, 0), (0, 3), (3, 3), (6, 3), (0, 6), (3, 6), (6, 6))

    x_pos = 0
    y_pos = 0
    for e in range(size_of_sudoku):
        if (x_pos == size_of_sudoku/3): # Stay inside this group
            x_pos = 0
            y_pos += 1
        if (not (x_crd == x_pos and y_crd == y_pos)):
            group_content.update(list[inital_groups[group_number] [1] + y_pos]   [inital_groups[group_number] [0] + x_pos])
            
        x_pos += 1
    return group_content

def is_legal():
    legal_inputs = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    keepGoing = True
    possibilites_all = [
            [set(), set(), set(),     set(), set(), set(),     set(), set(), set()],
            [set(), set(), set(),     set(), set(), set(),     set(), set(), set()],
            [set(), set(), set(),     set(), set(), set(),     set(), set(), set()],

            [set(), set(), set(),     set(), set(), set(),     set(), set(), set()],
            [set(), set(), set(),     set(), set(), set(),     set(), set(), set()],
            [set(), set(), set(),     set(), set(), set(),     set(), set(), set()],

            [set(), set(), set(),     set(), set(), set(),     set(), set(), set()],
            [set(), set(), set(),     set(), set(), set(),     set(), set(), set()],
            [set(), set(), set(),     set(), set(), set(),     set(), set(), set()]
            ]
    once = True
    count = 0

    while (once):
        x = 0
        y = 0
        # Iterates over all ints in psoduko
        for e in range((size_of_sudoku**2)): #First method Naked Single
            if (x == size_of_sudoku):
                x = 0
                y += 1
            if (psudoku[y][x] == 0):                    
                possibilites = legal_inputs.difference(check_horisontal(y), check_vertical(x), check_group(find_group(x, y)))
                possibilites_all[y][x] = possibilites
                
                if (len(possibilites) == 1):
                    for newNumber in possibilites:
                        psudoku[y][x] = newNumber
                        #print(f"Første metode!! {newNumber} At coordinate: {x}, {y}")
    
            else:
                possibilites_all[y][x] = {psudoku[y][x]}
                
            x += 1

        for y_axis in range(size_of_sudoku): # Second method
            for x_axis, original_value in enumerate(possibilites_all[y_axis]):     # Iterates over possibilites List
                
                if (psudoku[y_axis][x_axis] == 0):    # Only check unknown numbers in puzzle 
                    
                    posibil_horisontal  = set()
                    posibil_vertical    = set()
                    posibil_group       = set()

                    posibil_group = group_exlusiveCoord(possibilites_all, x_axis, y_axis) # Embedded

                    for e in range(x_axis - 1, x_axis - size_of_sudoku, -1):    # Combine horisontal
                        posibil_horisontal.update   (possibilites_all[y_axis][e])

                    for e in range(y_axis - 1, y_axis - size_of_sudoku, -1):    # Combine Vertical
                        posibil_vertical.update     (possibilites_all[e][x_axis])
                    
                    
                    
                    horisontal_remaining   = original_value.difference(posibil_horisontal)
                    vertical_remaining      = original_value.difference(posibil_vertical)
                    group_remaining        = original_value.difference(posibil_group)
                    #print(f"Horisontal: {horisontal_remaining}. Vertikal: {vertical_remaining}. Gruppe: {group_remaining}")
                    #print(posibil_horisontal)

                    horisontal_remaining.update(vertical_remaining, group_remaining)     # Combine the two solutions

                    if (len(horisontal_remaining) == 1):
                        for thing in horisontal_remaining: 
                            psudoku[y_axis][x_axis] = thing
                            #print(f"Andre metode!! {thing} At coordinate: {y_axis}, {x_axis}")
                                  
        count += 1
        #print("once; ", count) 
        if count == 100:
            once = False   
        remaining = 0
        for list in psudoku:
            for integer in list:
                if (integer == 0):
                    remaining += 1
        if (remaining == 0):
            keepGoing = False
    printList(psudoku)
    #printList(possibilites_all)


    

#def possible_Group():
"""
legal_inputs = {1, 2, 3, 4, 5, 6, 7, 8, 9}

a = {5, 8}
b = {3, 5, 7, 8}
c = {3, 7, 8}
d = {4, 5, 8}
e = {3, 4, 5, 8}
f = {1}
g = {2}
h = {9}
i = {3, 6, 7}
list_all = [a, b, c, d, e, f, g, h, i]
"""

print("start")
is_legal()
print("slutt")

""" # IDENTITETSMATRISE
psudoku = [
#  0  1  2     3  4  5      6  7  8        #
   #  #  #     #  #  #      #  #  #        |
#                                          #
#     0           1            2        
  [0, 0, 0,    0, 0, 0,     0, 0, 0],    # 0
  [0, 0, 0,    0, 0, 0,     0, 0, 0],    # 1   
  [0, 0, 0,    0, 0, 0,     0, 0, 0],    # 2
#     3           4            5
  [0, 0, 0,    0, 0, 0,     0, 0, 0],    # 3
  [0, 0, 0,    0, 0, 0,     0, 0, 0],    # 4
  [0, 0, 0,    0, 0, 0,     0, 0, 0],    # 5
#     6           7            8
  [0, 0, 0,    0, 0, 0,     0, 0, 0],    # 6 -
  [0, 0, 0,    0, 0, 0,     0, 0, 0],    # 7
  [0, 0, 0,    0, 0, 0,     0, 0, 0]     # 8
]
        KINDERGARTEN
psudoku = [
#  0  1  2     3  4  5      6  7  8        #
   #  #  #     #  #  #      #  #  #        |
#                                          #
#     0           1            2        
  [0, 8, 0,    6, 0, 5,     0, 0, 9],    # 0
  [2, 0, 7,    0, 0, 4,     0, 1, 0],    # 1   
  [0, 9, 0,    0, 0, 0,     3, 5, 7],    # 2
#     3           4            5
  [9, 3, 0,    7, 0, 8,     1, 4, 0],    # 3
  [0, 7, 4,    0, 1, 0,     0, 0, 5],    # 4
  [6, 0, 0,    0, 3, 0,     8, 0, 2],    # 5
#     6           7            8
  [5, 0, 1,    0, 2, 0,     0, 9, 4],    # 6 -
  [0, 0, 8,    9, 0, 7,     0, 6, 0],    # 7
  [7, 0, 0,    5, 6, 0,     2, 0, 3]     # 8
]

    GRADUATE
psudoku = [
#  0  1  2     3  4  5      6  7  8        #
   #  #  #     #  #  #      #  #  #        |
#                                          #
#     0           1            2        
  [0, 0, 0,    0, 0, 6,     4, 0, 0],    # 0
  [0, 0, 1,    0, 0, 0,     6, 7, 0],    # 1   
  [2, 9, 0,    0, 0, 0,     0, 8, 0],    # 2
#     3           4            5
  [7, 0, 0,    2, 6, 0,     0, 0, 0],    # 3
  [0, 0, 4,    0, 0, 5,     0, 0, 0],    # 4
  [0, 2, 5,    0, 0, 8,     0, 0, 0],    # 5
#     6           7            8
  [3, 0, 0,    8, 0, 0,     7, 0, 4],    # 6 -
  [6, 0, 0,    4, 0, 0,     5, 0, 0],    # 7
  [0, 0, 0,    0, 0, 7,     0, 0, 2]     # 8
]
"""