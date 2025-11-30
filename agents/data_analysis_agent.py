from typing import Any, Dict

import pandas as pd


class DataAnalysisAgent:
    """
    Agent responsible for deterministic analysis over the experiment summary table.

    Expects a summary_df with at least the following columns:
      - 'algorithm'
      - 'gmapping'
      - 'duration_min'
      - 'rmse_error'
      - (optionally: 'mae_error', 'max_error', 'cpu_mean', 'memory_mean')
    """

    def __init__(self, summary_df: pd.DataFrame) -> None:
        if summary_df is None or summary_df.empty:
            raise ValueError("summary_df must be a non-empty pandas DataFrame.")
        self.summary_df = summary_df.copy()

    def get_min_rmse(self) -> Dict[str, Any]:
        """
        Return the row (as dict) corresponding to the configuration
        with the globally minimum RMSE.
        """
        if "rmse_error" not in self.summary_df.columns:
            raise KeyError("summary_df is missing required column 'rmse_error'.")

        idx = self.summary_df["rmse_error"].idxmin()
        return self.summary_df.loc[idx].to_dict()

    def filter_by_gmapping_and_duration(
        self, gmapping_state: str, duration_min: int
    ) -> pd.DataFrame:
        """
        Filter the summary_df by gmapping state ('ON' or 'OFF') and duration in minutes.
        Returns a copy of the filtered DataFrame.
        """
        if "gmapping" not in self.summary_df.columns:
            raise KeyError("summary_df is missing required column 'gmapping'.")
        if "duration_min" not in self.summary_df.columns:
            raise KeyError("summary_df is missing required column 'duration_min'.")

        gmapping_state = gmapping_state.upper()
        mask = (
            (self.summary_df["gmapping"] == gmapping_state)
            & (self.summary_df["duration_min"] == duration_min)
        )
        return self.summary_df.loc[mask].copy()

    def filter_by_algorithm(
        self, algorithm_name: str, gmapping_state: str | None = None
    ) -> pd.DataFrame:
        """
        Optionally filter by algorithm (e.g., 'AlgorithmA') and optional gmapping state.
        """
        if "algorithm" not in self.summary_df.columns:
            raise KeyError("summary_df is missing required column 'algorithm'.")

        df = self.summary_df[self.summary_df["algorithm"] == algorithm_name].copy()

        if gmapping_state is not None:
            if "gmapping" not in df.columns:
                raise KeyError("summary_df is missing required column 'gmapping'.")
            gmapping_state = gmapping_state.upper()
            df = df[df["gmapping"] == gmapping_state].copy()

        return df
