# Guia-N-5-Variabilidad-De-La-Frecuencia-Cardiaca-VHR-y-Balance-Autonomico-
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

####**DIAGRAMA DE FLUJO DE TODA LA METODOLOGIA QUE SE USO**


### b. ADQUISICION DE LA SEÑAL ECG
<img width="467" height="336" alt="image" src="https://github.com/user-attachments/assets/c0cbc64e-214b-48eb-912c-cf329cd1996c" />

Se utilizó esta analogía y la correcta ubicación de los electrodos para obtener la señal de ECG mediante el dispositivo BITalino. A partir de esta configuración, se realizó la adquisición de aproximadamente cuatro minutos de señal cardíaca continua, permitiendo registrar de manera adecuada la actividad eléctrica del corazón. Durante los primeros dos minutos, la persona se mantuvo en estado de reposo y silencio, con el fin de obtener una señal estable y con la menor cantidad posible de interferencias. Posteriormente, en los dos minutos restantes, la medición se realizó en un estado de excitación, hablando en voz alta, para observar los posibles cambios y variaciones presentes en la señal de ECG bajo diferentes condiciones. Finalmente, la señal obtenida fue utilizada para llevar a cabo el análisis correspondiente del comportamiento cardíaco durante ambas situaciones.

<img width="276" height="182" alt="image" src="https://github.com/user-attachments/assets/9ec62e97-c4d3-44d4-a009-cb2f5670ba3f" />

Además, al realizar el análisis de la señal obtenida, se evidenció que la variación observada presentaba un comportamiento similar al de la derivación V3 del ECG, ya que la forma y características de la señal mostraban una mayor semejanza con este tipo de derivación precordial. Esta variación permitió visualizar de manera más clara algunos cambios en la actividad eléctrica cardíaca durante las diferentes condiciones de medición.

## PARTE B
### c. PRE-PROCESAMINETO DE LA SEÑAL
### d. ANALISIS DE LA HRV EN EL DOMINIO DEL TIEMPO
## PARTE C
### e. CONSTRUCCION DEL DIAGRAMA DE PIONCARÉ
