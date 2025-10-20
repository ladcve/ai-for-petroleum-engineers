# **Herramienta de Calidad de Datos para Ingenieros de Petróleo**  
**Fase 1: Preparación y Limpieza de Datos**  

---

## 📌 **Descripción General**

Esta herramienta es una **aplicación de escritorio profesional** diseñada para ingenieros de petróleo que trabajan con datos de producción y monitoreo de pozos. Permite **cargar, analizar, limpiar y visualizar** datos de forma intuitiva, sin necesidad de conocimientos avanzados en programación.

La solución aborda los desafíos más comunes en el upstream:
- Archivos con formato regional (separador `;`, decimal `,`)
- Valores nulos representados como `"NULL"`
- Nombres de columna no estandarizados (`FECHA` en mayúsculas)
- Outliers y ruido instrumental
- Brechas en los datos

---

## ✨ **Características Principales**

### **1. Carga de Datos Flexible**
- Soporta archivos **CSV** (con separador `;` o `,`) y **Excel** (`.xlsx`)
- Detecta automáticamente la columna de fecha (`Fecha`, `FECHA`, `fecha`, etc.)
- Convierte fechas en formato `DD/MM/YYYY` o `YYYY-MM-DD`
- Maneja valores nulos: `"NULL"`, `"N/A"`, celdas vacías

### **2. Análisis Inteligente**
- Detecta todas las variables numéricas presentes en los archivos
- Calcula rangos operativos sugeridos (percentiles 1%–99%)
- Muestra rangos iniciales basados en los datos reales

### **3. Limpieza Técnica Rigurosa**
- **Filtra outliers** (no los aplasta): elimina valores fuera del rango definido
- **Interpola brechas cortas**: solo rellena gaps ≤ 3 días
- **Preserva gaps largos**: mantiene discontinuidades como información útil
- **Mantiene la integridad temporal**: respeta la secuencia cronológica

### **4. Visualización Profesional**
- **Dos gráficos independientes** para comparar variables
- **Comparación antes/después**: original (gris) vs limpio (azul)
- **Barra de herramientas de Matplotlib**: zoom, pan, guardar, etc.
- **Selectores de variables**: elige qué variables visualizar

### **5. Interfaz de Usuario Intuitiva**
- **Botones numerados** (1 a 5) que guían el flujo de trabajo
- **Área de log** en tiempo real con mensajes de estado
- **Panel de rangos** editable para ajustar límites operativos
- **Diseño limpio y profesional** optimizado para ingenieros

### **6. Exportación Robusta**
- Guarda datos limpios en formato **CSV**
- Mantiene el mismo separador y formato decimal que la entrada
- Valores nulos se exportan como celdas vacías

---

## 📦 **Requisitos y Librerías**

### **Requisitos del Sistema**
- **Sistema Operativo**: Windows, macOS o Linux
- **Python**: versión 3.8 o superior
- **Espacio en disco**: ~200 MB

### **Librerías Necesarias**

| Librería | Versión Mínima | Propósito |
|----------|----------------|-----------|
| `tkinter` | Incluido en Python | Interfaz gráfica |
| `pandas` | 1.3.0+ | Manipulación de datos |
| `numpy` | 1.21.0+ | Operaciones numéricas |
| `matplotlib` | 3.4.0+ | Visualización de gráficos |

---

## ⚙️ **Instalación Paso a Paso**

### **Opción 1: Instalación Manual (Recomendado para Desarrolladores)**

