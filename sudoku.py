import ortools.sat.python.cp_model

model = ortools.sat.python.cp_model.CpModel()

# Meta-Definition der Dimensionen des Problems.
zahlen = list(range(1, 10))
zeilen = list(range(1, 10))
spalten = list(range(1, 10))
quadranten = [[(zeile, spalte) for zeile in zeilen[i:i + 3] for spalte in spalten[j:j + 3]] for j in [0, 3, 6] for i in [0, 3, 6]]

vorgaben = [
  [0, 7, 0, 0, 0, 0, 0, 9, 0],
  [0, 4, 1, 6, 9, 2, 0, 8, 7],
  [0, 9, 0, 0, 0, 5, 0, 0, 0],
  [0, 6, 0, 2, 8, 1, 0, 7, 0],
  [0, 2, 7, 5, 4, 9, 0, 1, 6],
  [1, 5, 0, 3, 6, 7, 0, 0, 2],
  [0, 0, 0, 1, 0, 6, 7, 3, 9],
  [0, 1, 0, 0, 0, 0, 0, 0, 0],
  [7, 3, 6, 9, 2, 4, 1, 5, 8]]

# Definition der Entscheidungsmöglichkeiten.
entscheidungsvariablen = {}
for zahl in zahlen:
  for zeile in zeilen:
    for spalte in spalten:
      if zahl not in entscheidungsvariablen:
        entscheidungsvariablen[zahl] = {}
      if zeile not in entscheidungsvariablen[zahl]:
        entscheidungsvariablen[zahl][zeile] = {}
      entscheidungsvariablen[zahl][zeile][spalte] = model.NewBoolVar(
        "Zahl {} ist in Zeile {} und Spalte {}.".format(zahl, zeile, spalte))
def position(zahl, zeile, spalte):
  return entscheidungsvariablen[zahl][zeile][spalte]

# Auf jeder Position steht eine Zahl.
for zeile in zeilen:
  for spalte in spalten:
    eine_zahl_kommt_in_dieser_position_vor = []
    for zahl in zahlen:
      eine_zahl_kommt_in_dieser_position_vor.append(position(zahl, zeile, spalte))
    model.AddBoolOr(eine_zahl_kommt_in_dieser_position_vor)

# In keiner Zeile gibt es eine Wiederholung.
for zeile in zeilen:
  for zahl in zahlen:
    for spalte_1 in spalten:
      for spalte_2 in spalten:
        if spalte_1 != spalte_2:
          model.AddBoolOr([position(zahl, zeile, spalte_1).Not(), position(zahl, zeile, spalte_2).Not()])

# In keiner Spalte gibt es eine Wiederholung.
for spalte in spalten:
  for zahl in zahlen:
    for zeile_1 in zeilen:
      for zeile_2 in zeilen:
        if zeile_1 != zeile_2:
          model.AddBoolOr([position(zahl, zeile_1, spalte).Not(), position(zahl, zeile_2, spalte).Not()])

# In keinem Quadranten gibt es eine Wiederholung.
for quadrant in quadranten:
  for zahl in zahlen:
    for (zeile_1, spalte_1) in quadrant:
      for (zeile_2, spalte_2) in quadrant:
        if (zeile_1, spalte_1) != (zeile_2, spalte_2):
          model.AddBoolOr([position(zahl, zeile_1, spalte_1).Not(), position(zahl, zeile_2, spalte_2).Not()])

print(vorgaben)
for zeile in zeilen:
  for spalte in spalten:
    zahl = vorgaben[zeile - 1][spalte - 1]
    if zahl > 0:
      model.AddBoolOr([position(zeile, spalte, zahl)])

# Berechnung des Plans.
solver = ortools.sat.python.cp_model.CpSolver()
status = solver.Solve(model)

# Visualisierung des Plans.
print("Status: {}.".format(status))
if status == ortools.sat.python.cp_model.OPTIMAL:
  for zahl in zahlen:
    for zeile in zeilen:
      for spalte in spalten:
        variable = position(zahl, zeile, spalte)
        entscheidung = bool(solver.Value(variable))
        print("{} {}.".format(variable, entscheidung))
