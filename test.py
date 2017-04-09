import datetime
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
print('['+bcolors.OKGREEN + "Warning" + bcolors.ENDC+']')
start_time = datetime.datetime(2021,5,4,12,00)
seconds = (start_time - datetime.datetime.today())

k = ['123',123]
print "%s : %d"%(k[0],k[1])
print seconds.hour
