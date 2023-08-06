
from vsg import rule
from vsg import utils

import copy


class rule_013(rule.rule):
    '''
    Port rule 013 checks for multiple ports declared on single line.
    '''

    def __init__(self):
        rule.rule.__init__(self, 'port', '013')
        self.solution = 'Place multiple ports on their own lines.'
        self.phase = 1

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.isPortDeclaration:
            if len(utils.extract_port_names_from_port_map(oLine)) > 1:
                self.add_violation(iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations[::-1]:
            oLine = oFile.lines[iLineNumber]
            iNumberOfPorts = oLine.line.split(':')[0].count(',') + 1
            iLeadingSpaces = utils.begin_of_line_index(oLine)
            # Replicate ports
            for iIndex in range(1, iNumberOfPorts):
                oFile.lines.insert(iLineNumber, copy.deepcopy(oLine))
            # Split ports
            for iIndex in range(0, iNumberOfPorts):
                oLine = oFile.lines[iLineNumber + iIndex]
                lLine = oLine.line.split(':', 1)
                lPorts = lLine[0].split(',')
                oLine.update_line(' ' * iLeadingSpaces + lPorts[iIndex].strip() + ' :' + lLine[1])
