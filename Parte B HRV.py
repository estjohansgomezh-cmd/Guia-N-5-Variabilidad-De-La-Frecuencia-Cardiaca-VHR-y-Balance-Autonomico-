# -*- coding: utf-8 -*-
"""
=============================================================================
PRÁCTICA DE LABORATORIO – HRV Y BALANCE AUTONÓMICO
Universidad Militar Nueva Granada | Procesamiento Digital de Señales

PARTE B – Pre-procesamiento y análisis HRV en el dominio del tiempo

Este script:
  1. Lee la señal ECG desde archivo BITalino (.txt)
  2. Convierte de ADC a mV
  3. Diseña e implementa filtro IIR Butterworth pasabanda
  4. Divide la señal en dos segmentos de 2 minutos
  5. Detecta picos R y calcula intervalos R-R
  6. Calcula parámetros HRV en el dominio del tiempo (media, SDNN, FC)
  7. Genera gráficas: ECG original vs filtrada, detección de picos R, taquograma
=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, find_peaks
from datetime import datetime

# =============================================================================
# PARÁMETROS GLOBALES
# =============================================================================
ARCHIVO  = "ECG-4minutes.txt"   # archivo OpenSignals BITalino
FS       = 1000                  # frecuencia de muestreo [Hz]
VCC      = 3.3                   # tensión de alimentación BITalino [V]
N_BITS   = 10                    # resolución ADC [bits]
ts       = datetime.now().strftime("%Y%m%d_%H%M%S")

# =============================================================================
# PASO 1 – LECTURA DEL ARCHIVO BITALINO (formato OpenSignals)
#
# Estructura del archivo:
#   Líneas 1-3: encabezado con '#'
#   Columnas  : nSeq | I1 | I2 | O1 | O2 | A1(ECG)
#   Canal ECG : columna índice 5 (A1), resolución 10 bits
# =============================================================================
print("=" * 60)
print("  PASO 1 – LECTURA DE SEÑAL ECG (BITalino)")
print("=" * 60)

datos = np.loadtxt(ARCHIVO, comments='#')

# Columna 5 → canal ECG (valor ADC 10 bits)
adc = datos[:, 5]

# Conversión ADC → mV según datasheet BITalino (sensor ECGBIT, G = 1100)
# ECG_mV = ((ADC / 2^n) - 0.5) × VCC / G × 1000
ecg_mv = ((adc / (2 ** N_BITS)) - 0.5) * VCC / 1100 * 1000

# Vector de tiempo
n_muestras = len(ecg_mv)
t = np.arange(n_muestras) / FS       # [s]

print(f"  Archivo         : {ARCHIVO}")
print(f"  Fs              : {FS} Hz  |  Nyquist: {FS//2} Hz")
print(f"  Muestras        : {n_muestras}")
print(f"  Duración real   : {t[-1]:.2f} s")
print(f"  ECG rango       : {ecg_mv.min():.4f} – {ecg_mv.max():.4f} mV")
print("✓ Señal cargada y convertida a mV")

# =============================================================================
# PASO 2 – DISEÑO E IMPLEMENTACIÓN DEL FILTRO IIR BUTTERWORTH PASABANDA
#
# Justificación de parámetros:
#   Banda útil del ECG para detección QRS: 0.5 – 40 Hz
#     • Corte inferior 0.5 Hz: elimina deriva de línea base (respiración,
#       movimiento de electrodos) sin distorsionar la onda P.
#     • Corte superior 40 Hz: elimina ruido EMG y de red (50/60 Hz) sin
#       recortar la energía del complejo QRS (5–20 Hz principal).
#   Orden 4: buen compromiso entre pendiente de atenuación y estabilidad.
#   Implementación con condiciones iniciales en 0 (lfilter, zi=0 por defecto).
# =============================================================================
print("\n" + "=" * 60)
print("  PASO 2 – DISEÑO E IMPLEMENTACIÓN FILTRO IIR BUTTERWORTH")
print("=" * 60)

F_LOW  = 0.5    # Hz – frecuencia de corte inferior
F_HIGH = 40.0   # Hz – frecuencia de corte superior
ORDEN  = 4

# Frecuencias normalizadas respecto a Nyquist
fn_low  = F_LOW  / (FS / 2)
fn_high = F_HIGH / (FS / 2)

# Diseño del filtro → coeficientes b (numerador) y a (denominador)
b, a = butter(ORDEN, [fn_low, fn_high], btype='band')

print(f"  Tipo            : Butterworth pasabanda, orden {ORDEN}")
print(f"  Banda de paso   : {F_LOW} – {F_HIGH} Hz")
print(f"  Nyquist         : {FS // 2} Hz")
print(f"  fn normalizada  : {fn_low:.5f} – {fn_high:.5f}")
print(f"\n  Coeficientes b  : {np.round(b, 6)}")
print(f"  Coeficientes a  : {np.round(a, 6)}")

# Ecuación en diferencias (forma directa I)
print("\n  Ecuación en diferencias (condiciones iniciales = 0):")
b_terms = " + ".join([
    f"{b[i]:.6f}·x[n]" if i == 0 else f"{b[i]:.6f}·x[n-{i}]"
    for i in range(len(b)) if round(b[i], 8) != 0
])
a_terms = " - ".join([
    f"{a[i]:.6f}·y[n-{i}]"
    for i in range(1, len(a))
])
print(f"  y[n] = {b_terms}")
print(f"         - {a_terms}")

# Aplicar filtro (zi = 0 implícito en lfilter)
ecg_filt = lfilter(b, a, ecg_mv)
print("\n✓ Filtro aplicado con condiciones iniciales = 0")

# =============================================================================
# PASO 3 – DIVISIÓN EN DOS SEGMENTOS DE 2 MINUTOS
# =============================================================================
print("\n" + "=" * 60)
print("  PASO 3 – DIVISIÓN EN SEGMENTOS")
print("=" * 60)

mid      = n_muestras // 2
seg1_ecg = ecg_filt[:mid]       # Segmento 1: reposo (0 – 2 min)
seg2_ecg = ecg_filt[mid:]       # Segmento 2: lectura en voz alta (2 – 4 min)
t1       = t[:mid]
t2       = t[mid:]

print(f"  Segmento 1 – Reposo   : 0 – {t1[-1]:.1f} s  ({len(seg1_ecg)} muestras)")
print(f"  Segmento 2 – Lectura  : {t2[0]:.1f} – {t2[-1]:.1f} s  ({len(seg2_ecg)} muestras)")

# =============================================================================
# PASO 4 – DETECCIÓN DE PICOS R E INTERVALOS R-R
#
# Se usa scipy.signal.find_peaks con:
#   height   : umbral = 50% del máximo del segmento (adapta a la amplitud)
#   distance : distancia mínima entre picos = 400 ms (FC máx ~150 lpm)
# El intervalo R-R se obtiene dividiendo la diferencia de muestras entre Fs.
# =============================================================================
print("\n" + "=" * 60)
print("  PASO 4 – DETECCIÓN DE PICOS R Y CÁLCULO R-R")
print("=" * 60)

def detectar_picos_rr(segmento, fs, umbral_rel=0.5, dist_min_ms=400):
    """
    Detecta picos R en un segmento de ECG filtrado y calcula intervalos R-R.

    Parámetros
    ----------
    segmento    : array ECG filtrado
    fs          : frecuencia de muestreo [Hz]
    umbral_rel  : fracción del máximo como umbral de altura
    dist_min_ms : distancia mínima entre picos [ms]

    Retorna
    -------
    picos : índices de los picos R detectados
    rr_ms : intervalos R-R en milisegundos
    """
    umbral   = umbral_rel * segmento.max()
    dist_mue = int(dist_min_ms / 1000 * fs)
    picos, _ = find_peaks(segmento, height=umbral, distance=dist_mue)
    rr_ms    = np.diff(picos) / fs * 1000   # diferencia de muestras → ms
    return picos, rr_ms

picos1, rr1 = detectar_picos_rr(seg1_ecg, FS)
picos2, rr2 = detectar_picos_rr(seg2_ecg, FS)

print(f"  Segmento 1 → {len(picos1)} picos R  |  {len(rr1)} intervalos R-R")
print(f"  Segmento 2 → {len(picos2)} picos R  |  {len(rr2)} intervalos R-R")

# =============================================================================
# PASO 5 – ANÁLISIS HRV EN EL DOMINIO DEL TIEMPO
# =============================================================================
print("\n" + "=" * 60)
print("  PASO 5 – ANÁLISIS HRV DOMINIO DEL TIEMPO")
print("=" * 60)

def hrv_tiempo(rr_ms, nombre):
    """
    Calcula y muestra los parámetros básicos de HRV en el dominio del tiempo.

    Parámetros
    ----------
    media R-R : promedio de los intervalos R-R
    SDNN      : desviación estándar de los intervalos R-R
    FC media  : frecuencia cardíaca media = 60000 / media_RR [lpm]
    """
    media = np.mean(rr_ms)
    sdnn  = np.std(rr_ms, ddof=1)
    fc    = 60000 / media
    print(f"\n  [{nombre}]")
    print(f"    Media R-R   : {media:.2f} ms")
    print(f"    SDNN        : {sdnn:.2f} ms")
    print(f"    FC media    : {fc:.1f} lpm")
    return media, sdnn, fc

media1, sdnn1, fc1 = hrv_tiempo(rr1, "Segmento 1 – Reposo")
media2, sdnn2, fc2 = hrv_tiempo(rr2, "Segmento 2 – Lectura en voz alta")

print(f"\n  Comparación entre segmentos:")
print(f"    ΔMedia R-R  : {media2 - media1:+.2f} ms")
print(f"    ΔSDNN       : {sdnn2 - sdnn1:+.2f} ms")
print(f"    ΔFC         : {fc2 - fc1:+.1f} lpm")

# =============================================================================
# PASO 6 – GRÁFICAS PARTE B
# =============================================================================
print("\n" + "=" * 60)
print("  PASO 6 – GENERANDO GRÁFICAS")
print("=" * 60)

# ── Gráfica 1: Señal COMPLETA original vs filtrada (4 min) ───────────────────
fig1, axes = plt.subplots(2, 1, figsize=(16, 7), sharex=True)
fig1.suptitle("Señal ECG completa – Original vs Filtrada (4 minutos)",
              fontsize=13, fontweight='bold')

t_mid = t[mid]   # tiempo en segundos donde cambia el segmento

axes[0].plot(t, ecg_mv, color='#B71C1C', lw=0.4, label='ECG original')
axes[0].axvline(t_mid, color='black', ls='--', lw=1.2, label=f'Cambio de condición ({t_mid:.0f} s)')
axes[0].axvspan(0,     t_mid, alpha=0.05, color='blue',  label='Reposo')
axes[0].axvspan(t_mid, t[-1], alpha=0.05, color='green', label='Lectura en voz alta')
axes[0].set_ylabel("Amplitud (mV)", fontsize=10)
axes[0].set_title("Señal sin filtrar", fontsize=10)
axes[0].legend(fontsize=8, loc='upper right')
axes[0].grid(True, alpha=0.3)

axes[1].plot(t, ecg_filt, color='#1565C0', lw=0.4, label='ECG filtrada')
axes[1].axvline(t_mid, color='black', ls='--', lw=1.2, label=f'Cambio de condición ({t_mid:.0f} s)')
axes[1].axvspan(0,     t_mid, alpha=0.05, color='blue',  label='Reposo')
axes[1].axvspan(t_mid, t[-1], alpha=0.05, color='green', label='Lectura en voz alta')
axes[1].set_ylabel("Amplitud (mV)", fontsize=10)
axes[1].set_xlabel("Tiempo (s)", fontsize=10)
axes[1].set_title(
    f"Filtro Butterworth pasabanda orden {ORDEN} [{F_LOW}–{F_HIGH} Hz]", fontsize=10)
axes[1].legend(fontsize=8, loc='upper right')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f"B1_ecg_completa_{ts}.png", dpi=150, bbox_inches='tight')
plt.show()

# ── Gráfica 1b: Zoom 10 s para verificar efecto del filtro ───────────────────
fig1b, axes1b = plt.subplots(2, 1, figsize=(14, 5), sharex=True)
fig1b.suptitle("Verificación del filtro – Zoom primeros 10 s",
               fontsize=12, fontweight='bold')

n10 = 10 * FS
axes1b[0].plot(t[:n10], ecg_mv[:n10],   color='#B71C1C', lw=0.7, label='Original')
axes1b[0].set_ylabel("Amplitud (mV)", fontsize=10)
axes1b[0].set_title("Sin filtrar", fontsize=10)
axes1b[0].legend(fontsize=9)
axes1b[0].grid(True, alpha=0.3)

axes1b[1].plot(t[:n10], ecg_filt[:n10], color='#1565C0', lw=0.7, label='Filtrada')
axes1b[1].set_ylabel("Amplitud (mV)", fontsize=10)
axes1b[1].set_xlabel("Tiempo (s)", fontsize=10)
axes1b[1].set_title("Filtrada – Butterworth pasabanda", fontsize=10)
axes1b[1].legend(fontsize=9)
axes1b[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f"B1b_zoom_filtro_{ts}.png", dpi=150, bbox_inches='tight')
plt.show()

# ── Gráfica 2: Detección de picos R – segmento completo (2 min) ──────────────
fig2, axes2 = plt.subplots(2, 1, figsize=(16, 7))
fig2.suptitle("Detección de Picos R – Segmento completo (2 minutos)",
              fontsize=13, fontweight='bold')

for ax, seg, picos, t_base, titulo, color in [
    (axes2[0], seg1_ecg, picos1, t1, "Segmento 1 – Reposo (0 – 2 min)",          '#1565C0'),
    (axes2[1], seg2_ecg, picos2, t2, "Segmento 2 – Lectura en voz alta (2 – 4 min)", '#2E7D32')
]:
    ax.plot(t_base, seg, color=color, lw=0.4, label='ECG filtrada')
    ax.plot(t_base[picos], seg[picos],
            'rv', markersize=5, label=f'Picos R ({len(picos)} detectados)')
    ax.set_title(titulo, fontsize=10)
    ax.set_ylabel("Amplitud (mV)", fontsize=9)
    ax.set_xlabel("Tiempo (s)", fontsize=9)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f"B2_picos_R_{ts}.png", dpi=150, bbox_inches='tight')
plt.show()



# =============================================================================
# RESUMEN PARTE B
# =============================================================================
print("\n" + "=" * 60)
print("  RESUMEN PARTE B")
print("=" * 60)
print(f"  {'Parámetro':<20} {'Seg. 1 – Reposo':>18} {'Seg. 2 – Lectura':>18}")
print("-" * 58)
print(f"  {'Picos R detectados':<20} {len(picos1):>18} {len(picos2):>18}")
print(f"  {'Intervalos R-R':<20} {len(rr1):>18} {len(rr2):>18}")
print(f"  {'Media R-R (ms)':<20} {media1:>18.2f} {media2:>18.2f}")
print(f"  {'SDNN (ms)':<20} {sdnn1:>18.2f} {sdnn2:>18.2f}")
print(f"  {'FC media (lpm)':<20} {fc1:>18.1f} {fc2:>18.1f}")
print("=" * 60)
print("\n✓ Parte B finalizada. Gráficas guardadas.")

# Exportar arrays R-R para usar en Parte C
np.save(f"rr_seg1_{ts}.npy", rr1)
np.save(f"rr_seg2_{ts}.npy", rr2)
print(f"  Arrays R-R guardados: rr_seg1_{ts}.npy  |  rr_seg2_{ts}.npy")