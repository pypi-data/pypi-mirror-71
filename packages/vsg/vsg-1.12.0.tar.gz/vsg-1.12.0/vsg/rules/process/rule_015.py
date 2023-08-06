
from vsg import rule
from vsg import fix


class rule_015(rule.rule):
    '''
    Process rule 015 checks for a blank line or a comment line above the "process" keyword.
    '''

    def __init__(self):
        rule.rule.__init__(self, 'process', '015')
        self.solution = 'Add a space or a comment above the "process" keyword.'
        self.phase = 3

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.isProcessKeyword and \
           not oFile.lines[iLineNumber - 1].isBlank and \
           not oFile.lines[iLineNumber - 1].isComment:
            self.add_violation(iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations[::-1]:
            fix.insert_blank_line_above(self, oFile, iLineNumber)
