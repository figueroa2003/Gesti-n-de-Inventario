# Entregado por: Paul Figueroa | Fecha: domingo, 31 de agosto de 2025\n# Proyecto: Sistema Avanzado de Gestión de Inventario\n\nfrom __future__ import annotations
from typing import Dict, List, Set, Tuple, Iterable, Optional
from models import Producto


class Inventario:
    """Colección de productos con índice auxiliar por nombre.

    Estructuras:
    - _items: dict[str, Producto]
    - _index_nombre: dict[str, set[str]]  # nombre_normalizado -> {ids}
    """

    def __init__(self) -> None:
        self._items: Dict[str, Producto] = {}
        self._index_nombre: Dict[str, Set[str]] = {}

    # ---------------------- Helpers de índice ----------------------
    def _agregar_a_indice(self, producto: Producto) -> None:
        clave = producto.normalizar_nombre()
        if clave not in self._index_nombre:
            self._index_nombre[clave] = set()
        self._index_nombre[clave].add(producto.id)

    def _remover_de_indice(self, producto: Producto) -> None:
        clave = producto.normalizar_nombre()
        ids = self._index_nombre.get(clave)
        if ids:
            ids.discard(producto.id)
            if not ids:
                self._index_nombre.pop(clave, None)

    def _reindexar(self) -> None:
        self._index_nombre.clear()
        for p in self._items.values():
            self._agregar_a_indice(p)

    # ---------------------- Operaciones CRUD ----------------------
    def agregar(self, producto: Producto) -> None:
        if producto.id in self._items:
            raise KeyError(f"Ya existe un producto con ID '{producto.id}'.")
        self._items[producto.id] = producto
        self._agregar_a_indice(producto)

    def eliminar(self, id_producto: str) -> Producto:
        if id_producto not in self._items:
            raise KeyError(f"No existe producto con ID '{id_producto}'.")
        prod = self._items.pop(id_producto)
        self._remover_de_indice(prod)
        return prod

    def actualizar(self, id_producto: str,
                   cantidad: Optional[int] = None,
                   precio: Optional[float] = None,
                   nombre: Optional[str] = None) -> Producto:
        if id_producto not in self._items:
            raise KeyError(f"No existe producto con ID '{id_producto}'.")
        p = self._items[id_producto]

        # Si cambia el nombre, hay que mantener el índice
        if nombre is not None and nombre.strip() != p.nombre.strip():
            self._remover_de_indice(p)
            p.nombre_producto = nombre
            self._agregar_a_indice(p)

        if cantidad is not None:
            p.cantidad_producto = cantidad
        if precio is not None:
            p.precio_producto = precio
        return p

    # ---------------------- Consultas ----------------------
    def obtener(self, id_producto: str) -> Producto:
        if id_producto not in self._items:
            raise KeyError(f"No existe producto con ID '{id_producto}'.")
        return self._items[id_producto]

    def buscar_por_nombre(self, texto: str) -> List[Producto]:
        """Búsqueda por coincidencia parcial, insensible a mayúsculas.
        Utiliza el índice por nombres para mejorar el rendimiento cuando hay
        coincidencias exactas; si no, recorre linealmente (fallback).
        """
        t = texto.strip().lower()
        if not t:
            return []
        # Coincidencia exacta rápida mediante índice
        exact_ids = self._index_nombre.get(t, set())
        resultados: Set[str] = set(exact_ids)

        # Búsqueda parcial (contiene) recorriendo claves indexadas
        for clave, ids in self._index_nombre.items():
            if t in clave:
                resultados.update(ids)

        return sorted((self._items[i] for i in resultados),
                      key=lambda p: (p.nombre.lower(), p.id))

    def listar_todos(self, ordenar_por: str = "nombre") -> List[Producto]:
        if ordenar_por == "id":
            return sorted(self._items.values(), key=lambda p: p.id)
        elif ordenar_por == "valor":
            return sorted(self._items.values(), key=lambda p: p.valor_total(), reverse=True)
        else:
            return sorted(self._items.values(), key=lambda p: p.nombre.lower())

    def resumen(self) -> Tuple[int, int, float]:
        """Retorna (items_distintos, unidades_totales, valor_total)."""
        items = len(self._items)
        unidades = sum(p.cantidad for p in self._items.values())
        valor = round(sum(p.valor_total() for p in self._items.values()), 2)
        return (items, unidades, valor)

    # ---------------------- Persistencia ----------------------
    def cargar_desde_dicts(self, datos: Iterable[dict]) -> None:
        self._items.clear()
        ids_vistos: Set[str] = set()
        for d in datos:
            p = Producto.from_dict(d)
            if p.id in ids_vistos:
                raise ValueError(f"ID duplicado al cargar: {p.id}")
            ids_vistos.add(p.id)
            self._items[p.id] = p
        self._reindexar()

    def a_dicts(self) -> List[dict]:
        return [p.to_dict() for p in self.listar_todos("id")]
