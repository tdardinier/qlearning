<<<<<<< HEAD
        
def minimax(agent_id, my_agent_id, M, depth, h):
=======

def minimax(agent_id, my_agent_id, M, depth):
>>>>>>> a3589ba4fc3efd8600a74f8a258ed6acd2225e76
    """
    The tree of possibilities is explored until the depth equals 0
    """
                
    if M.win(my_agent_id) or M.lose(my_agent_id):
        return M.score(my_agent_id), -1
    if len(M.possibilities(my_agent_id))==0:
        return -M.gridsize**2, -1
    if len(M.possibilities(agent_id))==0:
        M.update(agent_id, -1)
        (value, move)=minimax((agent_id+1)%M.nagents, my_agent_id, M, depth, h)
        M.reverseLast()
    if depth==h:
        return M.evaluate(my_agent_id), -1

    if agent_id == my_agent_id:
        maxv=float('-inf')
        for move in M.actions(agent_id):
            M.update(agent_id, move)
            curr=minimax((agent_id+1)%M.nagents, my_agent_id, M, depth+1, h)
            if curr>maxv:
                maxv=curr
                maxarg=move
            M.reverseLast()
        return (maxv, maxarg)

    else:
        minv=float('inf')
        minarg=-1
        for move in M.actions(agent_id):
            M.update(agent_id, move)
            curr=minimax((agent_id+1)%M.nagents, my_agent_id, M, depth, h)
            if minv>curr:
                minv=curr
                minarg=move.type
            M.reverseLast()
        return (minv, minarg)
<<<<<<< HEAD
                
=======
>>>>>>> a3589ba4fc3efd8600a74f8a258ed6acd2225e76
