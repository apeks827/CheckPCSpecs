"""Score calculation and PC evaluation."""

from dataclasses import dataclass
from enum import Enum


class PCVerdict(Enum):
    """Overall PC verdict based on score."""
    MEETS_REQUIREMENTS = "meets_requirements"
    MEETS_MINIMUM = "meets_minimum"
    DOES_NOT_MEET = "does_not_meet"


@dataclass
class PCScore:
    """Overall PC score and verdict."""
    total_score: int
    verdict: PCVerdict

    @property
    def verdict_text_ru(self) -> str:
        """Get verdict text in Russian."""
        return {
            PCVerdict.MEETS_REQUIREMENTS: "ПК соответствует требованиям",
            PCVerdict.MEETS_MINIMUM: "ПК соответствует минимальным требованиям",
            PCVerdict.DOES_NOT_MEET: "ПК не соответствует требованиям"
        }[self.verdict]

    @property
    def verdict_color(self) -> str:
        """Get color for verdict display."""
        return {
            PCVerdict.MEETS_REQUIREMENTS: "green",
            PCVerdict.MEETS_MINIMUM: "DarkOrange3",
            PCVerdict.DOES_NOT_MEET: "red"
        }[self.verdict]


class ScoreCalculator:
    """Calculates overall PC score from component scores."""

    THRESHOLD_MEETS = 18
    THRESHOLD_MINIMUM = 0

    @classmethod
    def calculate(cls, *component_scores: int) -> PCScore:
        """Calculate overall PC score from component scores.
        
        Args:
            *component_scores: Individual component scores
            
        Returns:
            PCScore with total and verdict
        """
        total = sum(component_scores)

        if total >= cls.THRESHOLD_MEETS:
            verdict = PCVerdict.MEETS_REQUIREMENTS
        elif total >= cls.THRESHOLD_MINIMUM:
            verdict = PCVerdict.MEETS_MINIMUM
        else:
            verdict = PCVerdict.DOES_NOT_MEET

        return PCScore(total_score=total, verdict=verdict)
