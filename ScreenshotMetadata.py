class ScreenshotMetadata:
    def __init__(self):
        self.kingdom = None
        self.x = None
        self.y = None
        self.level = None
        self.date = None
        self.time = None
        self.monster_name = None
        self.defeated = False

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
        and (self.defeated = True)# and self.defeated == True)

    def __str__(self):
        string = 'K: ' + self.kingdom  \
        + '\nX: '      + self.x        \
        + '\nY: '      + self.y        \
        + '\nLevel: '  + self.level    \
        + '\nDate: '   + self.date     \
        + '\nTime: '   + self.time     \
        + '\nMonster: '+ self.monster_name
        return string
