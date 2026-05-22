
#  Práctica de Laboratorio N° 5: Variabilidad de la frecuencia cardiaca VHR y Balance Autonomico
Universidad Militar Nueva Granada — Ingeniería Biomédica — Procesamiento Digital de Señales
---
## Descripción

Esta práctica tiene como objetivo identificar cambios en el balance autonómico mediante el análisis temporal de la variabilidad de la frecuencia cardíaca (HRV). A partir de una señal ECG adquirida con el dispositivo BITalino durante dos condiciones distintas —reposo en silencio y lectura en voz alta— se aplica un pipeline completo de procesamiento digital de señales que incluye: filtrado IIR, detección de picos R, cálculo de intervalos R-R, análisis estadístico en el dominio del tiempo y construcción del diagrama de Poincaré con sus índices autonómicos (CVI y CSI).

Los resultados permiten relacionar los cambios en la variabilidad R-R con la activación del sistema nervioso simpático y parasimpático ante actividades que implican verbalización.

## Metodología

Para el desarrollo de esta guía se dispusieron de tres partes: 

Parte A (Fundamento teórico y planeación): Se investigan los conceptos del sistema nervioso autónomo, el efecto de cada rama sobre la frecuencia cardíaca, la HRV y el diagrama de Poincaré. Se formula el diagrama de flujo que guía el procesamiento.

Parte B  (Adquisición, filtrado y análisis temporal): Se adquiere la señal ECG (4 minutos, Fs = 1000 Hz) con el dispositivo BITalino. Se diseña e implementa un filtro IIR Butterworth pasabanda. Se segmenta la señal, se detectan los picos R, se calculan los intervalos R-R y se obtienen los parámetros estadísticos básicos de HRV (media R-R y SDNN) para cada segmento.

Parte C (Análisis no lineal con el diagrama de Poincaré): Se construye el diagrama de Poincaré para cada segmento, se calculan SD1, SD2 y los índices autonómicos CVI y CSI definidos por Toichi et al. (1997), y se compara el balance simpático/parasimpático entre condiciones.

## PARTE A
### a. FUNDAMENTO TEÓRICO

**1).** Actividad simpática y parasimpática del sistema nervioso autónomo.
- R/:
 
  El SNA regula funciones involuntarias del organismo a través de dos ramas antagónicas:
  
   - **Rama simpática:** se activa ante situaciones de estrés, esfuerzo o alerta. Libera noradrenalina, lo que aumenta la frecuencia cardíaca (efecto cronotrópico positivo) y reduce la variabilidad R-R.
  
   - **Rama parasimpática (vagal):** predomina en reposo. Libera acetilcolina a través del nervio vago, disminuyendo la frecuencia cardíaca y aumentando la variabilidad R-R.}
         
El balance entre ambas ramas determina el estado autonómico del sujeto en cada momento.

**2).** Efecto de la actividad simpática y parasimpática en la frecuencia cardíaca.
- R/:

| CONDICION | RAMA DOMINANTE | FRCUENCIA CARDIACA | INTERVALO R-R | VARIABILIDAD |
| :---: | :---: | :---: | :---: | :---: |
| En resposo, en este caso sin hablar | parasimpatico | disminuye | es largo | es alta la variabilidad |
| en estres, en este caso cuando se habla en voz alta | simpatico | aumenta | es corto | es baja la variabilidad |

La verbalización (al momento de hablar) activa el sistema simpático porque implica esfuerzo cognitivo, control motor del habla y mayor demanda de oxígeno.

**3).** Variabilidad de la frecuencia cardíaca (HRV) obtenida a partir de la señal electrocardiográfica (ECG).
- R/:

La HRV es la fluctuación en la duración de los intervalos entre latidos consecutivos (intervalos R-R), medidos desde la señal ECG. No es ruido: es información fisiológica sobre el balance autonómico.

Parámetros en el dominio del tiempo:

   - **Media R-R:** valor promedio de los intervalos. Inversamente proporcional a la FC.

   - **SDNN:** desviación estándar de los intervalos R-R. Refleja la variabilidad total; valores altos indican buen tono vagal. 

**4).** Diagrama de Poincaré como herramienta de análisis de la serie R-R.
- R/:

El diagrama de Poincaré es una herramienta no lineal que grafica cada intervalo R-R[n] contra el siguiente R-R[n+1]. La nube de puntos resultante forma una elipse cuyos ejes revelan el balance autonómico:

   - **SD1 (eje transversal, T):** dispersión perpendicular a la línea de identidad. Refleja la variabilidad latido a latido → actividad vagal (parasimpática).
   - **SD2 (eje longitudinal, L):** dispersión a lo largo de la línea de identidad. Refleja la variabilidad a largo plazo → actividad simpática.

