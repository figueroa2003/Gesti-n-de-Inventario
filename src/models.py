# Entregado por: Paul Figueroa | Fecha: domingo, 31 de agosto de 2025\n# Proyecto: Sistema Avanzado de Gestión de Inventario\n\nfrom __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any


def _validar_id(valor: str) -> str:
    valor = str(valor).strip()
    if not valor:
        raise ValueError("El ID no puede estar vacío.")
    return valor


def _validar_nombre(valor: str) -> str:
    valor = str(valor).strip()
    if not valor:
        raise ValueError("El nombre no puede estar vacío.")
    return valor


def _validar_cantidad(valor: int) -> int:
    try:
        iv = int(valor)
    except Exception as e:
        raise ValueError("La cantidad debe ser un entero.") from e
    if iv < 0:
        raise ValueError("La cantidad no puede ser negativa.")
    return iv


def _validar_precio(valor: float) -> float:
    try:
        fv = float(valor)
    except Exception as e:
        raise ValueError("El precio debe ser numérico.") from e
    if fv < 0:
        raise ValueError("El precio no puede ser negativo.")
    return round(fv, 2)


@dataclass(slots=True)
class Producto:
    """Entidad de dominio que representa un producto del inventario."""
    id: str = field(metadata={"desc": "Identificador único"})
    nombre: str
    cantidad: int
    precio: float

    def __post_init__(self) -> None:
        # Validaciones centralizadas
        self.id = _validar_id(self.id)
        self.nombre = _validar_nombre(self.nombre)
        self.cantidad = _validar_cantidad(self.cantidad)
        self.precio = _validar_precio(self.precio)

    # Propiedades (getters/setters con validación)
    @property
    def id_producto(self) -> str:
        return self.id

    @property
    def nombre_producto(self) -> str:
        return self.nombre

    @nombre_producto.setter
    def nombre_producto(self, valor: str) -> None:
        self.nombre = _validar_nombre(valor)

    @property
    def cantidad_producto(self) -> int:
        return self.cantidad

    @cantidad_producto.setter
    def cantidad_producto(self, valor: int) -> None:
        self.cantidad = _validar_cantidad(valor)

    @property
    def precio_producto(self) -> float:
        return self.precio

    @precio_producto.setter
    def precio_producto(self, valor: float) -> None:
        self.precio = _validar_precio(valor)

    # Serialización
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Producto":
        return Producto(
            id=data["id"],
            nombre=data["nombre"],
            cantidad=data["cantidad"],
            precio=data["precio"],
        )

    def valor_total(self) -> float:
        """Retorna el valor total de este ítem (cantidad * precio)."""
        return round(self.cantidad * self.precio, 2)

    def normalizar_nombre(self) -> str:
        return self.nombre.strip().lower()
