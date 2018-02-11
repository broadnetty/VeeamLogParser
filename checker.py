import Logger

JobPath = 'Svc.VeeamBackup.log'
#JobPath = 'logs/2017-01-16T120006_Job.LBS_RI-Backup.Backup.1.log'

class LogMessage:
    def __init__(self, date, time, pid, level, words): # , id):
        self.date = date
        self.time = time
        self.pid = pid
        self.level = level
        #self.id = id
        # remove empty words ('')
        self.words = []
        for word in words:
            if word != '':
                self.words.append(word.strip('\r\n'))
        return

class Job:
    def __init__(self,lines):
        self.Lines = self.parse_lines(lines)

    def parse_lines(self, lines):
        logLines = []
        id = 0
        for line in lines:
            id += 1
            if line[0] == '[':
                text = line.split(' ')
                logLines.append(
                    LogMessage(text[0].strip('[]'),  # date
                               text[1].strip('[]'),  # time
                               text[2].strip('<>'),  # pid
                               text[3],  # type
                               text[4:]
                               )  # words
                )
        return logLines


class BackupJob:
    def __init__(self, path):
        self.logger = None
        self.ProxyList = []
        self.VMnames = []

        if path != '':
            fd = open(path, 'r')
            self.Lines = self.parse_lines(fd.readlines())
            print 'Loaded objects: \t' + str(len(self.Lines))
        else:
            self.Lines = []
        return

    def set_logger(self, logger):
        self.logger = logger
        return

    def report(self, msg):
            if self.logger:
                self.logger.Write(msg)

    def parse_lines(self, lines):
        logLines = []
        id = 0
        for line in lines:
            id += 1
            if line[0] == '[':
                text = line.split(' ')
                logLines.append(
                    LogMessage(text[0].strip('[]'),  # date
                               text[1].strip('[]'),  # time
                               text[2].strip('<>'),  # pid
                               text[3],  # type
                               text[4:],
                               id
                               )  # words
                )
        return logLines

    def checkproxyip(self):
        for line in self.Lines:
            if 'Testing' in line.words:
                if line.words[line.words.index('Testing') + 1] == 'proxy':
                    proxy = line.words[3].strip('[],')
                    if proxy not in self.ProxyList:
                        self.ProxyList.append(proxy)
        return self.ProxyList

    def getmachinelist(self):
        for line in self.Lines:
            if self.checkseq(['[VM','name:', 'Source'],line.words) == True:
                vmname = line.words[2].strip('[],')  # line[line.index('[VM name: ') + 11:line.index(', Host ')-1]
                if vmname not in self.VMnames:
                    self.VMnames.append(vmname.strip("'"))
        return self.VMnames

    def getvmid(self, machine):
        for line in self.Lines:
            if self.checkseq(['VM','name:','ref:'],line.words) == True:
                name = line.words[line.words.index('ref:') + 1]
                return name.strip(',')

    def checkseq(self, seq, words):
        if len(seq) == 0:
            return True
        for word in words:
            if seq[0] == word:
                return self.checkseq(seq[1:],words[words.index(word)+1:])
        return False

    def getpex(self, machine, vmid):
        return

# # Check # #
job = BackupJob(JobPath)

