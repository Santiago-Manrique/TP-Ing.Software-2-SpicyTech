"""Módulo analítico para SpicyTech.

Paso 1:
- Genera un dataset simulado de n=50 reservas.
- Calcula media, mediana y moda de Y (Horas Reservadas).
- Ajusta una regresión lineal por mínimos cuadrados.
- Calcula el coeficiente de Pearson.
- Ejecuta una prueba t unilateral con H0: media <= 4 vs H1: media > 4.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression


@dataclass
class AnalyticsResult:
    dataset: pd.DataFrame
    mean_y: float
    median_y: float
    mode_y: float
    slope: float
    intercept: float
    pearson_r: float
    t_statistic: float
    p_value: float


def generate_dataset(n: int = 50, seed: int = 42) -> pd.DataFrame:
    """Genera un dataset reproducible de reservas simuladas."""
    rng = np.random.default_rng(seed)
    x = rng.integers(0, 21, size=n)  # Días de anticipación
    noise = rng.normal(0, 1.1, size=n)
    y = 3.2 + (0.22 * x) + noise
    y = np.clip(y, 0.5, None)
    y = np.round(y, 2)

    df = pd.DataFrame({
        "dias_anticipacion": x.astype(int),
        "horas_reservadas": y.astype(float),
    })
    return df.sort_values("dias_anticipacion").reset_index(drop=True)


def descriptive_stats(y: pd.Series) -> tuple[float, float, float]:
    """Calcula media, mediana y moda de Y."""
    mean_y = float(y.mean())
    median_y = float(y.median())
    mode_series = y.mode()
    mode_y = float(mode_series.iloc[0]) if not mode_series.empty else float("nan")
    return mean_y, median_y, mode_y


def fit_least_squares(x: pd.Series, y: pd.Series) -> tuple[float, float, float]:
    """Ajusta regresión lineal simple y devuelve pendiente, intercepto y r de Pearson."""
    model = LinearRegression()
    x_values = x.to_numpy().reshape(-1, 1)
    y_values = y.to_numpy()
    model.fit(x_values, y_values)

    slope = float(model.coef_[0])
    intercept = float(model.intercept_)
    pearson_r, _ = stats.pearsonr(x_values.ravel(), y_values)
    return slope, intercept, float(pearson_r)


def one_sided_t_test(y: pd.Series, popmean: float = 4.0) -> tuple[float, float]:
    """Prueba t unilateral H0: media <= popmean vs H1: media > popmean."""
    result = stats.ttest_1samp(y.to_numpy(), popmean=popmean, alternative="greater")
    return float(result.statistic), float(result.pvalue)


def analyze_reservations(n: int = 50, seed: int = 42) -> AnalyticsResult:
    dataset = generate_dataset(n=n, seed=seed)
    y = dataset["horas_reservadas"]
    x = dataset["dias_anticipacion"]

    mean_y, median_y, mode_y = descriptive_stats(y)
    slope, intercept, pearson_r = fit_least_squares(x, y)
    t_statistic, p_value = one_sided_t_test(y, popmean=4.0)

    return AnalyticsResult(
        dataset=dataset,
        mean_y=mean_y,
        median_y=median_y,
        mode_y=mode_y,
        slope=slope,
        intercept=intercept,
        pearson_r=pearson_r,
        t_statistic=t_statistic,
        p_value=p_value,
    )


def _format_result(result: AnalyticsResult) -> str:
    return (
        "\n".join(
            [
                "=== SpicyTech Analytics - Paso 1 ===",
                f"Muestra: {len(result.dataset)} reservas",
                f"Media(Y): {result.mean_y:.3f}",
                f"Mediana(Y): {result.median_y:.3f}",
                f"Moda(Y): {result.mode_y:.3f}",
                f"Recta LS: Y = {result.intercept:.3f} + {result.slope:.3f} * X",
                f"Pearson r: {result.pearson_r:.3f}",
                f"t-statistic: {result.t_statistic:.3f}",
                f"p-value (unilateral): {result.p_value:.6f}",
                "",
                "Primeras 5 filas:",
                result.dataset.head().to_string(index=False),
            ]
        )
    )


if __name__ == "__main__":
    analytics_result = analyze_reservations(n=50, seed=42)
    print(_format_result(analytics_result))
