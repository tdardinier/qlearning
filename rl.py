MOVES = [
    (1, 0),
    (0, -1),
    (-1, 0),
    (0, 1)
]

def convert_input(agent_id, M):
    head = M.agents[agent_id].head()
    x = head[0]
    y = head[1]

    walls = [0.0, 0.0, 0.0, 0.0]
    snakes = [0.0, 0.0, 0.0, 0.0]
    candies = [0.0, 0.0, 0.0, 0.0]

    for i in range(len(MOVES)):

        (xx, yy) = MOVES[i]

        # Walls
        dist_wall = None
        if xx == 1:
            dist_wall = M.gridsize - x
        elif xx == -1:
            dist_wall = x + 1
        elif yy == 1:
            dist_wall = M.gridsize - y
        elif yy == -1:
            dist_wall = y + 1
        else:
            print("ERROR: shouldn't happen")
        walls[i] = 1.0 / dist_wall

        # Candies
        dist_candy = M.gridsize
        for (a, b) in M.candies:
            if xx == 1:
                if y == b and x < a:
                    dist_candy = min(dist_candy, a - x)
            elif xx == -1:
                if y == b and x > a:
                    dist_candy = min(dist_candy, x - a)
            elif yy == 1:
                if x == a and y < b:
                    dist_candy = min(dist_candy, b - y)
            elif yy == -1:
                if x == a and y > b:
                    dist_candy = min(dist_candy, y - b)
            else:
                print("ERROR: shouldn't happen")
        if dist_candy  < M.grid:
            candies[i] = 1.0 / dist_candy

        # Snakes
        dist_snake = M.gridsize
        for agent in M.agent:
            for (a, b) in agent.pos:
                if xx == 1:
                    if y == b and x < a:
                        dist_snake = min(dist_snake, a - x)
                elif xx == -1:
                    if y == b and x > a:
                        dist_snake = min(dist_snake, x - a)
                elif yy == 1:
                    if x == a and y < b:
                        dist_snake = min(dist_snake, b - y)
                elif yy == -1:
                    if x == a and y > b:
                        dist_snake = min(dist_snake, y - b)
                else:
                    print("ERROR: shouldn't happen")
            if dist_snake  < M.grid:
                snakes[i] = 1.0 / dist_snake

        return walls + candies + snakes
