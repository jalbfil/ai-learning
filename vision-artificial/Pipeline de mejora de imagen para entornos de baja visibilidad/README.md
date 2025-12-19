# Pipeline de Mejora de Imagen para Entornos de Baja Visibilidad

Este proyecto implementa y compara diferentes técnicas de **Visión Artificial** (operaciones puntuales) para la recuperación de información en imágenes nocturnas o severamente subexpuestas.

El estudio utiliza un subconjunto del dataset **"The Dark Face"** para evaluar cómo distintos algoritmos afectan al histograma, el contraste global y la entropía de la imagen.

---

## 🎯 Objetivo

El objetivo principal no es solo "aclarar" la imagen, sino recuperar detalles estructurales ocultos en las sombras sin introducir ruido artificial ni degradar la naturalidad de la escena. Se busca responder a la pregunta: **¿Son los métodos automáticos (como la ecualización) siempre la mejor opción?**

## 🛠️ Metodología

Se ha implementado un pipeline de procesamiento en Python que aplica y compara las siguientes transformaciones:

1. **Estiramiento Lineal de Contraste (Contrast Stretching):** Basado en percentiles (2% - 98%) para robustez frente a outliers.
2. **Transformación Logarítmica:** Expansión de rango dinámico teórica.
3. **Corrección Gamma (Ley de Potencia):** Expansión no lineal de zonas oscuras.
4. **Ecualización de Histograma (HistEq):** Redistribución automática de intensidades basada en la CDF.

---

## Resultados 

El análisis cuantitativo (Media, Desviación Típica, Entropía de Shannon) y cualitativo arrojó las siguientes conclusiones:

* **Ecualización de Histograma:** Aunque maximiza el contraste matemático (), en escenas nocturnas amplifica severamente el **ruido del sensor** y provoca posterización (caída de la entropía).
* **Logaritmo:** Resultó insuficiente para imágenes con histogramas colapsados en el negro absoluto.
* **Corrección Gamma ():** Fue la técnica óptima. Logró expandir las sombras preservando la **coherencia estructural** y manteniendo la entropía de la imagen original.

---

## Instalación y Uso

### Prerrequisitos

* Python 3.10+.
* Git.

### Pasos

1. **Clonar el repositorio:**
```bash
git clone https://github.com/tu-usuario/vision-artificial-pipeline.git

```


2. **Crear entorno virtual (Recomendado):**
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Mac/Linux:
source venv/bin/activate

```


3. **Instalar dependencias:**
```bash
pip install -r requirements.txt

```


4. **Ejecutar el pipeline:**
Asegúrate de tener tus imágenes en la carpeta `images/` y ejecuta:
```bash
python src/main.py

```


El script generará automáticamente una carpeta `results/` con:

* Gráficas comparativas individuales.
* Láminas resumen 3x3 para Anexos.
* Un diagrama de flujo del pipeline (Graphviz).

---

## Estructura del Proyecto

```text
vision-artificial/
├── images/          # Imágenes de entrada (Dataset Dark Face)
├── results/         # Salida generada (Gráficas y métricas)
├── src/             # Código fuente
│   └── main.py      # Script principal del pipeline
├── .gitignore       # Configuración de exclusiones Git
├── requirements.txt # Dependencias del proyecto
└── README.md        # Documentación

```

## Tecnologías Utilizadas

* **Python:** Lenguaje principal.
* **OpenCV (cv2):** Procesamiento de imágenes y transformaciones.
* **NumPy:** Operaciones matriciales y cálculo de percentiles.
* **Matplotlib:** Visualización de histogramas y resultados.
* **Scikit-image:** Cálculo de entropía de Shannon.
* **Graphviz:** Generación automática de diagramas de flujo.

## Autor

**Juan Carlos Albert Fillol**

* Máster en Inteligencia Artificial - Visión Artificial
* https://www.linkedin.com/in/juan-carlos-albert-fillol-778295397/
