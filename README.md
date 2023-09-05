# 📘 Proyecto: lab_PCPDF_CREADORAGENDALAB_04_PY

## 📌 Descripción del proyecto

Este proyecto tiene como objetivo **generar una agenda en PDF** de manera automática.  
La agenda se construye a partir del **día actual** hasta el **31 de diciembre del mismo año**, asignando **una página por cada día**.

Cada página incluye:
- Un **encabezado grande y centrado** con la fecha completa en español (ejemplo: `Jueves 28 Agosto 2025`).
- Un **fondo cuadriculado tipo matemáticas** (grid en gris claro) para escribir notas.
- Un **margen superior** para que la cuadrícula no interfiera con el encabezado.
- Opcionalmente, **números de página** centrados en el pie.

---

## 🛠️ Librerías utilizadas

Este proyecto está desarrollado en **Python 3.9+** y utiliza las siguientes librerías:

1. **[reportlab](https://pypi.org/project/reportlab/)**  
   - Se usa para **generar el PDF**.  
   - Permite dibujar texto, líneas y cuadrículas en las páginas.  
   - Proporciona soporte para fuentes tipográficas personalizadas (ej. Arial, DejaVuSans).  

2. **datetime (incluida en la librería estándar de Python)**  
   - Maneja fechas y operaciones de calendario.  
   - Nos permite obtener la fecha actual y generar el rango de días hasta fin de año.  

3. **zoneinfo (incluida en Python 3.9+)**  
   - Asegura que la fecha actual se tome en la zona horaria **Europe/Paris**.  
   - Si no está disponible, se usa la hora local del sistema.  

4. **os (librería estándar)**  
   - Se utiliza para verificar la existencia de fuentes en el sistema (Arial, DejaVuSans, etc.).  

5. **typing (estándar en Python)**  
   - Añade anotaciones de tipos (`Optional`, `Tuple`, etc.) para mejorar la legibilidad y el mantenimiento del código.  

---

## 📂 Estructura del código

El archivo principal `crear_agenda.py` está organizado en secciones:

1. **Configuración**  
   - Define nombres de días y meses en español.  
   - Configura fuentes tipográficas candidatas para el encabezado.  

2. **Manejo de fuentes**  
   - Función `register_readable_font()` que intenta registrar una fuente con soporte para acentos (Arial o DejaVuSans).  
   - Si no encuentra ninguna, utiliza `Helvetica` como fallback.  

3. **Utilidades de fechas**  
   - `today_europe_paris()`: obtiene la fecha de hoy en la zona horaria Europe/Paris.  
   - `end_of_year()`: devuelve el 31 de diciembre del año actual.  
   - `format_date_spanish()`: devuelve la fecha con formato en español (`Lunes 5 Mayo 2025`).  

4. **Dibujo en PDF**  
   - `draw_grid()`: genera la cuadrícula tipo matemáticas en gris claro.  
   - `draw_centered_text_top()`: escribe el encabezado centrado arriba de la página.  
   - `draw_page_number()`: añade un número de página centrado en el pie.  

5. **Pipeline principal**  
   - `build_agenda_pdf()`: genera el PDF completo desde la fecha de inicio hasta fin de año.  
   - Una página por día, con cuadrícula y encabezado en grande.  

6. **Main**  
   - Ejecuta directamente `build_agenda_pdf()` con parámetros por defecto:  
     - Salida: `Agenda_2025.pdf`  
     - Fecha de inicio: hoy  
     - Tamaño de cuadrícula: 20 puntos (~7 mm)  
     - Tamaño de título: 40 pt  
     - Incluye números de página  

---

## ▶️ Ejecución

Con Python 3.9+ y `reportlab` instalado:

```bash
python crear_agenda.py
```

Esto generará automáticamente el archivo:

```
Agenda_2025.pdf
```

en la carpeta actual.

---

## 📋 Ejemplo visual

Cada página del PDF se verá aproximadamente así:

```
┌───────────────────────────────────────┐
│          Jueves 28 Agosto 2025        │   ← Encabezado grande
├───────────────────────────────────────┤
│   ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢     │   ← Fondo cuadriculado
│   ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢     │
│   ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢     │
│                                       │
│                   [123]               │   ← Número de página (opcional)
└───────────────────────────────────────┘
```

---

## 📌 Notas

- El proyecto está pensado como un **laboratorio básico de manipulación de PDFs en Python**.  
- Puede servir como plantilla para agendas, planificadores o cuadernos personalizados.  
- Nombre del laboratorio: **`lab_PCPDF_CREADORAGENDALAB_04_PY`**.  

---

## 📜 Licencia

Este proyecto está bajo licencia **MIT**.  
Autor: **braco96**
