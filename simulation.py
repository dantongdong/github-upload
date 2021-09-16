import pandas as pd
from Planner import Planner
col_names = ["S", "iteration", "R_e", "I_max"]
simulation_df = pd.DataFrame(columns=col_names)
for s in [0.25, 0.5, 0.75]:
    for i in range(100):
        print("running s=" + str(s) + ", iteration=" + str(i))
        planner = Planner(400, 400, 8000, 0.02, s, 0.85, 0.45, 20)
        simulation_df.loc[len(simulation_df)] = planner.run_result()
    simulation_df.to_csv(str(s*100)+'_0_100'+'_simulation.csv')
    for i in range(100, 200):
        print("running s=" + str(s) + ", iteration=" + str(i))
        planner = Planner(400, 400, 8000, 0.02, s, 0.85, 0.45, 20)
        simulation_df.loc[len(simulation_df)] = planner.run_result()
    simulation_df.to_csv(str(s*100)+'_100_200'+'_simulation.csv')
    for i in range(200, 300):
        print("running s=" + str(s) + ", iteration=" + str(i))
        planner = Planner(400, 400, 8000, 0.02, s, 0.85, 0.45, 20)
        simulation_df.loc[len(simulation_df)] = planner.run_result()
    simulation_df.to_csv(str(s*100)+'_200_300'+'_simulation.csv')
    for i in range(300,400):
        print("running s=" + str(s) + ", iteration=" + str(i))
        planner = Planner(400, 400, 8000, 0.02, s, 0.85, 0.45, 20)
        simulation_df.loc[len(simulation_df)] = planner.run_result()
    simulation_df.to_csv(str(s*100)+'_300_400'+'_simulation.csv')
    for i in range(400, 500):
        print("running s=" + str(s) + ", iteration=" + str(i))
        planner = Planner(400, 400, 8000, 0.02, s, 0.85, 0.45, 20)
        simulation_df.loc[len(simulation_df)] = planner.run_result()
    simulation_df.to_csv(str(s*100)+'_400_500'+'_simulation.csv')