import numpy as np

def randPair(s,e):
    return np.random.randint(s,e), np.random.randint(s,e)


#finds an array in the "depth" dimension of the grid
def findLoc(state, obj):
    if(obj == (np.array([0,0,1,0]))).all():
        wall_list = []
        for i in range(0,4):
            for j in range(0,4):
                if (state[i,j] == obj).all():
                    wall_list.append((i,j))
        return wall_list
    else:
        for i in range(0,4):
            for j in range(0,4):
                if (state[i,j] == obj).all():
                    return i,j
    

#Initialize stationary grid, all items are placed deterministically
def initGrid():
    

    state = np.zeros((4,4,4))
    #place player
    state[0,0] = np.array([0,0,0,1])
    #place initial wall
    #state[2,2] = np.array([0,0,1,0])

    #Add initial wall to list
    #wall_list.append((2,2))

    #place pit
    state[0,1] = np.array([0,1,0,0])

    #place goal
    state[3,3] = np.array([1,0,0,0])

    return state

#Initialize player in random location, but keep wall, goal and pit stationary
def initGridPlayer():
    state = np.zeros((4,4,4))
    #place player
    state[randPair(0,4)] = np.array([0,0,0,1])
    #place wall
    state[2,2] = np.array([0,0,1,0])
    #place pit
    state[1,1] = np.array([0,1,0,0])
    #place goal
    state[1,2] = np.array([1,0,0,0])


    a = findLoc(state, np.array([0,0,0,1])) #find grid position of player (agent)
    w = findLoc(state, np.array([0,0,1,0])) #find wall
    g = findLoc(state, np.array([1,0,0,0])) #find goal
    p = findLoc(state, np.array([0,1,0,0])) #find pit
    if (not a or not w or not g or not p):
        #print('Invalid grid. Rebuilding..')
        return initGridPlayer()

    return state

#Initialize grid so that goal, pit, wall, player are all randomly placed
def initGridRand():
    state = np.zeros((4,4,4))
    #place player
    state[randPair(0,4)] = np.array([0,0,0,1])
    #place wall
    state[randPair(0,4)] = np.array([0,0,1,0])
    #place pit
    state[randPair(0,4)] = np.array([0,1,0,0])
    #place goal
    state[randPair(0,4)] = np.array([1,0,0,0])

    a = findLoc(state, np.array([0,0,0,1]))
    w = findLoc(state, np.array([0,0,1,0]))
    g = findLoc(state, np.array([1,0,0,0]))
    p = findLoc(state, np.array([0,1,0,0]))
    #If any of the "objects" are superimposed, just call the function again to re-place
    if (not a or not w or not g or not p):
        #print('Invalid grid. Rebuilding..')
        return initGridRand()

    return state

def makeMove(state, action):
    #need to locate player in grid
    #need to determine what object (if any) is in the new grid spot the player is moving to

    player_loc = findLoc(state, np.array([0,0,0,1]))
    wall = findLoc(state, np.array([0,0,1,0]))
    goal = findLoc(state, np.array([1,0,0,0]))
    pit = findLoc(state, np.array([0,1,0,0]))
    state = np.zeros((4,4,4))

    actions = [[-1,0],[1,0],[0,-1],[0,1]]
    #e.g. up => (player row - 1, player column + 0)
    #global same_position

    new_loc = (player_loc[0] + actions[action][0], player_loc[1] + actions[action][1])
    if (new_loc not in wall):
        if ((np.array(new_loc) <= (3,3)).all() and (np.array(new_loc) >= (0,0)).all()):
            state[new_loc][3] = 1
            state[player_loc][2] = 1
           

    if (not findLoc(state, np.array([0,0,0,1]))):
        state[player_loc] = np.array([0,0,0,1])

        
    #re-place pit
    state[pit][1] = 1
    #re-place walls
    for i in range(0, len(wall)):
        state[wall[i]][2] = 1
    #re-place goal
    state[goal][0] = 1

  

    return state

def getLoc(state, level):
    for i in range(0,4):
        for j in range(0,4):
            if (state[i,j][level] == 1):
                return i,j

def isBlocked(state):
    stateUp = makeMove(state, 0) #Up
    stateDown = makeMove(state, 1) #Down
    stateLeft = makeMove(state, 2) #Left
    stateRight = makeMove(state, 3) #Right
    if all( [(state == stateUp).all(), (state == stateDown).all(), (state == stateLeft).all(), (state == stateRight).all()] ):
        return True
    else:
        return False

def getReward(state):
    player_loc = getLoc(state, 3)
    pit = getLoc(state, 1)
    goal = getLoc(state, 0)
    wall_list = findLoc(state, np.array([0,0,1,0]))

 
    if (player_loc == goal):
        if(len(wall_list) == 14):
            return 10
        else:
            return 0
    elif (player_loc == pit or isBlocked(state)):
        return -10
    else:
        return 1

def dispGrid(state):
    grid = np.zeros((4,4), dtype='<U2')
    player_loc = findLoc(state, np.array([0,0,0,1]))
    wall = findLoc(state, np.array([0,0,1,0]))
    goal = findLoc(state, np.array([1,0,0,0]))
    pit = findLoc(state, np.array([0,1,0,0]))

   
    for i in range(0,4):
        for j in range(0,4):
            grid[i,j] = '*'


    if player_loc:
        grid[player_loc] = 'P' #player
    
    for i in range(0, len(wall)):
        grid[wall[i]] = 'W' #wall

    if goal:
        grid[goal] = '+' #goal

    if pit:
        grid[pit] = '-' #pit

    return grid





