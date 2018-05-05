#!/usr/bin/env python3
class ScreenshotMetadata:
    def __init__(self, kingdom = None, x = None, y = None, level = None, date = None, time = None, monster_name = None, defeated = None):
        self.kingdom = kingdom
        self.x = x
        self.y = y
        self.level = level
        self.date = date
        self.time = time
        self.monster_name = monster_name
        self.defeated = defeated

    def Hash(self):
        return

    def Completed(self):
        return (self.kingdom   is not None) \
        and (self.x            is not None) \
        and (self.y            is not None) \
        and (self.level        is not None) \
        and (self.date         is not None) \
        and (self.time         is not None) \
        and (self.monster_name is not None) \
        and (self.defeated == True)# and self.defeated == True)

    def __str__(self):
        string = 'K: ' + self.kingdom  \
        + '\nX: '      + self.x        \
        + '\nY: '      + self.y        \
        + '\nLevel: '  + self.level    \
        + '\nDate: '   + self.date     \
        + '\nTime: '   + self.time     \
        + '\nMonster: '+ self.monster_name
        return string

    def __eq__(self, other):
        return (self.kingdom      == other.kingdom)         \
        and    (self.x            == other.x)               \
        and    (self.y            == other.y)               \
        and    (self.level        == other.level)           \
        and    (self.date         == other.date)            \
        and    (self.time         == other.time)            \
        and    (self.monster_name == other.monster_name)    \
        and    (self.defeated     == other.defeated)        \

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((self.kingdom, self.x, self.y, self.level, self.date, self.time, self.monster_name, self.defeated))
