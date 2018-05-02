class ScreenshotMetadata:
    def __init__(self):
        self.x = -1
        self.y = -1
        self.level = 'None'
        self.date = 'None'
        self.time = 'None'
        self.monster_name = 'None'
        self.defeated = False

    def Hash(self):
        return

    def Completed(self):
        return (self.x != -1 and self.y != -1 and self.level != 'None' and self.date != 'None' and self.time != 'None' and self.monster_name != 'None' and self.defeated = True)
