import json
import ortools.sat.python.cp_model
import sys

model = ortools.sat.python.cp_model.CpModel()

# Meta-Definition der Dimensionen des Problems.
zahlen = list(range(1, 10))
zeilen = list(range(1, 10))
spalten = list(range(1, 10))
quadranten = [[(zeile, spalte) for zeile in zeilen[i:i + 3] for spalte in spalten[j:j + 3]] for j in [0, 3, 6] for i in [0, 3, 6]]

vorgaben = json.load(sys.stdin)

# Definition der Entscheidungsmöglichkeiten.
entscheidungsvariablen = {}
for zeile in zeilen:
  for spalte in spalten:
    for zahl in zahlen:
      if zeile not in entscheidungsvariablen:
        entscheidungsvariablen[zeile] = {}
      if spalte not in entscheidungsvariablen[zeile]:
        entscheidungsvariablen[zeile][spalte] = {}
      entscheidungsvariablen[zeile][spalte][zahl] = model.NewBoolVar(
        "Zeile {} und Spalte {} enthalten Zahl {}.".format(zeile, spalte, zahl))
def position(zeile, spalte, zahl):
  return entscheidungsvariablen[zeile][spalte][zahl]

# Auf jeder Position steht eine Zahl.
for zeile in zeilen:
  for spalte in spalten:
    eine_zahl_kommt_in_dieser_position_vor = []
    for zahl in zahlen:
      eine_zahl_kommt_in_dieser_position_vor.append(position(zeile, spalte, zahl))
    model.AddBoolOr(eine_zahl_kommt_in_dieser_position_vor)

# In keiner Zeile gibt es eine Wiederholung.
for zeile in zeilen:
  for zahl in zahlen:
    for spalte_1 in spalten:
      for spalte_2 in spalten:
        if spalte_1 != spalte_2:
          model.AddBoolOr([position(zeile, spalte_1, zahl).Not(), position(zeile, spalte_2, zahl).Not()])

# In keiner Spalte gibt es eine Wiederholung.
for spalte in spalten:
  for zahl in zahlen:
    for zeile_1 in zeilen:
      for zeile_2 in zeilen:
        if zeile_1 != zeile_2:
          model.AddBoolOr([position(zeile_1, spalte, zahl).Not(), position(zeile_2, spalte, zahl).Not()])

# In keinem Quadranten gibt es eine Wiederholung.
for quadrant in quadranten:
  for zahl in zahlen:
    for (zeile_1, spalte_1) in quadrant:
      for (zeile_2, spalte_2) in quadrant:
        if (zeile_1, spalte_1) != (zeile_2, spalte_2):
          model.AddBoolOr([position(zeile_1, spalte_1, zahl).Not(), position(zeile_2, spalte_2, zahl).Not()])

for zeile in zeilen:
  for spalte in spalten:
    zahl = vorgaben[zeile - 1][spalte - 1]
    if zahl != 0:
      model.AddBoolOr([position(zeile, spalte, zahl)])

# Berechnung des Plans.
solver = ortools.sat.python.cp_model.CpSolver()
status = solver.Solve(model)

# Visualisierung des Plans.
if status != ortools.sat.python.cp_model.OPTIMAL:
  print("Es gibt kein Sudokubrett zu den Vorgaben.")
else:
  endzustand = [[0 for spalte in spalten] for zeile in zeilen]
  for zeile in zeilen:
    for spalte in spalten:
      for zahl in zahlen:
        if solver.Value(position(zeile, spalte, zahl)):
          endzustand[zeile - 1][spalte - 1] = zahl
  for zeile in zeilen:
    print(endzustand[zeile - 1])
