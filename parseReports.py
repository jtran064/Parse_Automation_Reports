lSuccess = 'test_run_this_test Success'
lFailure = 'test_run_this_test Failure'
lError = 'test_run_this_test Error'
lTestStep = 'Test Step'
lFailStep = 'C:/Python27'
lFailStep2 = 'F]]>'
lExceptOpen = '<exception>'
lExceptClose = '</exception>'

class ParseReport(object):

    def __init__(self):
        # do nothing for now
        pass

    def printLines(self, lis):
        for item in lis:
            print item

    def concatLines(self, lis):
        final = ''
        for item in lis:
            final += item.rstrip('\n')
        return final

    def findException(self, s):
        n = '/n'
        e = ']>'
        count = 0
        last = ''
        nExcept = False
        lastExcept = ''
        lExcept = False
        while count < len(s) - 1:
            count += 1
            if count < 1:
                continue
            elif s[count-1:count+1] == e:
                return lastExcept
            elif nExcept == False:
                if s[count-1:count+1] == n:
                    nExcept = True
                    last = s[count-1:count+1]
                else:
                    last += s[count]
            elif nExcept == True:
                if s[count-1:count+1] == n:
                    last += s[count]
                    lastExcept = last
                    nExcept = False
                else:
                    last += s[count]
        return lastExcept

    def run(self):
        addTo = 'pass'
        testStep = []
        testException = []
        testStepList = []
        testExceptionList = []
        f = open('testReport.txt', 'r+')

        lines = f.readlines()

        for line in lines:
            if addTo == 'pass':
                if line[0:len(lFailure)] == lFailure:
                    addTo = 'fail'
            if addTo == 'fail':
                if line[0:len(lTestStep)] == lTestStep:
                    testStep.append(line)
                    addTo = 'failStep'
            if addTo == 'failStep':
                if line[0:len(lTestStep)] == lTestStep:
                    testStep = []
                    testStep.append(line)
                elif line[0:len(lFailStep)] == lFailStep or line[0:len(lFailStep2)] == lFailStep2:
                    addTo = 'except'
                    testException.append(line)
                    testStepList.append(self.concatLines(testStep))
                    testStep = []
                else:
                    testStep.append(line)
            elif addTo == 'except':
                if line[0:len(lExceptOpen)] == lExceptOpen:
                    addTo = 'exceptOpen'
                    testException = []
                    testException.append(line)
            elif addTo == 'exceptOpen':
                if line[0:len(lExceptClose)] == lExceptClose:
                    addTo = 'pass'
                    testException.append(line)
                    testExceptionList.append(self.findException(self.concatLines(
                        testException)))
                else:
                    testException.append(line)

        count = 0
        for i in testStepList:
            count += 1
            print str(count) + '. ' + i
            #print '\n'

        count = 0
        for i in testExceptionList:
            count += 1
            print str(count) + '. ' + i
            #print '\n'

        f.close()

if __name__ == "__main__":
    pr = ParseReport()
    pr.run()
