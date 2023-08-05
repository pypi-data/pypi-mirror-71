class RAConst :

    HR_TO_MIN   : float = 60.0
    HR_TO_SEC   : float = 60.0 * 60.0
    HR_TO_MSEC  : float = 60.0 * 60.0 * 1000.0
    MIN_TO_HR   : float = 1.0 / 60.0
    MIN_TO_SEC  : float = 60.0
    MIN_TO_MSEC : float = 60.0 * 1000.0
    SEC_TO_HR   : float = 1.0 / (60.0 * 60.0)
    SEC_TO_MIN  : float = 1.0 / 60.0
    SEC_TO_MSEC : float = 1000.0
    MSEC_TO_HR  : float = 1.0 / (60.0 * 60.0 * 1000.0)
    MSEC_TO_MIN : float = 1.0 / (60.0 * 1000.0)
    MSEC_TO_SEC : float = 1.0 / 1000.0

    @staticmethod
    def hrToMin(hours): return float(hours * RAConst.HR_TO_MIN)
    @staticmethod
    def hrToSec(hours): return float(hours * RAConst.HR_TO_SEC)
    @staticmethod
    def hrToMSec(hours): return float(hours * RAConst.HR_TO_MSEC)
    @staticmethod
    def minToHr(mins): return float(mins * RAConst.MIN_TO_HR)
    @staticmethod
    def minToSec(mins): return float(mins * RAConst.MIN_TO_SEC)
    @staticmethod
    def minToMSec(mins): return float(mins * RAConst.MIN_TO_MSEC)
    @staticmethod
    def secToHr(secs): return float(secs * RAConst.SEC_TO_HR)
    @staticmethod
    def secToMin(secs): return float(secs * RAConst.SEC_TO_MIN)
    @staticmethod
    def secToMSec(secs): return float(secs * RAConst.SEC_TO_MSEC)
    @staticmethod
    def mSecToHr(msecs): return float(msecs * RAConst.MSEC_TO_HR)
    @staticmethod
    def mSecToMin(msecs): return float(msecs * RAConst.MSEC_TO_MIN)
    @staticmethod
    def mSecToSec(msecs): return float(msecs * RAConst.MSEC_TO_SEC)
