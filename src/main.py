# Entregado por: Paul Figueroa | Fecha: domingo, 31 de agosto de 2025\n# Proyecto: Sistema Avanzado de Gestión de Inventario\n\nfrom __future__ import annotations
from typing import Optional
from inventory import Inventario
from models import Producto
from storage import guardar_json, cargar_json, exportar_csv, JSON_PATH, CSV_PATH


def input_no_vacio(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Entrada vacía. Intenta de nuevo.")


def pedir_entero(prompt: str, minimo: Optional[int] = None) -> int:
    while True:
        try:
            v = int(input(prompt))
            if minimo is not None and v < minimo:
                print(f"Debe ser un entero ≥ {minimo}.")
                continue
            return v
        except ValueError:
            print("Debe ser un número entero.")


def pedir_float(prompt: str, minimo: Optional[float] = None) -> float:
    while True:
        try:
            v = float(input(prompt))
            if minimo is not None and v < minimo:
                print(f"Debe ser un número ≥ {minimo}.")
                continue
            return round(v, 2)
        except ValueError:
            print("Debe ser un número (usa punto decimal).")


def mostrar_producto(p: Producto) -> None:
    print(f"- ID: {p.id} | Nombre: {p.nombre} | Cantidad: {p.cantidad} | Precio: {p.precio:.2f} | Valor: {p.valor_total():.2f}")


def menu() -> None:
    inv = Inventario()
    cargar_json(inv)  # auto crea si no existe

    acciones = {
        "1": "Añadir producto",
        "2": "Eliminar producto por ID",
        "3": "Actualizar producto",
        "4": "Buscar por nombre",
        "5": "Mostrar todos",
        "6": "Resumen",
        "7": "Guardar",
        "8": "Cargar",
        "9": "Exportar CSV",
        "0": "Salir",
    }

    while True:
        print("\n=== Inventario (almacenado en JSON) ===")
        for k in sorted(acciones):
            print(f"{k}. {acciones[k]}")
        op = input("Elige una opción: ").strip()

        if op == "1":
            try:
                idp = input_no_vacio("ID: ")
                nom = input_no_vacio("Nombre: ")
                cant = pedir_entero("Cantidad: ", minimo=0)
                prec = pedir_float("Precio: ", minimo=0.0)
                inv.agregar(Producto(id=idp, nombre=nom, cantidad=cant, precio=prec))
                print("Producto añadido correctamente.")
            except Exception as e:
                print(f"Error al añadir: {e}")

        elif op == "2":
            try:
                idp = input_no_vacio("ID a eliminar: ")
                prod = inv.eliminar(idp)
                print("Eliminado:")
                mostrar_producto(prod)
            except Exception as e:
                print(f"Error al eliminar: {e}")

        elif op == "3":
            try:
                idp = input_no_vacio("ID a actualizar: ")
                print("Deja en blanco si no deseas cambiar ese campo.")
                nom_raw = input("Nuevo nombre: ").strip()
                cant_raw = input("Nueva cantidad: ").strip()
                prec_raw = input("Nuevo precio: ").strip()

                kwargs = {}
                if nom_raw:
                    kwargs["nombre"] = nom_raw
                if cant_raw:
                    try:
                        kwargs["cantidad"] = int(cant_raw)
                    except ValueError:
                        print("Cantidad inválida. Se ignora.")
                if prec_raw:
                    try:
                        kwargs["precio"] = float(prec_raw)
                    except ValueError:
                        print("Precio inválido. Se ignora.")

                prod = inv.actualizar(idp, **kwargs)
                print("Actualizado:")
                mostrar_producto(prod)
            except Exception as e:
                print(f"Error al actualizar: {e}")

        elif op == "4":
            texto = input_no_vacio("Texto a buscar en el nombre: ")
            resultados = inv.buscar_por_nombre(texto)
            if not resultados:
                print("Sin coincidencias.")
            else:
                print(f"Encontrados {len(resultados)} producto(s):")
                for p in resultados:
                    mostrar_producto(p)

        elif op == "5":
            modo = input("Ordenar por [nombre|id|valor] (enter=nombre): ").strip().lower() or "nombre"
            for p in inv.listar_todos(modo):
                mostrar_producto(p)

        elif op == "6":
            items, unidades, valor = inv.resumen()
            print(f"Items distintos: {items} | Unidades totales: {unidades} | Valor total: {valor:.2f}")

        elif op == "7":
            try:
                ruta = guardar_json(inv)
                print(f"Guardado en: {ruta}")
            except Exception as e:
                print(f"Error al guardar: {e}")

        elif op == "8":
            try:
                ruta = cargar_json(inv)
                print(f"Cargado desde: {ruta}")
            except Exception as e:
                print(f"Error al cargar: {e}")

        elif op == "9":
            try:
                ruta = exportar_csv(inv)
                print(f"CSV exportado en: {ruta}")
            except Exception as e:
                print(f"Error al exportar CSV: {e}")

        elif op == "0":
            print("¡Hasta luego!")
            break

        else:
            print("Opción no válida, intenta de nuevo.")


if __name__ == "__main__":
    menu()
