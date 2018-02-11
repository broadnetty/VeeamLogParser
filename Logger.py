import sys

## EXAMPLE ##
#logf = open('main.log', 'aw')
#logger = Logger()
#logger.SetTarget(logf)
#logger.Write('==================================')
#logger.Write('Starting script')


## CLASSES ##
class Logger:
    def __init__(self):
        self.target = sys.stdout
        return

    def SetTarget(self, target):
        if target == None:
            self.target = sys.stdout
        elif type(target) == 'file':
            self.target = open('log', 'raw')
        else:
            self.target = target
        return

    def Clear(self, target):
        return

    ## log to somewhere
    def Write(self, msg):
        self.target.write(str(datetime.datetime.now()) + ' ' + msg + '\n')
        return

