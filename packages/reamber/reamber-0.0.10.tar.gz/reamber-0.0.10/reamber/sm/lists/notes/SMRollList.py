from reamber.sm.lists.notes.SMNoteList import SMNoteList
from reamber.sm.SMRollObj import SMRollObj
from typing import List


class SMRollList(List[SMRollObj], SMNoteList):

    def _upcast(self, objList: List = None):
        return SMRollList(objList)

    def data(self) -> List[SMRollObj]:
        return self

    # Copied from Holds, don't think it's worth splitting this further to just reduce repeated code
    def lengths(self) -> List[float]:
        return self.attribute('length')

    def tailOffsets(self) -> List[float]:
        return [obj() for obj in self.attribute('tailOffset')]
