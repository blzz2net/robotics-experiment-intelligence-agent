from typing import Optional

import pandas as pd

from .data_analysis_agent import DataAnalysisAgent
from .explanation_agent import ExplanationAgent
from .memory_store import MemoryStore


class OrchestratorAgent:
    """
    High-level orchestrator that interprets user questions and delegates to:
      - DataAnalysisAgent (metrics and filtering)
      - ExplanationAgent (natural language summaries)
      - MemoryStore (context/history)

    This version implements a small set of supported query patterns.
    In a production system, this could be replaced or augmented by a Gemini-backed
    intent interpreter while leaving metric computation deterministic.
    """

    def __init__(self, summary_df: pd.DataFrame) -> None:
        self.memory = MemoryStore()
        self.analysis_agent = DataAnalysisAgent(summary_df)
        self.explainer = ExplanationAgent()

    def answer(self, question: str) -> str:
        """
        Answer a user question using simple rule-based intent detection.

        Supported intents include:
          - Asking for the configuration with minimum localization error / lowest RMSE.
          - Comparing the effect of Gmapping for 10-minute runs.
        """
        q = question.lower().strip()

        # Intent 1: best configuration by RMSE
        if (
            "minimum localization error" in q
            or "lowest rmse" in q
            or "best configuration" in q
        ):
            best = self.analysis_agent.get_min_rmse()
            text = self.explainer.explain_best_config(best)
            self.memory.add_entry(question, {"best_config": best})
            return text

        # Intent 2: gmapping effect for 10-minute runs (example logic)
        if "gmapping" in q and ("10" in q or "10-minute" in q or "ten minute" in q):
            df_on = self.analysis_agent.filter_by_gmapping_and_duration("ON", 10)
            df_off = self.analysis_agent.filter_by_gmapping_and_duration("OFF", 10)
            text = self.explainer.explain_gmapping_effect(df_on, df_off, duration=10)
            self.memory.add_entry(
                question,
                {
                    "gmapping_on_runs": df_on.to_dict(orient="records"),
                    "gmapping_off_runs": df_off.to_dict(orient="records"),
                },
            )
            return text

        # Fallback when the question is not matched by current rules
        return (
            "This prototype currently supports a limited set of queries, such as:\n"
            "- 'Which configuration has the minimum localization error?'\n"
            "- 'How does Gmapping affect localization for 10-minute runs?'\n"
            "You asked: "
            f"'{question}'. To handle more query types, the orchestration logic can be extended."
        )

    def get_history(self) -> list:
        """Convenience method to expose conversation history."""
        return self.memory.get_history()