Según Toichi et al. (1997), los índices autonómicos se definen como:
T = 4 · SD1          (eje transversal)
L = 4 · SD2          (eje longitudinal)

CVI = log₁₀(L × T)    --> Cardiac Vagal Index    (↑ = mayor tono parasimpatico)

CSI = L / T           --> Cardiac Sympathetic Index (↑ = mayor tono simpatico)

Visualmente: una elipse más ancha y grande indica mayor tono vagal (reposo); una elipse más larga y estrecha indica mayor tono simpático (estrés/lectura).
 

**5).** Variabilidad de la frecuencia cardíaca (HRV) y balance autonómico.
- R/:
1. Sistema Nervioso Autónomo (SNA)
El SNA es la división del sistema nervioso que regula funciones involuntarias del organismo (frecuencia cardíaca, presión arterial, digestión, respiración). Se divide en dos ramas antagónicas:

**Rama simpática:**

- Se activa ante situaciones de estrés, esfuerzo físico o alerta
- Libera noradrenalina en el nodo sinusal
- Efecto: aumenta la FC, acorta los intervalos R-R, reduce la HRV
- Ejemplo: hablar en público, ejercicio, susto

**Rama parasimpática (vagal):**

- Predomina en reposo y relajación
- Actúa a través del nervio vago, liberando acetilcolina
- Efecto: disminuye la FC, alarga los intervalos R-R, aumenta la HRV
- Ejemplo: reposo, sueño, meditación

El balance entre ambas ramas en cada momento determina el estado autonómico del sujeto.

### DIAGRAMA DE FLUJO

<img width="800" height="1200" alt="diagrama_flujo_hrv" src="https://github.com/user-attachments/assets/44155369-c0dd-41e7-a8e3-9c9d4169e38f" />


### b. ADQUISICION DE LA SEÑAL ECG
<img width="467" height="336" alt="image" src="https://github.com/user-attachments/assets/c0cbc64e-214b-48eb-912c-cf329cd1996c" />

Se utilizó esta analogía y la correcta ubicación de los electrodos para obtener la señal de ECG mediante el dispositivo BITalino. A partir de esta configuración, se realizó la adquisición de aproximadamente cuatro minutos de señal cardíaca continua, permitiendo registrar de manera adecuada la actividad eléctrica del corazón. Durante los primeros dos minutos, la persona se mantuvo en estado de reposo y silencio, con el fin de obtener una señal estable y con la menor cantidad posible de interferencias. Posteriormente, en los dos minutos restantes, la medición se realizó en un estado de excitación, hablando en voz alta, para observar los posibles cambios y variaciones presentes en la señal de ECG bajo diferentes condiciones. Finalmente, la señal obtenida fue utilizada para llevar a cabo el análisis correspondiente del comportamiento cardíaco durante ambas situaciones.

<img width="600" height="350" alt="image" src="https://github.com/user-attachments/assets/9ec62e97-c4d3-44d4-a009-cb2f5670ba3f" />

Además, al realizar el análisis de la señal obtenida, se evidenció que la variación observada presentaba un comportamiento similar al de la derivación V3 del ECG, ya que la forma y características de la señal mostraban una mayor semejanza con este tipo de derivación precordial. Esta variación permitió visualizar de manera más clara algunos cambios en la actividad eléctrica cardíaca durante las diferentes condiciones de medición.

| PARAMETRO | VALOR | 
| :---: | :---: |
| Archivo | ECG-4minutes.txt |
| Fs | 1000 Hz |
| Nyquist |  500 Hz |
| Muestras totales | 240 900 |
| Duración real | 240.90 s |
| Rango ECG | −1.0840 a +0.9434 mV | 

## PARTE B
### c. PRE-PROCESAMINETO DE LA SEÑAL

#### Diseño del Filtro IIR Butterworth

Se diseñó un filtro IIR Butterworth pasabanda de orden 4 con banda de paso de 0.5 a 40 Hz, adecuado para retener el contenido espectral del ECG (complejo QRS: 5–40 Hz) y eliminar la línea base (< 0.5 Hz) y el ruido de alta frecuencia (> 40 Hz).

| PARAMETRO | VALOR | 
| :---: | :---: |
| Tipo | Butterworth pasabanda |
| Orden | 4 |
| f_low |  0.5 Hz |
| f_high | 40.0 Hz |
| Fs | 1000 Hz |
| fn normalizada | 0.0010 – 0.0800 |

