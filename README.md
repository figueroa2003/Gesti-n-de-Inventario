---
Entregado por: Paul Figueroa
Fecha de entrega: domingo, 31 de agosto de 2025
Universidad: Universidad Estatal Amazónica
---

# Sistema Avanzado de Gestión de Inventario (Python)

Este proyecto implementa un sistema de gestión de inventario en consola utilizando **POO**, **colecciones de Python** y **almacenamiento persistente en archivos**.

## Estructura
```
inventario_avanzado/
├── src/
│   ├── models.py        # Clase Producto
│   ├── inventory.py     # Clase Inventario y lógica de negocio
│   ├── storage.py       # Lectura/escritura JSON y CSV
│   └── main.py          # Interfaz de usuario por consola (menú)
├── data/
│   └── inventario.json  # Archivo de datos (persistencia)
└── README.md
```

## Cómo ejecutar
1. Requisitos: Python 3.10+ (no requiere librerías externas).
2. En consola, ubicarse en la carpeta `src` y ejecutar:
   ```bash
   python main.py
   ```
3. El programa crea/usa `../data/inventario.json` para guardar y cargar el inventario.

## Colecciones utilizadas y por qué
- **dict**: `Inventario._items` mapea `id -> Producto` para **búsqueda O(1)** por ID.
- **dict[str, set[str]]**: `Inventario._index_nombre` es un índice invertido `nombre_normalizado -> {ids}`
  para búsquedas por nombre rápidas y consistentes. Usa **set** para evitar duplicados y obtener operaciones eficientes de unión/intersección.
- **list**: para **listados ordenados** (e.g., mostrar productos ordenados por nombre o ID).
- **tuple**: métodos que retornan múltiples valores, p.ej. `resumen()` retorna
  `(cantidad_items, cantidad_total_unidades, valor_total)`.
- **set** adicionalmente para detectar **IDs duplicados** al cargar desde archivo.

## Persistencia en archivos
- **JSON**: serialización/deserialización de `Producto` a diccionario (`to_dict()` / `from_dict()`).
- **CSV** (opcional): exportación para uso externo (Excel/Sheets).
- Manejo robusto de errores de E/S y validación de datos.

## Funcionalidades
- Añadir productos (con validaciones de ID único, cantidad ≥ 0, precio ≥ 0).
- Eliminar por ID.
- Actualizar **cantidad** y/o **precio**.
- Buscar por nombre (coincidencia parcial, insensible a mayúsculas).
- Mostrar todos (opción de ordenamiento).
- Guardar / Cargar.
- Exportar CSV.
- Resumen del inventario (conteos y valor total).

## Diseño
- `Producto` encapsula atributos con propiedades y validaciones.
- `Inventario` mantiene la integridad del índice por nombre y del contenedor principal.
- `storage.py` separa la **infraestructura** de la **lógica de negocio**.
- `main.py` proporciona una **UI en consola** clara y guiada.

---

© 2025. Proyecto educativo.
