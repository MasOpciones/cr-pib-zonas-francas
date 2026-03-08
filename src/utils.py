# src/utils.py
# Funciones utilitarias para el proyecto CR PIB Zonas Francas

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ─── Rutas del proyecto ────────────────────────────────────────────
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_RAW = ROOT_DIR / "data" / "raw"
DATA_PROCESSED = ROOT_DIR / "data" / "processed"
OUTPUTS = ROOT_DIR / "outputs" / "graficos"


def cargar_datos(nombre_archivo: str) -> pd.DataFrame:
    """Carga un archivo CSV o Excel desde data/raw/."""
    ruta = DATA_RAW / nombre_archivo
    if ruta.suffix == ".csv":
        return pd.read_csv(ruta)
    elif ruta.suffix in (".xlsx", ".xls"):
        return pd.read_excel(ruta)
    else:
        raise ValueError(f"Formato no soportado: {ruta.suffix}")


def guardar_procesado(df: pd.DataFrame, nombre_archivo: str) -> None:
    """Guarda un DataFrame en data/processed/."""
    ruta = DATA_PROCESSED / nombre_archivo
    df.to_csv(ruta, index=False)
    print(f"Guardado en {ruta}")


def guardar_grafico(fig: plt.Figure, nombre: str, dpi: int = 150) -> None:
    """Guarda una figura de matplotlib en outputs/graficos/."""
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    ruta = OUTPUTS / nombre
    fig.savefig(ruta, dpi=dpi, bbox_inches="tight")
    print(f"Gráfico guardado en {ruta}")
