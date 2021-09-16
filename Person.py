import random


class Person:
    """ Initialze a person with unique id and initial position"""

    def __init__(self, id, pos_x, pos_y,
                 death_rate, recover_period,
                 mobile=True, infection=False):
        # unique identifier
        self.id = id

        # defined probability
        self.death_rate = death_rate
        self.recover_period = recover_period

        # position in matrix
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.mobile = mobile

        # default direction
        self.dx = 0
        self.dy = 0

        # disease state
        self.infection_period = 0
        self.infection = infection
        self.infection_people = 0
        self.infection_day = 0

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return self.id == other.id

    """ 
    move to a new position with dx, dy increment
    :param dx can be +1, -1, or 0
    :param dy can be +1, -1, or 0
    """

    def set_direction(self, dx, dy):
        if self.mobile:
            self.dx = dx
            self.dy = dy

    """ 
    calculate its next step position
    :return new x, new y after moving
    """

    def calculate_move(self):
        return self.pos_x + self.dx, self.pos_y + self.dy

    """move the person to new position and apply state"""
    def move(self, stay=False):
        # if infected, increment its infection_period by 1
        if self.infection:
            self.infection_period += 1
            # its dead, flag removal
            if self.fate():
                self.pos_x = -1
                self.pos_y = -1
                return -10, -10
        if not stay:
            self.pos_x, self.pos_y = self.calculate_move()
        return self.pos_x, self.pos_y

    """
    try to infect this person according to probability
    :return True if successfully infected, else False
    """

    def infect(self, iteration):
        self.infection = True
        self.infection_day = iteration
        return True

    """
    call this method if it infected other
    """

    def guilt(self):
        self.infection_people += 1


    """
    determine the fate of individual
    :return True if dead, False otherwise
    """

    def fate(self):
        # not your time yet, sit tight!
        if self.infection_period < self.recover_period:
            return False
        death = random.random() < self.death_rate
        # ya dead
        if death:
            return True
        # ya recovered
        else:
            self.infection = False
            self.infection_period = 0
            return False
