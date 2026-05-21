# -*- coding: utf-8 -*-
"""
=============================================================================
PRÁCTICA DE LABORATORIO – HRV Y BALANCE AUTONÓMICO
Universidad Militar Nueva Granada | Procesamiento Digital de Señales

PARTE C – Diagrama de Poincaré e índices de balance autonómico

Este script:
  1. Carga los intervalos R-R de cada segmento (generados por Parte B)
  2. Construye el diagrama de Poincaré para cada segmento
  3. Calcula SD1, SD2, T y L según Toichi et al. (1997)
  4. Obtiene CVI (índice vagal) y CSI (índice simpático)
  5. Genera gráficas comparativas de los dos diagramas

Referencia:
  Toichi M. et al. (1997). A new method of assessing cardiac autonomic
  function and its comparison with spectral analysis and coefficient of
  variation of R-R interval. J. Auton. Nerv. Syst., 62, 79-84.
=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import glob
import os
from datetime import datetime

ts = datetime.now().strftime("%Y%m%d_%H%M%S")

# =============================================================================
# PASO 1 – CARGAR INTERVALOS R-R (generados por Parte B)
#
# Parte B exporta dos archivos .npy con los arrays R-R de cada segmento.
# Si no se encuentran, se muestra un mensaje de error orientativo.
# =============================================================================
print("=" * 60)
print("  PASO 1 – CARGA DE INTERVALOS R-R")
print("=" * 60)

archivos_seg1 = sorted(glob.glob("rr_seg1_*.npy"))
archivos_seg2 = sorted(glob.glob("rr_seg2_*.npy"))

if not archivos_seg1 or not archivos_seg2:
    raise FileNotFoundError(
        "No se encontraron archivos rr_seg1_*.npy / rr_seg2_*.npy.\n"
        "Ejecuta primero la Parte B para generarlos."
    )

# Usar los más recientes
rr1 = np.load(archivos_seg1[-1])
rr2 = np.load(archivos_seg2[-1])

print(f"  Seg. 1 (reposo)  : {archivos_seg1[-1]}  →  {len(rr1)} intervalos")
print(f"  Seg. 2 (lectura) : {archivos_seg2[-1]}  →  {len(rr2)} intervalos")
print("✓ Intervalos R-R cargados")

# =============================================================================
# PASO 2 – CÁLCULO DE SD1, SD2, T, L, CVI Y CSI
#
# El diagrama de Poincaré grafica RR[n] vs RR[n+1].
# La nube de puntos tiene forma elíptica con dos ejes principales:
#
#   SD1 = std(RR[n+1] - RR[n]) / sqrt(2)
#       → dispersión perpendicular a la línea de identidad
#       → refleja variabilidad latido a latido (actividad vagal)
#
#   SD2 = sqrt(2·Var(RR) - Var(RR[n+1] - RR[n]) / 2)
#       → dispersión a lo largo de la línea de identidad
#       → refleja variabilidad a largo plazo (actividad simpática)
#
# Según Toichi et al. (1997):
#   T   = 4·SD1             (eje transversal del plot, en ms)
#   L   = 4·SD2             (eje longitudinal del plot, en ms)
#   CVI = log10(L × T)      (Cardiac Vagal Index)
#   CSI = L / T             (Cardiac Sympathetic Index)
# =============================================================================
print("\n" + "=" * 60)
print("  PASO 2 – CÁLCULO SD1, SD2, CVI, CSI")
print("=" * 60)

def poincare_indices(rr_ms, nombre):
    """
    Calcula índices autonómicos a partir del diagrama de Poincaré.

    Parámetros
    ----------
    rr_ms  : array de intervalos R-R en ms
    nombre : etiqueta del segmento (para impresión)

    Retorna
    -------
    SD1, SD2, T, L, CVI, CSI
    """
    diff  = np.diff(rr_ms)            # RR[n+1] - RR[n]

    SD1 = np.std(diff, ddof=1) / np.sqrt(2)
    SD2 = np.sqrt(np.maximum(
        2 * np.var(rr_ms, ddof=1) - (np.var(diff, ddof=1) / 2), 0
    ))

    T   = 4 * SD1
    L   = 4 * SD2
    CVI = np.log10(L * T) if (L * T) > 0 else np.nan
    CSI = L / T           if T > 0        else np.nan

    print(f"\n  [{nombre}]")
    print(f"    SD1  (eje T – vagal)     : {SD1:.4f} ms")
    print(f"    SD2  (eje L – simpático) : {SD2:.4f} ms")
    print(f"    T = 4·SD1                : {T:.4f} ms")
    print(f"    L = 4·SD2                : {L:.4f} ms")
    print(f"    CVI = log10(L×T)         : {CVI:.4f}  (↑ = mayor tono vagal)")
    print(f"    CSI = L/T                : {CSI:.4f}  (↑ = mayor tono simpático)")

    return SD1, SD2, T, L, CVI, CSI

SD1_1, SD2_1, T1, L1, CVI1, CSI1 = poincare_indices(rr1, "Segmento 1 – Reposo")
SD1_2, SD2_2, T2, L2, CVI2, CSI2 = poincare_indices(rr2, "Segmento 2 – Lectura en voz alta")

# =============================================================================
# PASO 3 – GENERACIÓN DEL DIAGRAMA DE POINCARÉ
# =============================================================================
print("\n" + "=" * 60)
print("  PASO 3 – ZOOM 20 s POR SEGMENTO")
print("=" * 60)

from scipy.signal import butter, lfilter, find_peaks

FS_     = 1000
VCC_    = 3.3
NBITS_  = 10

datos_  = np.loadtxt("ECG-4minutes.txt", comments='#')
ecg_mv_ = ((datos_[:, 5] / (2 ** NBITS_)) - 0.5) * VCC_ / 1100 * 1000
t_      = np.arange(len(ecg_mv_)) / FS_
b_, a_  = butter(4, [0.5 / 500, 40.0 / 500], btype='band')
ecg_f_  = lfilter(b_, a_, ecg_mv_)
mid_    = len(ecg_f_) // 2
s1_     = ecg_f_[:mid_];  t1_ = t_[:mid_]
s2_     = ecg_f_[mid_:];  t2_ = t_[mid_:]

def _picos(seg):
    p, _ = find_peaks(seg, height=0.5 * seg.max(), distance=400)
    return p

p1_ = _picos(s1_);  p2_ = _picos(s2_)
N20 = 20 * FS_

fig_z, ax_z = plt.subplots(2, 1, figsize=(14, 6))
fig_z.suptitle("Zoom 20 s por segmento – Intervalos R-R detectados",
               fontsize=13, fontweight='bold')

for ax, seg, picos, t_b, titulo, color in [
    (ax_z[0], s1_, p1_, t1_, "Segmento 1 – Reposo (primeros 20 s)",             '#1565C0'),
    (ax_z[1], s2_, p2_, t2_, "Segmento 2 – Lectura en voz alta (primeros 20 s)", '#2E7D32')
]:
    mask = picos < N20
    ax.plot(t_b[:N20], seg[:N20], color=color, lw=0.6, label='ECG filtrada')
    ax.plot(t_b[picos[mask]], seg[picos[mask]],
            'rv', markersize=6, label=f'Picos R ({mask.sum()} en 20 s)')
    pz = picos[mask]
    for i in range(min(4, len(pz) - 1)):
        xm = (t_b[pz[i]] + t_b[pz[i+1]]) / 2
        ym = seg[pz[i]] * 0.55
        rr = (pz[i+1] - pz[i]) / FS_ * 1000
        ax.annotate(f'{rr:.0f} ms', xy=(xm, ym), fontsize=7,
                    ha='center', bbox=dict(boxstyle='round,pad=0.2',
                    facecolor='white', edgecolor='gray', alpha=0.7))
    ax.set_title(titulo, fontsize=10)
    ax.set_ylabel("Amplitud (mV)", fontsize=9)
    ax.set_xlabel("Tiempo (s)", fontsize=9)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f"C0_zoom_20s_{ts}.png", dpi=150, bbox_inches='tight')
plt.show()
print("✓ Zoom 20 s generado")

print("\n" + "=" * 60)
print("  PASO 4 – GENERANDO DIAGRAMA DE POINCARÉ")
print("=" * 60)

def dibujar_poincare(ax, rr_ms, SD1, SD2, CVI, CSI, titulo, color):
    """
    Dibuja el diagrama de Poincaré en el eje dado con la elipse SD1/SD2
    y anota los índices CVI y CSI.
    """
    # Nube de puntos
    ax.scatter(rr_ms[:-1], rr_ms[1:],
               color=color, alpha=0.45, s=14, edgecolors='none',
               label='Puntos RR[n] vs RR[n+1]')

    # Línea de identidad RR[n] = RR[n+1]
    lim_min = min(rr_ms) * 0.94
    lim_max = max(rr_ms) * 1.06
    ax.plot([lim_min, lim_max], [lim_min, lim_max],
            'k--', lw=1, alpha=0.45, label='Identidad (45°)')

    # Elipse SD1 / SD2 centrada en la media R-R
    mu   = np.mean(rr_ms)
    theta = np.linspace(0, 2 * np.pi, 300)
    ang   = np.pi / 4                     # 45° → alinea con la identidad
    ex = (mu + SD2 * np.cos(theta) * np.cos(ang)
             - SD1 * np.sin(theta) * np.sin(ang))
    ey = (mu + SD2 * np.cos(theta) * np.sin(ang)
             + SD1 * np.sin(theta) * np.cos(ang))
    ax.plot(ex, ey, '-', color='red', lw=1.6, alpha=0.85, label='Elipse SD1/SD2')

    # Anotación de ejes de la elipse
    # Eje SD1 (perpendicular a identidad)
    ax.annotate('', xy=(mu + SD1 * np.cos(ang + np.pi/2),
                         mu + SD1 * np.sin(ang + np.pi/2)),
                xytext=(mu, mu),
                arrowprops=dict(arrowstyle='->', color='#C62828', lw=1.2))
    ax.text(mu + SD1 * np.cos(ang + np.pi/2) + 4,
            mu + SD1 * np.sin(ang + np.pi/2),
            f'SD1={SD1:.1f} ms', fontsize=8, color='#C62828')

    # Eje SD2 (a lo largo de identidad)
    ax.annotate('', xy=(mu + SD2 * np.cos(ang),
                         mu + SD2 * np.sin(ang)),
                xytext=(mu, mu),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1.2))
    ax.text(mu + SD2 * np.cos(ang) + 4,
            mu + SD2 * np.sin(ang),
            f'SD2={SD2:.1f} ms', fontsize=8, color='#1565C0')

    # Índices en recuadro
    ax.text(0.03, 0.97,
            f"CVI = {CVI:.3f}\nCSI = {CSI:.3f}",
            transform=ax.transAxes, fontsize=9, va='top',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                      edgecolor='gray', alpha=0.8))

    ax.set_title(titulo, fontsize=10)
    ax.set_xlabel("RR[n] (ms)", fontsize=9)
    ax.set_ylabel("RR[n+1] (ms)", fontsize=9)
    ax.legend(fontsize=8, loc='lower right')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal', adjustable='datalim')

fig4, axes4 = plt.subplots(1, 2, figsize=(14, 6))
fig4.suptitle("Diagrama de Poincaré – RR[n] vs RR[n+1]",
              fontsize=13, fontweight='bold')

dibujar_poincare(
    axes4[0], rr1, SD1_1, SD2_1, CVI1, CSI1,
    f"Segmento 1 – Reposo\nCVI={CVI1:.3f}  |  CSI={CSI1:.3f}",
    '#1565C0'
)
dibujar_poincare(
    axes4[1], rr2, SD1_2, SD2_2, CVI2, CSI2,
    f"Segmento 2 – Lectura en voz alta\nCVI={CVI2:.3f}  |  CSI={CSI2:.3f}",
    '#2E7D32'
)

plt.tight_layout()
plt.savefig(f"C1_poincare_{ts}.png", dpi=150, bbox_inches='tight')
plt.show()



# =============================================================================
# RESUMEN FINAL PARTE C
# =============================================================================
print("\n" + "=" * 60)
print("  RESUMEN COMPARATIVO PARTE C")
print("=" * 60)
print(f"  {'Parámetro':<22} {'Seg. 1 – Reposo':>18} {'Seg. 2 – Lectura':>18}")
print("-" * 60)
print(f"  {'SD1 (ms)':<22} {SD1_1:>18.4f} {SD1_2:>18.4f}")
print(f"  {'SD2 (ms)':<22} {SD2_1:>18.4f} {SD2_2:>18.4f}")
print(f"  {'T = 4·SD1 (ms)':<22} {T1:>18.4f} {T2:>18.4f}")
print(f"  {'L = 4·SD2 (ms)':<22} {L1:>18.4f} {L2:>18.4f}")
print(f"  {'CVI':<22} {CVI1:>18.4f} {CVI2:>18.4f}")
print(f"  {'CSI':<22} {CSI1:>18.4f} {CSI2:>18.4f}")
print("=" * 60)

# Interpretación automática
print("\n  Interpretación:")
if CVI2 > CVI1:
    print("  • CVI ↑ en lectura: mayor actividad vagal (o mixta).")
else:
    print("  • CVI ↓ en lectura: reducción del tono vagal (parasimpático).")
if CSI2 > CSI1:
    print("  • CSI ↑ en lectura: mayor actividad simpática.")
else:
    print("  • CSI ↓ en lectura: reducción del tono simpático.")

print("\n✓ Parte C finalizada. Gráficas guardadas.")