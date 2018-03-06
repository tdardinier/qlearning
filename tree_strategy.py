
        
def minimax(agent_id, my_agent_id, M, depth):
    """
    The tree of possibilities is explored until the depth equals 0
    """
#    if M.win(my_agent_id) or M.lose(my_agent_id):
#        return M.score(my_agent_id), -1
    if my_agent_id==agent_id:
        if len(M.possibilities(my_agent_id))==0:
            return (-M.gridsize**2, -1)
        if depth==0:
            return (M.agents[my_agent_id].size-M.evaluateDistClosestCandy(my_agent_id), -1)
        maxv=float('-inf')
        for move in M.possibilities(my_agent_id):
            M.update(agent_id, move)
            curr=minimax((my_agent_id+1)%M.nagents, my_agent_id, M, depth-1)
            if curr[0]>maxv:
                maxv=curr[0]
                maxarg=move
            M.revertLastUpdate()
        return (maxv, maxarg)
    else:
        if len(M.possibilities(agent_id))==0:
            M.update(agent_id, -1)
            (value, move)=minimax((agent_id+1)%M.nagents, my_agent_id, M)
            M.revertLastUpdate()
        if depth==0:
            return (M.agents[my_agent_id].size-M.evaluateDistClosestCandy(my_agent_id), -1)
        minv=float('inf')
        minarg=-1
        for move in M.possibilities(agent_id):
            M.update(agent_id, move)
            curr=minimax((agent_id+1)%M.nagents, my_agent_id, M, depth)
            if minv>curr[0]:
                minv=curr[0]
                minarg=move
            M.revertLastUpdate()
        return (minv, minarg)
            
            
        
        