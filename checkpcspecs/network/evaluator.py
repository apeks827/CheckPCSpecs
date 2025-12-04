"""Network performance evaluation."""

from dataclasses import dataclass
from enum import IntEnum


class NetworkScore(IntEnum):"""Network quality scoring."""
    EXCELLENT = 5
    GOOD = 4
    AVERAGE = 3
    POOR = 2
    VERY_POOR = 1
    UNUSABLE = 0


@dataclass
class NetworkEvaluation:
    """Evaluation of network performance."""
    score: NetworkScore
    score_points: int  # For overall PC score
    download: float
    upload: float
    ping: float


class NetworkEvaluator:
    """Evaluates network performance based on speed and ping."""

    # Thresholds
    MIN_DOWNLOAD_GOOD = 20  # Mbps
    MIN_UPLOAD_GOOD = 10  # Mbps
    MAX_PING_EXCELLENT = 30  # ms
    MAX_PING_GOOD = 100  # ms

    @classmethod
    def evaluate(cls, download: float, upload: float, ping: float) -> NetworkEvaluation:
        """Evaluate network performance.
        
        Args:
            download: Download speed in Mbps
            upload: Upload speed in Mbps
            ping: Ping latency in milliseconds
            
        Returns:
            NetworkEvaluation with score and details
        """
        speed_good = download >= cls.MIN_DOWNLOAD_GOOD and upload >= cls.MIN_UPLOAD_GOOD
        ping_excellent = ping <= cls.MAX_PING_EXCELLENT
        ping_good = ping <= cls.MAX_PING_GOOD

        if speed_good:
            if ping_excellent:
                score = NetworkScore.EXCELLENT
                points = 5
            elif ping_good:
                score = NetworkScore.GOOD
                points = 2
            else:
                score = NetworkScore.AVERAGE
                points = 0
        else:
            if ping_excellent:
                score = NetworkScore.POOR
                points = 2
            elif ping_good:
                score = NetworkScore.VERY_POOR
                points = 1
            else:
                score = NetworkScore.UNUSABLE
                points = 0

        return NetworkEvaluation(
            score=score,
            score_points=points,
            download=download,
            upload=upload,
            ping=ping
        )