#### Coeficientes del numerador (b):

b = [ 0.000175,  0.000000, -0.000699,  0.000000,  0.001049,
      0.000000, -0.000699,  0.000000,  0.000175 ]

#### Coeficientes del denominador (a):

a = [  1.000000, -7.349330,  23.651252, -43.535013,  50.135939,
      -36.992094, 17.077925,  -4.510463,   0.521783 ]

#### Ecuación en Diferencias

Aplicando la definición de filtro IIR con condiciones iniciales iguales a cero:

y[n] =   0.000175·x[n]
       - 0.000699·x[n-2]
       + 0.001049·x[n-4]
       - 0.000699·x[n-6]
       + 0.000175·x[n-8]
       + 7.349330·y[n-1]
       - 23.651252·y[n-2]
       + 43.535013·y[n-3]
       - 50.135939·y[n-4]
       + 36.992094·y[n-5]
       - 17.077925·y[n-6]
       + 4.510463·y[n-7]
       - 0.521783·y[n-8]
       
Las condiciones iniciales se asumen iguales a cero: y[-1] = y[-2] = ... = x[-1] = x[-2] = ... = 0

Donde:

- x[n] = muestra actual de la señal ECG sin filtrar (entrada)
- x[n-k] = muestras pasadas de la entrada → vienen de los coeficientes b
- y[n] = muestra actual de la señal filtrada (salida)
- y[n-k] = muestras pasadas de la salida → vienen de los coeficientes a (la parte "recursiva" que hace al filtro IIR)

Lo que significa que antes de empezar a filtrar, se asume que no había señal.

En pocas palabras: cada muestra filtrada depende de 8 muestras anteriores de entrada y 8 de salida. Eso es lo que lo hace IIR (respuesta infinita al impulso): la salida se retroalimenta a sí misma.

#### Segmentación y Detección de Picos R

Tras aplicar el filtro, la señal se dividió en dos segmentos de 2 minutos cada uno:

| SEGMENTO | CONDICION | TIEMPO | MUESTRAS | PICOS R | INTERVALOS R-R |
| :---: | :---: |  :---: |  :---: |  :---: |  :---: |
| Segmento 1 | Reposo | 0 – 120.4 s | 120 450 | 155 | 154 |
| Segmento 2 | Lectura en voz alta | 120.5 – 240.9 s | 120 450 | 181 | 180 |


<img width="2385" height="1036" alt="B1_ecg_completa_20260521_162836" src="https://github.com/user-attachments/assets/7cd7285e-4e97-4194-93a3-dfeb8faa251b" />
<img width="2085" height="742" alt="B1b_zoom_filtro_20260521_162836" src="https://github.com/user-attachments/assets/f4eff06c-b366-4d70-a175-816d597ac6c7" />
<img width="2372" height="1036" alt="B2_picos_R_20260521_162836" src="https://github.com/user-attachments/assets/3913f204-c857-42d0-8ca2-fd2b731da7d4" />


### d. ANALISIS DE LA HRV EN EL DOMINIO DEL TIEMPO

Los parámetros estadísticos de la serie R-R para cada segmento son:

#### Fórmulas utilizadas:

Media R-R = (1/N) · Σ RR[i]           (i = 1 … N)

SDNN = sqrt( (1/(N-1)) · Σ (RR[i] - Media_RR)² )

FC media (lpm) = 60 000 / Media_RR (ms)

#### Resultados:

| PARAMETRO | SEGMENTO 1-REPOSO | SEGMENTO 2-LECTURA | Δ |
| :---: | :---: |  :---: |  :---: |
| Picos R detectados | 155 | 181 | +26 | 
| Intervalos R-R | 154 | 180 | +26 | 
| Media R-R (ms) | 779.47 | 662.31 | −117.16 |
| SDNN (ms) | 49.55 | 63.49 | +13.94 |
| FC media (lpm) | 77.0 | 90.6 | +13.6 |

#### Interpretación:

La media R-R disminuyó 117 ms en la lectura, lo que refleja un aumento de la frecuencia cardíaca (+13.6 lpm), consistente con la activación del sistema simpático durante la verbalización.

El SDNN aumentó en la lectura (+13.94 ms), lo que puede parecer contraintuitivo; sin embargo, en condiciones de habla activa puede deberse a la arritmia sinusal respiratoria acentuada por los patrones respiratorios irregulares del habla, que incrementan momentáneamente la variabilidad latido a latido a pesar del tono simpático predominante.

