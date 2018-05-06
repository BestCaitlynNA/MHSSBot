class MHSSException(Exception):
    def __init__(self, message=None):#, errors):
        if message is None:
            message = "An error occured with the bot."
        self.message = message
        super(MHSSException, self).__init__(message)
        #self.errors = errors
