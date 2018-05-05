class ScreenshotMetadata:
    def __init__(self, kingdom = None, x = None, y = None, level = None, date = None, monster_name = None, defeated = None):
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