## PARTE C
### e. CONSTRUCCION DEL DIAGRAMA DE PIONCARÉ

El diagrama de Poincaré se construye graficando cada intervalo RR[n] en el eje X contra el intervalo siguiente RR[n+1] en el eje Y. La nube de puntos resultante tiene forma elíptica y sus ejes se calculan como:

#### Fórmulas SD1 y SD2:

SD1 = sqrt( (1/2) · Var(RR[n+1] - RR[n]) )
    = sqrt( (1/2) · std(diff(RR))² )

SD2 = sqrt( 2·Var(RR) - (1/2)·Var(diff(RR)) )
    = sqrt( 2·SDNN² - SD1² )

#### Índices de Toichi et al. (1997):

T   = 4 · SD1          [ms]   → eje transversal (vagal)
L   = 4 · SD2          [ms]   → eje longitudinal (simpático)

CVI = log₁₀(L × T)            → Cardiac Vagal Index
CSI = L / T                    → Cardiac Sympathetic Index

<img width="2091" height="889" alt="C1_poincare_20260521_163922" src="https://github.com/user-attachments/assets/d6664b97-6bad-453a-91ee-e5f0b1a940d3" />
<img width="2085" height="889" alt="C0_zoom_20s_20260521_163922" src="https://github.com/user-attachments/assets/c013cbc7-5800-4144-a5a6-e8f65fdb077c" />

#### Resultados: 

| PARAMETRO | SEGMENTO 1-REPOSO | SEGMENTO 2-LECTURA |
| :---: | :---: |  :---: |
| SD1 – eje T vagal (ms) | 25.2071 | 59.5431 |
| SD2 – eje L simpático (ms) | 65.3880 | 67.2049 |
| T = 4·SD1 (ms) | 100.8285 | 238.1726 |
| L = 4·SD2 (ms) | 261.5518 | 268.8194 |
| CVI = log₁₀(L×T) | 4.4211 | 4.8064 |
| CSI = L/T |2.5940 | 1.1287 |

#### Interpretación de los índices:

SD1 se duplicó en la lectura (25.2 → 59.5 ms): la variabilidad latido a latido aumentó considerablemente, lo que coincide con la irregularidad respiratoria característica del habla (arritmia sinusal respiratoria).

SD2 permaneció casi igual (65.4 → 67.2 ms): la variabilidad a largo plazo no cambió de forma significativa.

CVI aumentó (4.42 → 4.81): el índice vagal es mayor durante la lectura, impulsado por el incremento de SD1. Esto refleja que el habla genera un componente de modulación vagal rítmica asociada a la respiración, a pesar del incremento en la FC.

CSI disminuyó (2.59 → 1.13): el índice simpático se redujo a la mitad, porque aunque la FC aumentó, la nube de Poincaré se hizo más redonda (SD1 ↑ mientras SD2 apenas varió), haciendo que la relación L/T se acerque a 1.

### Resultados Esperados — Discusión:

Los cambios observados en los intervalos R-R entre reposo y lectura en voz alta son consistentes con el balance autonómico esperado:

| INDICADOR | REPOSO | LECTURA | INTERPRETACION |
| :---: | :---: |  :---: | :---: |
| FC media | 77.0 lpm | 90.6 lpm | Activación simpática ✓| 
| Media R-R | 779.47 ms | 662.31 ms | Intervalos más cortos: FC mayor ✓ | 
| SDNN  | 49.55 ms | 63.49 ms | Mayor variabilidad por patrón resp. irregular |
| SD1 (vagal) | 25.21 ms | 59.54 ms | Arritmia sinusal resp. del habla ↑ |
| CSI (simpático) | 2.59 | 1.13 |Elipse más redonda, no ausencia simpática |
| CVI (vagal) | 4.42 | 4.81 | Modulación vagal-respiratoria durante el habla |

La verbalización activa el eje simpático (FC ↑, R-R ↓) pero simultáneamente genera una modulación vagal-respiratoria fuerte que se refleja en SD1 y CVI. Este fenómeno es documentado en la literatura y no contradice la activación simpática: ambos sistemas pueden coactivarse dependiendo del estado y la tarea.

### Referencias

- Toichi, M., Sugiura, T., Murai, T., & Sengoku, A. (1997). A new method of assessing cardiac autonomic function and its comparison with spectral analysis and coefficient of variation of R–R interval. Journal of the Autonomic Nervous System, 62, 79–84.
- Task Force of the European Society of Cardiology (1996). Heart rate variability: standards of measurement, physiological interpretation, and clinical use. Circulation, 93, 1043–1065.
