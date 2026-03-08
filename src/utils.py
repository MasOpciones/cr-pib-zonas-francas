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


def exportar_grafico(fig: plt.Figure, nombre: str, carpeta: str | Path = "../outputs/graficos/") -> None:
    """
    Exporta una figura de matplotlib en 6 versiones (3 formatos x 2 temas).

    - **Formatos (px)**:
      - Square: 1080x1080
      - 16:9: 1920x1080
      - LinkedIn: 1200x627
    - **Temas**:
      - Light: fondo blanco, texto negro, grilla gris claro
      - Dark: fondo #0D0D0D, texto blanco, grilla gris oscuro
    - **Color principal** (líneas y elementos): #60ff12
    - **DPI**: 150 para todos los formatos

    La función modifica temporalmente estilo/tamaño de `fig` para exportar, y luego
    restaura el tamaño original.

    Parámetros
    ----------
    fig:
        Figura de matplotlib (ej. retornada por `plt.subplots()`).
    nombre:
        Nombre base del archivo (sin extensión). Ej: `"pib_regimen"`.
    carpeta:
        Carpeta de salida. Si es relativa, se interpreta relativa a la raíz del proyecto.

    Archivos generados
    ------------------
    - `{nombre}_light_square.png`
    - `{nombre}_dark_square.png`
    - `{nombre}_light_16x9.png`
    - `{nombre}_dark_16x9.png`
    - `{nombre}_light_linkedin.png`
    - `{nombre}_dark_linkedin.png`
    """

    DPI = 150
    COLOR_PRINCIPAL = "#60ff12"
    FORMATOS_PX: dict[str, tuple[int, int]] = {
        "square": (1080, 1080),
        "16x9": (1920, 1080),
        "linkedin": (1200, 627),
    }
    TEMAS = {
        "light": {"bg": "#FFFFFF", "fg": "#000000", "grid": "#D9D9D9"},
        "dark": {"bg": "#0D0D0D", "fg": "#FFFFFF", "grid": "#3A3A3A"},
    }

    def _resolver_carpeta(dest: str | Path) -> Path:
        p = Path(dest)
        if not p.is_absolute():
            p = (ROOT_DIR / p).resolve()
        return p

    def _aplicar_tema_y_color(fig_: plt.Figure, tema: dict[str, str]) -> None:
        # Figura (fondo general)
        fig_.set_facecolor(tema["bg"])

        for ax in fig_.get_axes():
            # Fondo del área de dibujo
            ax.set_facecolor(tema["bg"])

            # Títulos/labels/ticks
            ax.title.set_color(tema["fg"])
            ax.xaxis.label.set_color(tema["fg"])
            ax.yaxis.label.set_color(tema["fg"])
            ax.tick_params(axis="both", colors=tema["fg"])

            # Spines
            for spine in ax.spines.values():
                spine.set_color(tema["fg"])

            # Grid
            ax.grid(True, color=tema["grid"], linewidth=0.8, alpha=1.0)

            # Líneas
            for line in ax.get_lines():
                line.set_color(COLOR_PRINCIPAL)
                line.set_markerfacecolor(COLOR_PRINCIPAL)
                line.set_markeredgecolor(COLOR_PRINCIPAL)

            # Colecciones (scatter, etc.)
            for col in ax.collections:
                try:
                    col.set_facecolor(COLOR_PRINCIPAL)
                except Exception:
                    pass
                try:
                    col.set_edgecolor(COLOR_PRINCIPAL)
                except Exception:
                    pass

            # Patches (barras, áreas, etc.)
            for patch in ax.patches:
                try:
                    patch.set_facecolor(COLOR_PRINCIPAL)
                except Exception:
                    pass
                try:
                    patch.set_edgecolor(COLOR_PRINCIPAL)
                except Exception:
                    pass

            # Texto adicional dentro del eje (leyendas/anotaciones)
            for text in ax.texts:
                text.set_color(tema["fg"])

            leg = ax.get_legend()
            if leg is not None:
                leg.get_frame().set_facecolor(tema["bg"])
                leg.get_frame().set_edgecolor(tema["grid"])
                for t in leg.get_texts():
                    t.set_color(tema["fg"])

    salida = _resolver_carpeta(carpeta)
    salida.mkdir(parents=True, exist_ok=True)

    size_original = fig.get_size_inches().copy()

    try:
        for tema_nombre, tema in TEMAS.items():
            _aplicar_tema_y_color(fig, tema)

            for formato_nombre, (w_px, h_px) in FORMATOS_PX.items():
                w_in, h_in = (w_px / DPI), (h_px / DPI)
                fig.set_size_inches(w_in, h_in, forward=True)

                ruta = salida / f"{nombre}_{tema_nombre}_{formato_nombre}.png"
                fig.savefig(
                    ruta,
                    dpi=DPI,
                    bbox_inches=None,
                    facecolor=tema["bg"],
                    edgecolor=tema["bg"],
                )
                print(f"Exportado: {ruta}")
    finally:
        fig.set_size_inches(size_original, forward=True)


if __name__ == "__main__":
    # Ejemplo de uso:
    # Ejecuta este archivo directamente para generar 6 imágenes en ../outputs/graficos/
    import numpy as np

    x = np.linspace(0, 10, 200)
    y = np.sin(x)

    fig, ax = plt.subplots()
    ax.plot(x, y, linewidth=2)
    ax.set_title("Ejemplo exportar_grafico")
    ax.set_xlabel("x")
    ax.set_ylabel("sin(x)")

    exportar_grafico(fig, nombre="ejemplo_sin", carpeta="../outputs/graficos/")
