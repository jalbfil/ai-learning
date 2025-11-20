# Hate Speech Analysis in Spanish – TacticalMind.AI

Este repositorio forma parte de los proyectos de **TacticalMind.AI** y presenta un pipeline completo de NLP para **caracterizar y analizar posibles patrones de discurso de odio en textos en español**.

El objetivo del proyecto es construir una base sólida de:
- Procesamiento lingüístico con spaCy
- Análisis de entidades nombradas (NER)
- Ingeniería de características lingüísticas
- Exploración de patrones en el contenido
- Preparación de datos para futuros modelos de clasificación o sistemas de moderación automatizada

---

## 👤 Autor
**Juan Carlos Albert – TacticalMind.AI**

---

## 🔍 ¿Qué incluye el proyecto?

### ✔️ Preprocesamiento del corpus  
Normalización, limpieza de columnas residuales y preparación del dataset para análisis.

### ✔️ Procesamiento lingüístico (spaCy – es_core_news_md)
- Tokenización  
- Lematización  
- POS tagging  
- Dependencias sintácticas  
- Atributos morfológicos

### ✔️ Análisis de Entidades (NER)
Identificación de:
- Personas  
- Localizaciones  
- Organizaciones  
- Nacionalidades  

### ✔️ Ingeniería de características
Creación de:
- Distribuciones de POS  
- Longitud del texto  
- Densidad de entidades  
- Frecuencias de patrones relevantes  
- Indicadores útiles para modelos de hate speech

### ✔️ Análisis exploratorio
Primeras visualizaciones y estadísticas descriptivas para comprender tendencias en el texto.

---

## 📁 Estructura del repositorio

tacticalmind-hate-speech-es/
├── README.md
├── requirements.txt
└── caracteristicasOdio_PRO.ipynb