1. **Instalar Python**  
   Descarga e instala Python 3.8+ desde [python.org](https://www.python.org/downloads/)

2. **Clonar o descargar el repositorio**  
   ```bash
   git clone https://github.com/tu-usuario/calidad-datos-petroleo.git
   cd calidad-datos-petroleo
   ```

3. **Crear entorno virtual (opcional pero recomendado)**  
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

4. **Instalar dependencias**  
   ```bash
   pip install pandas numpy matplotlib
   ```

5. **Ejecutar la aplicación**  
   ```bash
   python fase1_calidad_datos.py
   ```

### **Opción 2: Instalación Directa (Sin entorno virtual)**

```bash
pip install pandas numpy matplotlib
python fase1_calidad_datos.py
```

---

## 🚀 **Generación de Ejecutable (Para Distribución)**

Para crear un archivo `.exe` autocontenido que no requiera Python instalado:

### **Paso 1: Instalar PyInstaller**
```bash
pip install pyinstaller
```

### **Paso 2: Generar el ejecutable**
```bash
pyinstaller --onefile --windowed --name="CalidadDatosPetroleo" fase1_calidad_datos.py
```

### **Parámetros explicados:**
- `--onefile`: Crea un único archivo ejecutable
- `--windowed`: Sin consola de comandos (solo interfaz gráfica)
- `--name`: Nombre del ejecutable

### **Paso 3: Localizar el ejecutable**
El archivo se generará en la carpeta `dist/`:
```
dist/CalidadDatosPetroleo.exe  # Windows
dist/CalidadDatosPetroleo      # macOS/Linux
```

### **Notas importantes:**
- El proceso de generación puede tardar 2-5 minutos
- El archivo `.exe` tendrá ~50-100 MB (incluye todas las dependencias)
- Para reducir el tamaño, considera usar `--exclude-module` para librerías no usadas

---

## 📁 **Estructura del Proyecto**

```
calidad-datos-petroleo/
├── fase1_calidad_datos.py     # Archivo principal de la aplicación
├── README.md                  # Este documento
├── ejemplo_datos/
│   ├── produccion.csv         # Ejemplo de archivo de producción
│   └── pt.csv                 # Ejemplo de archivo de presión/temperatura
└── requirements.txt           # Lista de dependencias (opcional)
```

---

## 📝 **Formato de Archivos de Entrada**

### **Archivo de Producción (`produccion.csv`)**
```csv
FECHA;TASA_GAS;TASA_CONDENSADO;TASA_AGUA;ACUM_CONDESADO;ACUM_AGUA;ACUM_GAS
01/01/2023;38,796031;1226,21;9,38;2468501,5;77080,46;79919,47
02/01/2023;38,961861;1216,16;12,43;2469717,66;77092,89;79958,43
03/01/2023;NULL;1267,73;8,36;2470985,39;77101,25;79997,91
```

### **Archivo de Presión/Temperatura (`pt.csv`)**
```csv
FECHA;Pwh;Pbh;Twh;Tbh
01/01/2023;450,2;2100,5;120,3;210,8
02/01/2023;445,7;2090,2;122,1;212,4
03/01/2023;448,9;NULL;121,5;211,7
```

### **Características soportadas:**
- ✅ Separador: punto y coma (`;`)
- ✅ Decimal: coma (`,`)
- ✅ Fecha: `DD/MM/YYYY` o `YYYY-MM-DD`
- ✅ Valores nulos: `"NULL"`, `"N/A"`, celdas vacías
- ✅ Nombres de columna: cualquier variante de `FECHA`

---

## 🆘 **Solución de Problemas Comunes**

### **Problema: "No se encontró la columna 'FECHA'"**
**Solución:** Verifica que tu archivo tenga una columna llamada `Fecha`, `FECHA`, `fecha`, etc. La herramienta es insensible a mayúsculas.

### **Problema: Errores al cargar el archivo**
**Solución:** Asegúrate de que el archivo no esté abierto en Excel u otro programa. Usa el formato CSV con separador `;`.

### **Problema: Gráficos no se muestran correctamente**
**Solución:** La limpieza filtra outliers. Si todos los datos están fuera de rango, no habrá puntos para graficar. Ajusta los rangos operativos.

### **Problema: Aplicación se cierra al iniciar**
**Solución:** Instala todas las dependencias: `pip install pandas numpy matplotlib`

---

## 📬 **Soporte y Actualizaciones**

- **Repositorio**: [github.com/tu-usuario/calidad-datos-petroleo](https://github.com/tu-usuario/calidad-datos-petroleo)
- **Autor**: [Tu Nombre]
- **Contacto**: [tu-email@dominio.com]
- **Licencia**: MIT License

---

## 🙏 **Agradecimientos**

Esta herramienta fue desarrollada con el apoyo de la comunidad de ingenieros de petróleo y científicos de datos del sector upstream. Gracias por su feedback y pruebas en entornos reales.

---

**© [Tu Nombre] – [Año]**  
*Herramienta de Calidad de Datos para Ingenieros de Petróleo*
