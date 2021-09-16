from Person import Person
import random
import matplotlib.pyplot as plt
import time


class Planner:
    """initialize initial state for each person and populate planner"""

    def __init__(self, m, n, population,
                 initial_infection, S,
                 mobility, death_rate, recover_period):
        # initial planner state
        self.m = m
        self.n = n
        self.population = population
        self.mobility = mobility

        self.id2people = {}
        self.occupied_grid = {}
        self.infected_id = set()
        self.alive = set(range(population))
        self.move_id = set()

        self.iteration = 0
        self.I_max = population * initial_infection
        self.S = S

        # generate random initial state for each person in batch
        random_x = [random.randint(0, m - 1) for i in range(population)]
        random_y = [random.randint(0, n - 1) for j in range(population)]
        random_move_id = set(random.sample(range(0, population), int(population * (1 - S))))
        random_infection_id = set(random.sample(range(0, population), int(population * initial_infection)))

        # populate planner state
        self.infected_id = random_infection_id
        self.move_id = random_move_id
        for id in range(population):
            pos_x, pos_y = random_x[id], random_y[id]
            mobile = id in self.move_id
            infected = id in random_infection_id

            self.occupied_grid[(pos_x, pos_y)] = id
            self.id2people[id] = Person(id, pos_x, pos_y, death_rate, recover_period, mobile, infected)
            # make sure its not stationary
            dx = random.randint(-1, 1)
            dy = random.randint(-1, 1)
            while dx == 0 and dy == 0:
                dx = random.randint(-1, 1)
                dy = random.randint(-1, 1)
            self.id2people[id].set_direction(dx, dy)

    def random_direction(self):
        # make sure its not stationary
        dx = random.randint(-1, 1)
        dy = random.randint(-1, 1)
        while dx == 0 and dy == 0:
            dx = random.randint(-1, 1)
            dy = random.randint(-1, 1)
        return dx, dy

    """check whether it will collide with edge"""

    def collide_edge(self, pos_x, pos_y):
        return pos_x < 0 or pos_x >= self.m or pos_y < 0 or pos_y >= self.n



    """check whether it will collide with another"""

    def collide_person(self, pos_x, pos_y):
        return (pos_x, pos_y) in self.occupied_grid

    def iterate(self):
        iter_move_id = set(random.sample(list(self.move_id), int(len(self.move_id) * self.mobility)))
        # purge move people first
        recovered = []
        dead = []
        dead_pos = []
        poplist = []
        for key in self.occupied_grid.keys():
            value = self.occupied_grid[key]
            if value in iter_move_id:
                poplist.append(key)
            else:
                new_x, new_y = self.id2people[value].move(stay=True)
                if new_x == -10:
                    dead.append(value)
                    dead_pos.append(key)
                if value in self.infected_id and not self.id2people[value].infection:
                    recovered.append(value)

        for key in poplist:
            self.occupied_grid.pop(key)

        newly_infected = []
        # move infected people first
        for id in self.infected_id:
            person = self.id2people[id]
            old_x, old_y = person.pos_x, person.pos_y
            # calculate move
            new_x, new_y = person.calculate_move()
            # check collision with edge
            threshold = 0
            while self.collide_edge(new_x, new_y) and threshold < 10:
                dx, dy = self.random_direction()
                self.id2people[id].set_direction(dx, dy)
                new_x, new_y = person.calculate_move()
                threshold += 1
            if threshold == 10:
                self.id2people[id].set_direction(0, 0)
                new_x, new_y = person.calculate_move()
            # check collision with people
            if self.collide_person(new_x, new_y):
                poor_guy_id = self.occupied_grid.get((new_x, new_y))
                if not self.id2people[poor_guy_id].infection:
                    newly_infected.append(poor_guy_id)
                self.id2people[poor_guy_id].infect(self.iteration)
                person.guilt()
                dx, dy = self.random_direction()
                person.set_direction(dx, dy)
                new_x, new_y = person.move(stay=True)
            # otherwise it will just move
            else:
                new_x, new_y = person.move()
            # if it's dead, wipe its existence everywhere
            if new_x == -10:
                dead.append(id)
                dead_pos.append((old_x, old_y))
            # populate grid
            else:
                self.occupied_grid[(new_x, new_y)] = id
            # if it recovered, remove it from infected
            if not person.infection:
                recovered.append(id)

        # move non-infected people too
        for id in self.move_id - self.infected_id:
            person = self.id2people[id]
            # calculate move
            new_x, new_y = person.calculate_move()
            # check collision with edge
            threshold = 0
            while self.collide_edge(new_x, new_y) and threshold < 10:
                dx, dy = self.random_direction()
                self.id2people[id].set_direction(dx, dy)
                new_x, new_y = person.calculate_move()
                threshold += 1
            if threshold == 10:
                self.id2people[id].set_direction(0, 0)
                new_x, new_y = person.calculate_move()
            # check collision with people
            if self.collide_person(new_x, new_y):
                other_id = self.occupied_grid[(new_x, new_y)]
                # if the other guy is infected
                if other_id in self.infected_id:
                    self.id2people[other_id].guilt()
                    person.infect(self.iteration)
                    self.infected_id.add(id)
                    dx, dy = self.random_direction()
                    person.set_direction(dx, dy)
                    new_x, new_y = person.move(stay=True)
            # otherwise it will just move
            else:
                new_x, new_y = person.move()
            # populate grid
            self.occupied_grid[(new_x, new_y)] = id

        for pos in dead_pos:
            if pos in self.occupied_grid:
                self.occupied_grid.pop(pos)
        for new_infect in set(newly_infected):
            self.infected_id.add(new_infect)
        for recovered_id in set(recovered):
            self.infected_id.remove(recovered_id)
        for dead_id in set(dead):
            if dead_id in self.alive:
                self.alive.remove(dead_id)
            if dead_id in self.infected_id:
                self.infected_id.remove(dead_id)
            if dead_id in self.move_id:
                self.move_id.remove(dead_id)
        self.iteration += 1

    def visual(self):
        figure, ax = plt.subplots(figsize=(10, 8))
        # setting title
        plt.title("COVID-19")
        while self.iteration < 2000 and len(self.infected_id) > 0 and len(self.alive) > 0:
            ax.clear()
            self.iterate()
            self.I_max = max(self.I_max, len(self.infected_id))
            x_non_infected = []
            y_non_infected = []
            x_infected = []
            y_infected = []
            for id, person in self.id2people.items():
                if person.pos_x != -1:
                    if person.infection:
                        x_infected.append(person.pos_x)
                        y_infected.append(person.pos_y)
                    else:
                        x_non_infected.append(person.pos_x)
                        y_non_infected.append(person.pos_y)
            ax.set_title('T='+str(self.iteration))
            non_infected = ax.scatter(x_non_infected, y_non_infected, marker="s", c="b", s=1)
            if len(x_infected) != 0:
                infected = ax.scatter(x_infected, y_infected, marker="s", c="r", s=5)
            plt.pause(0.05)


    def calculate_Re(self, end_iteration):
        infected_people_last100 = []
        for id in self.id2people:
            if self.id2people[id].infection_day > end_iteration - 121:
                infected_people_last100.append(self.id2people[id].infection_people)
        return sum(infected_people_last100)/len(infected_people_last100)


    def run(self):
        print("iteration: " + str(self.iteration) + " | Alive: " + str(len(self.alive)) + " | Infected: " + str(
            len(self.infected_id)))
        while self.iteration < 2000 and len(self.infected_id) > 0 and len(self.alive) > 0 :
            self.iterate()
            self.I_max = max(self.I_max, len(self.infected_id))
            print("iteration: " + str(self.iteration) + " | Alive: " + str(len(self.alive)) + " | Infected: " + str(len(self.infected_id)))
        print("=======result=======")
        print("iteration = " + str(self.iteration))
        print("R_e = " + str(self.calculate_Re(self.iteration)))
        print("I_max = " + str(self.I_max))

    def run_result(self):
        while self.iteration < 2000 and len(self.infected_id) > 0 and len(self.alive) > 0:
            self.iterate()
            self.I_max = max(self.I_max, len(self.infected_id))
        return {"S": self.S,
                "iteration": self.iteration,
                "R_e": self.calculate_Re(self.iteration),
                "I_max": self.I_max}




#m, n, population, initial_infection, S, mobility, death_rate, recover_period
planner = Planner(400, 400, 8000, 0.02, 0, 0.85, 0.45, 20)
planner.visual()