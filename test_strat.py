from snake_env import Map, Render

M = Map(nagents=2, ncandies=3, gridsize=40)
e = Render(M, spacing=20)
e.render()

M.update(0, 1)
e.render()
M.revertLastUpdate()
e.render()
M.update(1,1)
e.render()
M.update(1, 0)
M.update(1, 3)
e.render()
M.revertLastUpdate()
M.possibilities(1)
#s=M.agents[0]

