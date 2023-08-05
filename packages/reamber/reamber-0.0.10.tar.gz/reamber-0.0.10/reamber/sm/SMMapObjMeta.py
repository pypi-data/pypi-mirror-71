from dataclasses import dataclass
from dataclasses import field
from typing import List


class SMMapObjDifficulty:
    BEGINNER: str = "Beginner"
    EASY: str = "Easy"
    MEDIUM: str = "Medium"
    HARD: str = "Hard"
    CHALLENGE: str = "Challenge"
    EDIT: str = "Edit"


class SMMapObjChartTypes:
    # Full Description in CHART_TYPES
    DANCE_SINGLE: str = "dance-single"          # Your normal 4 panel dance mode.
    DANCE_DOUBLE: str = "dance-double"          # Both P1 & P2 pads are used for one player.
    DANCE_SOLO: str = "dance-solo"              # 4-panel, except with additional top-left and top-right columns.
    DANCE_COUPLE: str = "dance-couple"          # One chart, but P1 & P2 have different steps.
    DANCE_THREEPANEL: str = "dance-threepanel"  # Like Single, but the down arrow isn't used.
    DANCE_ROUTINE: str = "dance-routine"        # It's like Couple in that it's for two players
    PUMP_SINGLE: str = "pump-single"            # Single, 5-panel pad.
    PUMP_HALFDOUBLE: str = "pump-halfdouble"    # Uses only six panels in the middle of the pad
    PUMP_DOUBLE: str = "pump-double"            # Same as Dance.
    PUMP_COUPLE: str = "pump-couple"            # Same as Dance.
    PUMP_ROUTINE: str = "pump-routine"          # Same as Dance.
    KB7_SINGLE: str = "kb7-single"              # Standard kb7 layout
    KICKBOX_HUMAN: str = "kickbox-human"        # 4key
    KICKBOX_QUADARM: str = "kickbox-quadarm"    # 4key
    KICKBOX_INSECT: str = "kickbox-insect"      # 6key
    KICKBOX_ARACHNID: str = "kickbox-arachnid"  # 8key
    PARA_SINGLE: str = "para-single"            # 5key.
    BM_SINGLE5: str = "bm-single5"              # 5+1key game mode
    BM_VERSUS5: str = "bm-versus5"              # Unknown, might be the beat equivalent to Couple?
    BM_DOUBLE5: str = "bm-double5"              # Both sides are used.
    BM_SINGLE7: str = "bm-single7"              # 7+1key game mode
    BM_DOUBLE7: str = "bm-double7"              # Both sides are used.
    BM_VERSUS7: str = "bm-versus7"              # Unknown (see versus5)
    EZ2_SINGLE: str = "ez2-single"              # 1 pad
    EZ2_DOUBLE: str = "ez2-double"              # 2 pad
    EZ2_REAL: str = "ez2-real"                  # Divides the hand sensors into upper and lower halves.
    PNM_FIVE: str = "pnm-five"                  # 5key game mode.
    PNM_NINE: str = "pnm-nine"                  # 9key game mode.
    TECHNO_SINGLE4: str = "techno-single4"      # Identical to dance_single
    TECHNO_SINGLE5: str = "techno-single5"      # Identical to pump_single
    TECHNO_SINGLE8: str = "techno-single8"      # eight panels are used: ⬅⬇⬆➡↙↘↗↖
    TECHNO_DOUBLE4: str = "techno-double4"      # Identical to dance_double
    TECHNO_DOUBLE5: str = "techno-double5"      # Identical to pump_double
    TECHNO_DOUBLE8: str = "techno-double8"      # 16 panels (doubles)
    DS3DDX_SINGLE: str = "ds3ddx-single"        # 4key + 4hand...
    MANIAX_SINGLE: str = "maniax-single"        # 4key
    MANIAX_DOUBLE: str = "maniax-double"        # 8key

    @staticmethod
    def getKeys(chart: str) -> int or None:
        if   chart == SMMapObjChartTypes.DANCE_SINGLE:     return 4
        elif chart == SMMapObjChartTypes.DANCE_DOUBLE:     return 8
        elif chart == SMMapObjChartTypes.DANCE_SOLO:       return 6
        elif chart == SMMapObjChartTypes.DANCE_COUPLE:     return 4
        elif chart == SMMapObjChartTypes.DANCE_THREEPANEL: return 3
        elif chart == SMMapObjChartTypes.DANCE_ROUTINE:    return 8
        elif chart == SMMapObjChartTypes.PUMP_SINGLE:      return None
        elif chart == SMMapObjChartTypes.PUMP_HALFDOUBLE:  return None
        elif chart == SMMapObjChartTypes.PUMP_DOUBLE:      return None
        elif chart == SMMapObjChartTypes.PUMP_COUPLE:      return None
        elif chart == SMMapObjChartTypes.PUMP_ROUTINE:     return None
        elif chart == SMMapObjChartTypes.KB7_SINGLE:       return 7
        elif chart == SMMapObjChartTypes.KICKBOX_HUMAN:    return None
        elif chart == SMMapObjChartTypes.KICKBOX_QUADARM:  return None
        elif chart == SMMapObjChartTypes.KICKBOX_INSECT:   return None
        elif chart == SMMapObjChartTypes.KICKBOX_ARACHNID: return None
        elif chart == SMMapObjChartTypes.PARA_SINGLE:      return None
        elif chart == SMMapObjChartTypes.BM_SINGLE5:       return None
        elif chart == SMMapObjChartTypes.BM_VERSUS5:       return None
        elif chart == SMMapObjChartTypes.BM_DOUBLE5:       return None
        elif chart == SMMapObjChartTypes.BM_SINGLE7:       return None
        elif chart == SMMapObjChartTypes.BM_DOUBLE7:       return None
        elif chart == SMMapObjChartTypes.BM_VERSUS7:       return None
        elif chart == SMMapObjChartTypes.EZ2_SINGLE:       return None
        elif chart == SMMapObjChartTypes.EZ2_DOUBLE:       return None
        elif chart == SMMapObjChartTypes.EZ2_REAL:         return None
        elif chart == SMMapObjChartTypes.PNM_FIVE:         return None
        elif chart == SMMapObjChartTypes.PNM_NINE:         return None
        elif chart == SMMapObjChartTypes.TECHNO_SINGLE4:   return None
        elif chart == SMMapObjChartTypes.TECHNO_SINGLE5:   return None
        elif chart == SMMapObjChartTypes.TECHNO_SINGLE8:   return None
        elif chart == SMMapObjChartTypes.TECHNO_DOUBLE4:   return None
        elif chart == SMMapObjChartTypes.TECHNO_DOUBLE5:   return None
        elif chart == SMMapObjChartTypes.TECHNO_DOUBLE8:   return None
        elif chart == SMMapObjChartTypes.DS3DDX_SINGLE:    return None
        elif chart == SMMapObjChartTypes.MANIAX_SINGLE:    return None
        elif chart == SMMapObjChartTypes.MANIAX_DOUBLE:    return None


@dataclass
class SMMapObjMeta:

    chartType: str = SMMapObjChartTypes.DANCE_SINGLE
    description: str = ""
    difficulty: str = SMMapObjDifficulty.EASY
    difficultyVal: int = 1
    grooveRadar: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0, 0.0, 0.0])

    def _readNoteMetadata(self, metadata: List[str]):
        self.chartType = metadata[0].strip()
        self.description = metadata[1].strip()
        self.difficulty = metadata[2].strip()
        self.difficultyVal = int(metadata[3].strip())
        self.grooveRadar = [float(x) for x in metadata[4].strip().split(",")]

    def _readBpms(self, lines: List[str]):
        pass

    def _readStops(self, lines: List[str]):
        pass
