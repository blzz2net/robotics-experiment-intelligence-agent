from typing import Dict

import pandas as pd


class ExplanationAgent:
    """
    Agent responsible for turning numeric metrics into human-readable explanations.
    It assumes that metrics are already computed deterministically elsewhere.
    """

    def explain_best_config(self, best_row: Dict) -> str:
        """
        Generate a concise explanation for the best configuration by RMSE.
        Expects keys like:
          - 'algorithm', 'gmapping', 'duration_min'
          - 'rmse_error', 'mae_error', 'max_error'
          - 'cpu_mean', 'memory_mean'
        """
        algo = best_row.get("algorithm", "UnknownAlgorithm")
        gmapping = best_row.get("gmapping", "UNKNOWN")
        duration = int(best_row.get("duration_min", -1))

        rmse = best_row.get("rmse_error", None)
        mae = best_row.get("mae_error", None)
        max_err = best_row.get("max_error", None)
        cpu = best_row.get("cpu_mean", None)
        mem = best_row.get("memory_mean", None)

        parts: list[str] = []
        parts.append(
            f"The best configuration by RMSE is {algo} with Gmapping {gmapping} "
            f"for a duration of {duration} minutes."
        )

        metrics_str = []
        if rmse is not None:
            metrics_str.append(f"RMSE = {rmse:.4f} m")
        if mae is not None:
            metrics_str.append(f"MAE = {mae:.4f} m")
        if max_err is not None:
            metrics_str.append(f"maximum error = {max_err:.4f} m")
        if metrics_str:
            parts.append(" ".join(metrics_str) + ".")

        resource_str = []
        if cpu is not None:
            resource_str.append(f"CPU ≈ {cpu:.1f}%")
        if mem is not None:
            resource_str.append(f"Memory ≈ {mem:.1f} MB")
        if resource_str:
            parts.append("Resource usage: " + ", ".join(resource_str) + ".")

        return "\n".join(parts)

    def explain_gmapping_effect(
        self, df_on: pd.DataFrame, df_off: pd.DataFrame, duration: int
    ) -> str:
        """
        Explain the effect of enabling/disabling mapping (Gmapping) for a given duration.
        Expects data frames where 'rmse_error' contains localization RMSE.
        """
        if df_on.empty and df_off.empty:
            return f"No runs found for {duration}-minute duration with any Gmapping setting."

        if df_on.empty:
            return (
                f"No runs found for {duration}-minute duration with Gmapping ON. "
                f"Only OFF runs are available for comparison."
            )
        if df_off.empty:
            return (
                f"No runs found for {duration}-minute duration with Gmapping OFF. "
                f"Only ON runs are available for comparison."
            )

        if "rmse_error" not in df_on.columns or "rmse_error" not in df_off.columns:
            return (
                "Cannot compare Gmapping effect because 'rmse_error' is missing "
                "from one or both data sets."
            )

        mean_on = float(df_on["rmse_error"].mean())
        mean_off = float(df_off["rmse_error"].mean())
        diff = mean_off - mean_on

        if diff > 0:
            direction = "lower"
        elif diff < 0:
            direction = "higher"
        else:
            direction = "the same"

        explanation_lines = [
            f"For {duration}-minute runs:",
            f"- Gmapping ON:  average RMSE = {mean_on:.4f} m",
            f"- Gmapping OFF: average RMSE = {mean_off:.4f} m",
            "",
        ]

        if diff != 0:
            explanation_lines.append(
                f"On average, enabling Gmapping yields {abs(diff):.4f} m {direction} "
                f"localization error compared to disabling it."
            )
        else:
            explanation_lines.append(
                "On average, enabling or disabling Gmapping results in the same RMSE for this duration."
            )

        return "\n".join(explanation_lines)
