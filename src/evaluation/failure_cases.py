import json
import logging
from dataclasses import dataclass, asdict
from typing import List
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class FailureCase:
    question: str
    true_answer: str
    generated_answer: str
    contradiction_level: int
    confidence: float
    is_correct: bool
    category: str

class FailureCaseLogger:
    """Logs generation failures, specifically overconfidence under contradiction."""
    def __init__(self, output_dir: str = "benchmark/failure_cases", filename: str = "failure_log.json"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.filename = filename
        self.cases: List[FailureCase] = []

    def log_case(self, question: str, true_answer: str, generated_answer: str,
                 contradiction_level: int, confidence: float, is_correct: bool):
        
        # Categorize the prediction
        category = "True Positive (Correct & Confident)"
        if is_correct and confidence < 0.5:
            category = "False Negative (Correct but Unconfident)"
        elif not is_correct and confidence > 0.8:
            if contradiction_level >= 3:
                category = "Contradictory Evidence, Still High Confidence (Primary Failure)"
            else:
                category = "False Positive (Overconfident)"
        elif not is_correct and confidence <= 0.8:
            category = "True Negative (Incorrect & Unconfident)"
        
        case = FailureCase(
            question=question,
            true_answer=true_answer,
            generated_answer=generated_answer,
            contradiction_level=contradiction_level,
            confidence=confidence,
            is_correct=is_correct,
            category=category
        )
        self.cases.append(case)

    def export(self):
        output_path = self.output_dir / self.filename
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump([asdict(c) for c in self.cases], f, indent=2)
        logger.info(f"Exported {len(self.cases)} evaluated cases to {output_path}")

    def summary(self) -> dict:
        summary_counts = {}
        for case in self.cases:
            summary_counts[case.category] = summary_counts.get(case.category, 0) + 1
        return summary_counts
