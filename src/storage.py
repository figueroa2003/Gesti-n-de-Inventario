# Entregado por: Paul Figueroa | Fecha: domingo, 31 de agosto de 2025\n# Proyecto: Sistema Avanzado de Gestión de Inventario\n\nfrom __future__ import annotations
import json, csv, os
from typing import List, Dict
from inventory import Inventario
from models import Producto


DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
JSON_PATH = os.path.abspath(os.path.join(DATA_DIR, "inventario.json"))
CSV_PATH = os.path.abspath(os.path.join(DATA_DIR, "inventario.csv"))


def asegurar_directorio() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)


def guardar_json(inv: Inventario, ruta: str = JSON_PATH) -> str:
    asegurar_directorio()
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(inv.a_dicts(), f, ensure_ascii=False, indent=2)
    return ruta


def cargar_json(inv: Inventario, ruta: str = JSON_PATH) -> str:
    asegurar_directorio()
    if not os.path.exists(ruta):
        # si no existe, crear vacío
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump([], f)
    with open(ruta, "r", encoding="utf-8") as f:
        try:
            datos: List[Dict] = json.load(f)
        except json.JSONDecodeError:
            datos = []
    inv.cargar_desde_dicts(datos)
    return ruta


def exportar_csv(inv: Inventario, ruta: str = CSV_PATH) -> str:
    asegurar_directorio()
    campos = ["id", "nombre", "cantidad", "precio", "valor_total"]
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        for d in inv.a_dicts():
            d2 = dict(d)
            d2["valor_total"] = round(d["cantidad"] * d["precio"], 2)
            writer.writerow(d2)
    return ruta
