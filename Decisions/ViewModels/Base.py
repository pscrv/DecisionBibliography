import re
from Decisions.DBProxy import DecisionModelProxy

class  VMBase(object):

    def __init__(self):
        boardList = DecisionModelProxy.GetBoardList()
        boardGroups = self.__groupBoards(boardList)
        for group in boardGroups:
            boardGroups[group] = sorted(boardGroups[group])

        self.Context = {
            'boards': sorted(boardGroups.items())
            }


    def __groupBoards(self, boardList):
        numberedBoardFinder = re.compile(r'^(\d*).(\d*).(\d*)$')
        boardGroups = {}        
        for board in boardList:
            if board == '':
                continue
            numberedBoard = re.search(numberedBoardFinder, board)
            if numberedBoard:
                self.__addNumeredBoardToGroup(board, boardGroups, numberedBoard)
            else:
                self.__addSpecialBoardToGroup(board, boardGroups)
        return boardGroups


    def __addNumeredBoardToGroup(self, board, boardGroups, parseBoard):
        groupName = parseBoard.group(1) + '.' + parseBoard.group(2)
        group = boardGroups.get(groupName, [])
        if group == []:
            boardGroups[groupName] = group
        group.append(board)


    def __addSpecialBoardToGroup(self, board, boardGroups):
        newGroup = [ board ]
        boardGroups[board] = newGroup

