from __future__ import annotations

from typing import Dict, List, Tuple

from .models import Assessment, Answer, Question


def _weighted_average(pairs: List[Tuple[float, float]]) -> float:
    total_weight = sum(weight for _, weight in pairs) or 1.0
    weighted_sum = sum(value * weight for value, weight in pairs)
    return weighted_sum / total_weight


def compute_scores(assessment: Assessment) -> Dict[str, float]:
    """Compute compliance and maturity scores for an assessment.

    Current rule (adjustable later):
    - Answers expected in [0..5].
    - Compliance = weighted average of answers normalized to 0..100.
    - Maturity = simple function of compliance (identity for now).
    """
    answers: List[Answer] = list(
        assessment.answers.select_related("question", "question__dimension")
    )
    value_weight_pairs = [
        (max(0, min(5, float(ans.value))), float(ans.question.weight or 1.0))
        for ans in answers
    ]

    avg_0_to_5 = _weighted_average(value_weight_pairs) if value_weight_pairs else 0.0
    compliance = (avg_0_to_5 / 5.0) * 100.0
    maturity = compliance

    return {"compliance": round(compliance, 2), "maturity": round(maturity, 2)}


def build_recommendations(compliance: float, maturity: float) -> List[str]:
    """Return generic recommendations based on thresholds.

    These are placeholders to be refined later with domain-specific guidance.
    """
    recs: List[str] = []
    if compliance < 40:
        recs.append(
            "Formalize planejamento: escopo, cronograma e riscos com aprovações claras."
        )
        recs.append(
            "Implemente controles mínimos de compliance (políticas internas e registros)."
        )
    elif compliance < 70:
        recs.append(
            "Aprimore gestão de mudanças (comunicação segmentada e patrocínio ativo)."
        )
        recs.append(
            "Fortaleça governança: papéis claros, registro de decisões e checkpoints."
        )
    else:
        recs.append(
            "Consolide lições aprendidas e amplie automação de controles e métricas."
        )

    if maturity < 50:
        recs.append(
            "Priorize entregas incrementais com métricas de valor e adoção pelo usuário."
        )
    return recs


