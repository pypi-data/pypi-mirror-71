from reamber.algorithms.analysis.bpm.bpmActivity import bpmActivity
from reamber.osu.OsuMapObj import OsuMapObj
from reamber.sm.SMMapSetObj import SMMapObj
from reamber.quaver.QuaMapObj import QuaMapObj
from typing import overload, List, Dict


@overload
def scrollSpeed(m: OsuMapObj, centerBpm: float = None) -> List[Dict[str, float]]: ...
@overload
def scrollSpeed(m: SMMapObj, centerBpm: float = None) -> List[Dict[str, float]]: ...
@overload
def scrollSpeed(m: QuaMapObj, centerBpm: float = None) -> List[Dict[str, float]]: ...
def scrollSpeed(m: QuaMapObj, centerBpm: float = None) -> List[Dict[str, float]]:
    """ Evaluates the scroll speed based on mapType
    :param m: The Map Object
    :param centerBpm: The bpm to zero calculations on. If None, it'll calculate the bpm that lasts the longest
    e.g. if BPM == 200.0 and CenterBPM == 100.0, it'll return {'offset': X, 'speed': 2.0}
    :return: Returns a list dict of keys offset and speed
    """

    # This automatically calculates the center BPM
    if centerBpm is None: centerBpm = sorted(bpmActivity(m), key=lambda x: x[1])[-1]

    if isinstance(m, SMMapObj):  # SM doesn't have SV
        return [dict(offset=bpm.offset, speed=bpm.bpm/centerBpm[0].bpm) for bpm in m.bpms]

    svPairs = [(offset, multiplier) for offset, multiplier in zip(m.svs.sorted().offsets(), m.svs.multipliers())]
    bpmPairs = [(offset, bpm) for offset, bpm in zip(m.bpms.offsets(), m.bpms.bpms())]

    currBpmIter = 0
    nextBpmOffset = None if len(bpmPairs) == 1 else bpmPairs[1][0]
    speedList = []

    for offset, sv in svPairs:
        while offset < bpmPairs[0][0]:  # Offset cannot be less than the first bpm
            continue
        # Guarantee that svOffset is after first bpm
        if nextBpmOffset and offset >= nextBpmOffset:
            currBpmIter += 1
            if currBpmIter != len(bpmPairs):
                nextBpmOffset = bpmPairs[currBpmIter][0]
            else:
                nextBpmOffset = None
        speedList.append(dict(offset=offset, speed=bpmPairs[currBpmIter][1] * sv / centerBpm[0].bpm))

    return speedList
