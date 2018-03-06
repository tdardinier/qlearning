import random
        
def minimax(agent_id, my_agent_id, M, depth):
    """
    The tree of possibilities is explored until the depth equals 0
    """
    if M.win(my_agent_id) or M.lose(my_agent_id):
        return M.score(my_agent_id), -1
    possibilities = M.possibilities(agent_id)
    if my_agent_id==agent_id:
        if not M.agents[my_agent_id].alive or len(possibilities)==0:
            return (-M.gridsize**2, -1)
        if depth==0:
            return (M.agents[my_agent_id].size-M.evaluateDistClosestCandy(my_agent_id), -1)
        maxv=float('-inf')
        for move in possibilities:
            M.update(agent_id, move)
            curr=minimax((my_agent_id+1)%M.nagents, my_agent_id, M, depth-1)
            if curr[0]>maxv:
                maxv=curr[0]
                maxarg=[move]
            elif curr[0]==maxv:
                maxarg.append(move)
            M.revertLastUpdate()
        return (maxv, random.choice(maxarg))
    else:
        if not M.agents[agent_id].alive:
            return minimax((agent_id+1)%M.nagents, my_agent_id, M, depth)
        if len(possibilities)==0:
            M.update(agent_id, -1)
            (value, move)=minimax((agent_id+1)%M.nagents, my_agent_id, M, depth)
            M.revertLastUpdate()
            return (value, move)
        if depth==0:
            return (M.agents[my_agent_id].size-M.evaluateDistClosestCandy(my_agent_id), -1)
        minv=float('inf')
        minarg=-1
        for move in possibilities:
            M.update(agent_id, move)
            curr=minimax((agent_id+1)%M.nagents, my_agent_id, M, depth)
            if minv>curr[0]:
                minv=curr[0]
                minarg=[move]
            elif minv==curr[0]:
                minarg.append(move)
            M.revertLastUpdate()
        return (minv, random.choice(minarg))
            
            
        
        