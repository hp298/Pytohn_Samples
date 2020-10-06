"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the Alien
Invaders game.  Instances of Wave represent a single wave.  Whenever you move to a
new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on screen.
These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer.

# Hermogenes Parente & Jackson Bauer
# December 4th, The year of our lord Two-Thousand and Eighteen
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts on screen.
    It animates the laser bolts, removing any aliens as necessary. It also marches the
    aliens back and forth across the screen until they are all destroyed or they reach
    the defense line (at which point the player loses). When the wave is complete, you
    should create a NEW instance of Wave (in Invaders) if you want to make a new wave of
    aliens.

    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lecture 24 for an example.  This class will be similar to
    than one in how it interacts with the main class Invaders.

    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of Alien or None]
        _bolts:  the laser bolts currently on screen [list of Bolt, possibly empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   the amount of time since the last Alien "step" [number >= 0]

    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Invaders. It is okay if you do, but you MAY NOT ACCESS
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that
    you need to access in Invaders.  Only add the getters and setters that you need for
    Invaders. You can keep everything else hidden.

    You may change any of the attributes above as you see fit. For example, may want to
    keep track of the score.  You also might want some label objects to display the score
    and number of lives. If you make changes, please list the changes with the invariants.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _count:  the amount of steps the aliens have taken [int >= 0]
        _ycount: steps vertically alien takes [0 < int]
        _rate: how many steps until alien shoots [1 <= int <= BOLT_RATE]
        _mute: whether sound is muted or not [bool]
        _waskeydown: whether the key was down in the last frame [bool]
        _speedmult: multiplier for alien speed [0 < float <= 1]
        _score: player score [0 <= int]
    """

    def getShip(self):
        """
        returns _ship
        """
        return self._ship

    def getLives(self):
        """
        returns _lives
        """
        return self._lives

    def setShip(self):
        """
        resets the ship to start postion
        """
        self._ship = self.shiHelper()

    def setSpeedMult(self, speedmult):
        """
        sets the speed multiplier of ALIEN_SPEED

        parameter speedmult: speed multiplier to be used with ALIEN_SPEED
        precondition: 0 < speedmult <= 1 and speedmult is a float or int
        """
        assert type(speedmult) == float or type(speedmult) == int
        assert speedmult <= 1 and speedmult > 0
        self._speedmult = speedmult

    def getScore(self):
        """
        return _score
        """
        return self._score

    def setScore(self, score):
        """
        sets _score to score

        parameter score: score to set _score to
        precondition: score is an integer greater than or equal to 0
        """
        assert type(score) == int
        assert score >= 0
        self._score = score

    def __init__(self):
        """
        initialize the wave
        """
        self._ycount = 0
        self._aliens = self.aliHelper()
        self._ship = self.shiHelper()
        self._dline = GPath( linewidth = 2, points = [0, DEFENSE_LINE,
        GAME_WIDTH, DEFENSE_LINE], linecolor = 'gray')
        self._time = 0
        self._bolts = []
        self._count = 0
        self._rate = random.randint(1, BOLT_RATE)
        self._lives = 3
        self._mute = False
        self._waskeydown = False
        self._speedmult = 1
        self._score = 0

    def aliHelper(self):
        """
        creates the wave of aliens

        sets alien images in twos
        """
        list1 = []
        k = 1
        l = 0
        m = 0
        for i in range(ALIEN_ROWS):
            list2 = []
            if k < 2:
                img = ALIEN_IMAGES[2]
                k = k + 1
            elif l < 2:
                img = ALIEN_IMAGES[1]
                l = l + 1
            elif m < 1:
                img = ALIEN_IMAGES[0]
                m = m + 1
            else:
                img = ALIEN_IMAGES[0]
                m = 0
                l = 0
                k = 0

            for j in range(ALIENS_IN_ROW):
                alien = Alien(x =((j+1)*ALIEN_H_SEP + (ALIEN_WIDTH / 2) +
                (ALIEN_WIDTH * j)), y = (GAME_HEIGHT - ((ALIEN_CEILING) +
                (ALIEN_HEIGHT / 2) + (i * ALIEN_HEIGHT)+ (ALIEN_V_SEP * i))),
                width = ALIEN_WIDTH, height = ALIEN_HEIGHT, source = img)
                list2 = list2 + [alien]
            t = list2[:]
            list1 = list1 + [t]
        return list1

    def shiHelper(self):
        """
        creats the ship
        """
        ship = Ship(x = GAME_WIDTH / 2, bottom = SHIP_BOTTOM, width = SHIP_WIDTH,
        height = SHIP_HEIGHT, source = 'ship.png')
        if ship != None:
            return ship

    def shipMov(self, input):
        """
        moves the ship based on keyboard input

        user uses 'a' and 'd' to move the ship left and right respectively

        parameter input: used to detect user input
        precondition: instance of GInput
        """
        l = 0
        r = 0
        if input.is_key_down('a'):
            l = SHIP_MOVEMENT
        elif input.is_key_down('d'):
            r = SHIP_MOVEMENT

        if self._ship != None:
            if self._ship.left < SHIP_MOVEMENT:
                l = 0
            elif self._ship.right > (GAME_WIDTH - SHIP_MOVEMENT):
                r = 0
            self._ship.x = self._ship.x + r - l

    def aliMove(self):
        """
        makes list of alien edges and calls moveAlien to move Aliens
        """
        listr = []
        listl = []
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    listr = listr + [alien.right]
                    listl = listl + [alien.left]
        self.moveAlien(listr, listl)

    def moveAlien(self, listr, listl):
        """
        Moves aliens sideways and down at screen edge

        parameter listr: a list of the right edges of all the aliens
        precondition: is a list of ints

        parameter listl: a list of the left edges of all the aliens
        precondition: is a list of ints
        """
        if len(listr) != 0:
            if self._ycount % 2 == 0:
                if max(listr) > GAME_WIDTH - ALIEN_H_SEP:
                    for row in self._aliens:
                        for alien in row:
                            if alien != None:
                                alien.y = alien.y - (ALIEN_V_SEP)
                    self._ycount += 1
                else:
                    for row in self._aliens:
                        for alien in row:
                            if alien != None:
                                alien.x = alien.x + (ALIEN_H_WALK)
                                alien.y = alien.y

        if len(listl) != 0:
            if self._ycount % 2 == 1:
                if min(listl) < ALIEN_H_SEP:
                    for row in self._aliens:
                        for alien in row:
                            if alien != None:
                                alien.y = alien.y - (ALIEN_V_SEP)
                    self._ycount +=1
                else:
                    for row in self._aliens:
                        for alien in row:
                            if alien != None:
                                alien.x = alien.x - (ALIEN_H_WALK)
                                alien.y = alien.y

    def boltFire(self, input):
        """
        Checks if user can fire a bolt, creates a bolt if it can and plays sound

        parameter input: used to detect user input
        precondition: instance of GInput
        """
        fire = True
        for k in self._bolts:
            if k.isPlayerBolt():
                fire = False

        if fire:
            if input.is_key_down('spacebar'):
                if self._ship != None:
                    bolt = Bolt(BOLT_SPEED, x = self._ship.x, y = self._ship.y
                    + (SHIP_HEIGHT/2) + (BOLT_HEIGHT / 2), width = BOLT_WIDTH,
                    height = BOLT_HEIGHT, fillcolor = 'blue')
                    self._bolts = self._bolts + [bolt]
                    r = random.randint(0, 2)
                    boltSound = Sound(LASER_SOUNDS[r])
                    if self._mute == False:
                        boltSound.play()

        i = 0
        j = len(self._bolts)
        while i < j:
            boltz = self._bolts[i]
            boltz.y = boltz.y + Bolt.getVelocity(boltz)
            if boltz.bottom >= GAME_HEIGHT:
                self._bolts.pop(i)
                j = len(self._bolts)
            else:
                i += 1

    def botAli(self):
        """
        returns: a 2 element list that represents the row and column of a random
        bottom alien

        finds the bottom alien of every column of aliens and randomly chooses one
        """
        bottom = []
        for k in range(ALIENS_IN_ROW):
            bottom = bottom + [None]
        for l in range(ALIENS_IN_ROW):
            for row in range(ALIEN_ROWS):
                if self._aliens[row][l] != None:
                    if bottom[l] == None:
                        bottom[l] = row
                    elif row > bottom[l]:
                        bottom[l] = row

        r = random.randint(0, ALIENS_IN_ROW - 1)
        work = False
        while work == False:
            if bottom[r] == None:
                r = random.randint(0, ALIENS_IN_ROW - 1)
            else:
                work = True
        lst = [r, bottom[r]]
        return lst

    def aliBolt(self):
        """
        after the count reaches the rate, fires an alien bolt
        """
        if self._count == self._rate:
            list = self.botAli()
            alien = self._aliens[list[1]][list[0]]
            if alien != None:
                bolt = Bolt(-BOLT_SPEED, x = alien.x, y = alien.y -
                (ALIEN_HEIGHT / 2) - (BOLT_HEIGHT / 2), width = BOLT_WIDTH,
                height = BOLT_HEIGHT, fillcolor = 'red')
                self._bolts = self._bolts + [bolt]
                self._count = 0
                self._rate = random.randint(1, BOLT_RATE)

        i = 0
        j = len(self._bolts)
        while i < j:
            boltz = self._bolts[i]
            boltz.y = boltz.y + Bolt.getVelocity(boltz)
            if boltz.top <= 0:
                self._bolts.pop(i)
                j = len(self._bolts)
            else:
                i += 1

    def alidead(self):
        """
        checks if an alien has been hit by a bolt, if true sets alien to None
        and plays a sound effect
        """
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    for bolt in self._bolts:
                        if bolt.isPlayerBolt():
                            if alien.collides(bolt) == True:
                                self._bolts.remove(bolt)
                                r = row.index(alien)
                                row.remove(alien)
                                row.insert(r,None)
                                r = random.randint(0, 1)
                                aliSound = Sound(ALIEN_DEATH_SOUNDS[r])
                                if self._mute == False:
                                    aliSound.play()
                                self._score += self._aliens.index(row) + 1

    def shipdead(self):
        """
        checks if the ship has been hit by a bolt, if true, makes ship None and
        plays sound effect
        """
        for bolt in self._bolts:
            if self._ship != None:
                if self._ship.collides(bolt) == True:
                    self._bolts.remove(bolt)
                    self._ship = None
                    self._lives -= 1
                    deathSound = Sound('ded.wav')
                    if self._mute == False:
                        deathSound.play()

    def playerWin(self):
        """
        returns: True if all the aliens have been killed, false otherwise
        """
        bottom = []
        for k in range(ALIENS_IN_ROW):
            bottom = bottom + [None]
        for l in range(ALIENS_IN_ROW):
            for row in range(ALIEN_ROWS):
                if self._aliens[row][l] != None:
                    if bottom[l] == None:
                        bottom[l] = row
                    elif row > bottom[l]:
                        bottom[l] = row

        for i in bottom:
            if i != None:
                return False
        return True

    def aliWin(self):
        """
        returns: True if aliens go below the DEFENSE_LINE, False otherwise
        """
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    if alien.bottom <= DEFENSE_LINE:
                        return True
        return False

    def sound(self, input):
        """
        checks if the user toggles to mute the sound in game

        press 'm' to change from mute to unmute or unmute to mute

        parameter input: used to detect user input
        precondition: instance of GInput
        """
        if input.is_key_down('m'):
            if self._waskeydown == False:
                if self._mute:
                    self._mute = False
                else:
                    self._mute = True
            self._waskeydown = True
        else:
            self._waskeydown = False

    def updateWave(self, input, time):
        """
        updates the Wave every time it is called

        parameter input: used to detect user input
        precondition: instance of GInput

        parameter time: Time in seconds since last update
        precondition: time is a number (int or float)
        """
        assert type(input) == GInput
        assert type(time) == int or type(time) == float

        self.alidead()
        self.shipdead()
        self.shipMov(input)
        self.sound(input)
        self.boltFire(input)
        self.aliBolt()

        self._time += time
        if self._time > ALIEN_SPEED * self._speedmult:
            self._time = 0
            self.aliMove()
            self._count +=1

    def wave_draw(self, view):
        """
        draws the game objects to the view

        parameter view: the game view, used in drawing
        precondition: instance of GView
        """
        assert type(view) == GView

        for row in self._aliens:
            for alien in row:
                if alien != None:
                    alien.draw(view)

        if self._ship != None:
            self._ship.draw(view)

        self._dline.draw(view)

        for boltz in self._bolts:
            boltz.draw(view)
