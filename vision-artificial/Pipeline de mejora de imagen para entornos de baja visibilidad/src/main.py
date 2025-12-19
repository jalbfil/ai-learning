import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import shannon_entropy
from graphviz import Digraph

# =============================================================================
# BLOQUE 1: CONFIGURACION DE RUTAS
# =============================================================================
# Detectamos donde esta este archivo y subimos un nivel para encontrar la raiz
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Definimos rutas relativas para que funcione en cualquier PC
INPUT_DIR = os.path.join(BASE_DIR, "images")
OUT_DIR = os.path.join(BASE_DIR, "results")

# Crear carpeta de salida si no existe
os.makedirs(OUT_DIR, exist_ok=True)

IMG_FILES = ["img1.png", "img2.png", "img3.png", "img4.png"]

# =============================================================================
# BLOQUE 2: FUNCIONES AUXILIARES (MATEMATICAS Y CONVERSION)
# =============================================================================

def read_image_rgb(path):
    """
    Lee la imagen soportando rutas con tildes (ñ, á, ó...) en Windows.
    Usa numpy para leer los bytes raw y luego decodifica con OpenCV.
    """
    if not os.path.exists(path):
        print(f"[AVISO] No encontrado: {path}")
        return None
        
    try:
        # Leemos el archivo como un array de bytes (esto sí soporta tildes)
        img_array = np.fromfile(path, dtype=np.uint8)
        # Decodificamos esos bytes a una imagen BGR
        bgr = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
        if bgr is None:
            print(f"[ERROR] No se pudo decodificar la imagen: {path}")
            return None
            
        # Convertimos a RGB para matplotlib
        return cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        
    except Exception as e:
        print(f"[ERROR CRITICO] Fallo al leer {path}: {e}")
        return None

def to_gray(rgb):
    """Convierte a escala de grises."""
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

def normalize(img):
    """Normaliza de 0-255 a 0.0-1.0 (necesario para math)."""
    return img.astype(np.float32) / 255.0

def denormalize(img):
    """Devuelve de 0.0-1.0 a 0-255 (uint8)."""
    return np.clip(img * 255.0, 0, 255).astype(np.uint8)

def get_metrics_str(img):
    """Calcula media, desviacion y entropia y devuelve un texto formateado."""
    m = np.mean(img)
    s = np.std(img)
    h = shannon_entropy(img)
    return f"Media={m:.0f} Std={s:.0f} H={h:.2f}"

# =============================================================================
# BLOQUE 3: ALGORITMOS DE MEJORA (TEMA 6)
# =============================================================================

def contrast_stretch(img, p_low=2, p_high=98):
    """Estiramiento lineal basado en percentiles (robusto a ruido)."""
    img_float = normalize(img)
    p2, p98 = np.percentile(img_float, (p_low, p_high))
    # Estirar el rango [p2, p98] a [0, 1]
    res = (img_float - p2) / (p98 - p2 + 1e-8)
    return denormalize(np.clip(res, 0, 1))

def gamma_correction(img, gamma=0.5):
    """Correccion Gamma: Expande sombras si gamma < 1."""
    img_float = normalize(img)
    res = np.power(img_float, gamma)
    return denormalize(res)

def log_transform(img):
    """Transformacion Logaritmica: Expande valores bajos."""
    img_float = normalize(img)
    # Formula: c * log(1 + r) / log(1 + max) -> ya normalizado es mas simple
    res = np.log1p(img_float) / np.log1p(1.0)
    return denormalize(res)

def hist_equalization(img):
    """Ecualizacion Global (OpenCV)."""
    return cv2.equalizeHist(img)

# =============================================================================
# BLOQUE 4: GENERACION DE GRAFICAS
# =============================================================================

def save_comparison(fname, gray, processed, method_name):
    """Guarda una imagen comparativa individual."""
    fig, ax = plt.subplots(2, 2, figsize=(10, 8))
    
    # Original + Hist
    ax[0,0].imshow(gray, cmap='gray'); ax[0,0].set_title(f"Original\n{get_metrics_str(gray)}")
    ax[0,1].hist(gray.ravel(), 256, [0,256], color='k'); ax[0,1].set_title("Hist Original")
    
    # Procesada + Hist
    ax[1,0].imshow(processed, cmap='gray'); ax[1,0].set_title(f"{method_name}\n{get_metrics_str(processed)}")
    ax[1,1].hist(processed.ravel(), 256, [0,256], color='b'); ax[1,1].set_title("Hist Procesado")
    
    for a in [ax[0,0], ax[1,0]]: a.axis('off')
    
    out_path = os.path.join(OUT_DIR, f"{fname}_{method_name}.png")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    print(f" -> Guardado: {method_name}")

def save_summary_grid(fname, gray):
    """Genera la lamina resumen 3x3 para el Anexo."""
    methods = [
        ("Original", gray),
        ("Gamma 0.4", gamma_correction(gray, 0.4)),
        ("Gamma 0.5", gamma_correction(gray, 0.5)),
        ("Log", log_transform(gray)),
        ("Stretch", contrast_stretch(gray)),
        ("HistEq", hist_equalization(gray))
    ]
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle(f"Analisis Completo: {fname}", fontsize=16)
    axes = axes.flatten()
    
    for i, (name, img) in enumerate(methods):
        axes[i].imshow(img, cmap='gray')
        axes[i].set_title(f"{name}\n{get_metrics_str(img)}")
        axes[i].axis('off')
        
    out_path = os.path.join(OUT_DIR, f"ANEXO_{fname}")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    print(f" -> Guardado Anexo: {fname}")

# =============================================================================
# BLOQUE 5: EJECUCION
# =============================================================================

def main():
    # Plan de accion: Metodo principal para cada imagen
    PLAN = {
        "img1.png": ("Stretch", lambda x: contrast_stretch(x)),
        "img2.png": ("Gamma", lambda x: gamma_correction(x, 0.45)),
        "img3.png": ("HistEq", lambda x: hist_equalization(x)), # Fallo intencionado para informe
        "img4.png": ("Log", lambda x: log_transform(x))         # Fallo intencionado para informe
    }

    print("--- INICIANDO PROCESAMIENTO ---")
    
    for fname in IMG_FILES:
        path = os.path.join(INPUT_DIR, fname)
        rgb = read_image_rgb(path)
        if rgb is None: continue
        
        print(f"Procesando {fname}...")
        gray = to_gray(rgb)
        
        # 1. Aplicar metodo principal y guardar comparativa
        if fname in PLAN:
            name, func = PLAN[fname]
            processed = func(gray)
            save_comparison(fname, gray, processed, name)
            
        # 2. Generar lamina de anexo con todo
        save_summary_grid(fname, gray)

    print("\n--- HECHO: Revisa la carpeta 'results' ---")

if __name__ == "__main__":
    main()