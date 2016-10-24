from Issues.Issue import Issue, NullIssue

class IssuesCollection(object):

    testIssue = Issue('testIssue')
    testIssue.SetTextsearchTerms(['legal', 'board'])

    def __init__(self):
        self.__issues = {self.testIssue.Name: self.testIssue}

    def GetIssueFromName(self, name):
        return self.__issues.get(name, NullIssue())