import re
from urllib.parse import quote_plus

import pandas as pd


INPUT_FILE = "conversa_grupo.txt"
OUTPUT_FILE = "Controle_Vidracaria.xlsx"
FIELDS = ["Cliente", "Obra", "Peça", "Medidas", "Obs"]


def extract_orders(file_path: str) -> list[dict[str, str]]:
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    orders: list[dict[str, str]] = []
    current_order: dict[str, str] = {}
    pattern = re.compile(r"(Cliente|Obra|Peça|Medidas|Obs):\s*(.+)$")

    for line in lines:
        match = pattern.search(line.strip())
        if not match:
            continue

        key, value = match.groups()

        if key == "Cliente" and current_order:
            current_order = {}

        current_order[key] = value.strip()

        if key == "Obs" and all(field in current_order for field in FIELDS):
            piece_encoded = quote_plus(current_order["Peça"])
            order = {field: current_order[field] for field in FIELDS}
            order["Link Visualização"] = (
                f"https://www.google.com/search?tbm=isch&q={piece_encoded}"
            )
            orders.append(order)
            current_order = {}

    return orders


def main() -> None:
    orders = extract_orders(INPUT_FILE)
    df = pd.DataFrame(orders)
    df.to_excel(OUTPUT_FILE, index=False, engine="openpyxl")
    print(f"Arquivo '{OUTPUT_FILE}' gerado com {len(df)} pedido(s).")


if __name__ == "__main__":
    main()
