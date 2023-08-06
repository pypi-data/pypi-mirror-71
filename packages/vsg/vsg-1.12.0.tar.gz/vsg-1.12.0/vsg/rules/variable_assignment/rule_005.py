
from vsg import rule
from vsg import check
from vsg import fix
from vsg import line


class rule_005(rule.rule):
    '''
    Variable assignment rule 005 ensures the alignment of the ":=" keyword
    over multiple lines.
    '''

    def __init__(self):
        rule.rule.__init__(self)
        self.name = 'variable_assignment'
        self.identifier = '005'
        self.solution = 'Inconsistent alignment of ":=" in group of lines.'
        self.phase = 5
        self.dVars = create_dictionary()

    def _analyze(self, oFile, oLine, iLineNumber):
        check_for_start_of_group(self.dVars, oLine, iLineNumber)
        if not oLine.insideVariableAssignment and self.dVars['fGroupFound']:
            check.keyword_alignment(self, self.dVars['iStartGroupIndex'], ':=', self.dVars['lGroup'])
            self.dVars = create_dictionary()
        store_line_in_group(self.dVars, oLine)

    def _fix_violations(self, oFile):
        fix.keyword_alignment(self, oFile)


def create_dictionary():
    dVars = {}
    dVars['lGroup'] = []
    dVars['fGroupFound'] = False
    dVars['iStartGroupIndex'] = None
    return dVars


def check_for_start_of_group(dVars, oLine, iLineNumber):
    if oLine.isVariableAssignment and not dVars['fGroupFound']:
        dVars['fGroupFound'] = True
        dVars['iStartGroupIndex'] = iLineNumber


def store_line_in_group(dVars, oLine):
    if dVars['fGroupFound']:
        if oLine.isComment:
            dVars['lGroup'].append(line.line('Removed line'))
        else:
            dVars['lGroup'].append(oLine)
