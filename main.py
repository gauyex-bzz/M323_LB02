"""
author: Xavier Gauye
date: 09.11.2024
"""

from flask import Flask, request, jsonify
from functools import reduce

app = Flask(__name__)

# Beispiel-Datensatz für Benutzerinformationen
users = [
    {"name": "Barbara", "age": 25, "city": "Zürich"},
    {"name": "Karl", "age": 30, "city": "Bern"},
    {"name": "Frederik", "age": 35, "city": "Luzern"},
]


# Endpunkt für den gesamten Datensatz
# A1G: Eigenschaften von Funktionen beschreiben
@app.route('/dataset', methods=['GET'])
def get_dataset():
    return jsonify(users)


# Endpunkt für Map-Transformationen
# A1F: Verwendung von immutable values
@app.route('/transform/map', methods=['POST'])
def map_transformation():
    operation = request.json.get('operation')  # B2G: Funktionen als Objekte behandeln

    if operation == "age_squared":
        transformed = list(map(lambda x: {**x, "age": x["age"] ** 2}, users))
    elif operation == "uppercase_city":
        transformed = list(map(lambda x: {**x, "city": x["city"].upper()}, users))
    else:
        return jsonify({"error": "Unbekannte Operation"}), 400

    return jsonify(transformed)


# Endpunkt zum Filtern von Benutzern basierend auf einer Bedingung
# B1F: Algorithmus in funktionale Teilstücke aufteilen
# B1G: Filter zur Auswahl von Benutzern nach einem Kriterium
@app.route('/transform/filter', methods=['POST'])
def filter_transformation():
    condition = request.json.get('condition')

    if condition == "age_above_30":
        filtered = list(filter(lambda x: x["age"] > 30, users))
    else:
        return jsonify({"error": "Unbekannte Bedingung"}), 400

    return jsonify(filtered)


# Endpunkt zur Kombination von Filter und Map in einer Pipeline
# B1E: Funktionen in Algorithmen implementieren
@app.route('/filter_and_map', methods=['POST'])
def filter_and_map():
    """
    Filtert Benutzer mit Alter über 30 und macht deren Namen groß.
    """
    filtered_mapped = list(
        map(lambda x: {**x, "name": x["name"].upper()},
            filter(lambda x: x["age"] > 30, users))
    )
    return jsonify(filtered_mapped)


# Endpunkt zum Verwenden von Lambda-Ausdrücken mit mehreren Argumenten
# B3G: Einfache Lambda-Ausdrücke
def age_difference():
    user1_name = request.json.get("user1")
    user2_name = request.json.get("user2")

    # B3F: Lambda-Ausdruck mit mehreren Argumenten
    user1 = next((user for user in users if user["name"] == user1_name), None)
    user2 = next((user for user in users if user["name"] == user2_name), None)

    if user1 and user2:
        difference = (lambda a, b: abs(a - b))(user1["age"], user2["age"])
        return jsonify({"age_difference": difference})
    else:
        return jsonify({"error": "Ein oder beide Benutzer nicht gefunden"}), 400


# Endpunkt für benutzerdefinierte Altersanpassung
# B2G, B2F, B2E: Verwenden von Funktionen als Argumente und Closures
def apply_custom_operation(data, operation):
    # B2G: Funktionen als Objekte behandeln und als Parameter übergeben
    return list(map(operation, data))


@app.route('/custom_age_adjustment', methods=['POST'])
def custom_age_adjustment():
    adjustment = request.json.get("adjustment", 0)

    def adjust_age(user):
        return {**user, "age": user["age"] + adjustment}

    # B2E: Funktionen als Argumente verwenden (closures)
    adjusted_users = apply_custom_operation(users, adjust_age)
    return jsonify(adjusted_users)


# Lambda mit benuzterdefinierten Kriterien
@app.route('/sorted_users', methods=['GET'])
def sorted_users():
    sort_by = request.args.get("sort_by", "age")  # Default-Sortierung nach Alter

    # B3E: Lambda-Ausdruck zur Bestimmung des Sortierkriteriums
    sorted_list = sorted(users, key=lambda x: x[sort_by])
    return jsonify(sorted_list)


# Endpunkt für Reduktionsoperationen auf dem Datensatz
# B4G, B4F, B4E: Verwenden von Reduce zur Aggregation von Daten
@app.route('/reduce_total_age', methods=['GET'])
def reduce_total_age():
    total_age = reduce(lambda acc, x: acc + x["age"], users, 0)
    return jsonify({"total_age": total_age})


# Endpunkt zur komplexen Verarbeitung durch Kombination von Map und Filter
# A1E: Vergleich von verschiedenen Paradigmen, um komplexe Aufgaben zu lösen
@app.route('/complex_data_processing', methods=['GET'])
def complex_data_processing():
    processed_data = list(
        map(lambda u: {**u, "age": u["age"] * 2},
            filter(lambda u: u["age"] >= 18, users))
    )
    return jsonify(processed_data)


if __name__ == '__main__':
    app.run(debug=True)
