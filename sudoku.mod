using CP;

int vorgaben[1..9][1..9] = [
  [0, 7, 0, 0, 0, 0, 0, 9, 0],
  [0, 4, 1, 6, 9, 2, 0, 8, 7],
  [0, 9, 0, 0, 0, 5, 0, 0, 0],
  [0, 6, 0, 2, 8, 1, 0, 7, 0],
  [0, 2, 7, 5, 4, 9, 0, 1, 6],
  [1, 5, 0, 3, 6, 7, 0, 0, 2],
  [0, 0, 0, 1, 0, 6, 7, 3, 9],
  [0, 1, 0, 0, 0, 0, 0, 0, 0],
  [7, 3, 6, 9, 2, 4, 1, 5, 8]];

range Zeilen = 1..9;
range Spalten = 1..9;
range Zahlen = 1..9;

tuple Position {
  int zeile;
  int spalte;
};

{Position} quadrant_1 = {
  <1, 1>, <1, 2>, <1, 3>, <2, 1>, <2, 2>, <2, 3>, <3, 1>, <3, 2>, <3, 3>
};

{Position} quadrant_2 = {
  <4, 1>, <4, 2>, <4, 3>, <5, 1>, <5, 2>, <5, 3>, <6, 1>, <6, 2>, <6, 3>
};

{Position} quadrant_3 = {
  <7, 1>, <7, 2>, <7, 3>, <8, 1>, <8, 2>, <8, 3>, <9, 1>, <9, 2>, <9, 3>
};

{Position} quadrant_4 = {
  <1, 4>, <1, 5>, <1, 6>, <2, 4>, <2, 5>, <2, 6>, <3, 4>, <3, 5>, <3, 6>
};

{Position} quadrant_5 = {
  <4, 4>, <4, 5>, <4, 6>, <5, 4>, <5, 5>, <5, 6>, <6, 4>, <6, 5>, <6, 6>
};

{Position} quadrant_6 = {
  <7, 4>, <7, 5>, <7, 6>, <8, 4>, <8, 5>, <8, 6>, <9, 4>, <9, 5>, <9, 6>
};

{Position} quadrant_7 = {
  <1, 7>, <1, 8>, <1, 9>, <2, 7>, <2, 8>, <2, 9>, <3, 7>, <3, 8>, <3, 9>
};

{Position} quadrant_8 = {
  <4, 7>, <4, 8>, <4, 9>, <5, 7>, <5, 8>, <5, 9>, <6, 7>, <6, 8>, <6, 9>
};

{Position} quadrant_9 = {
  <7, 7>, <7, 8>, <7, 9>, <8, 7>, <8, 8>, <8, 9>, <9, 7>, <9, 8>, <9, 9>
};

{Position} Quadranten[1..9] = [quadrant_1, quadrant_2, quadrant_3, quadrant_4, quadrant_5, quadrant_6, quadrant_7, quadrant_8, quadrant_9];

dvar int Entscheidung[Zeilen][Spalten][Zahlen] in 0..1;

subject to {

  forall(zeile in Zeilen, spalte in Spalten) {
    or(zahl in Zahlen) Entscheidung[zeile][spalte][zahl] == 1;
  }

  forall(zeile in Zeilen, zahl in Zahlen, spalte_1 in Spalten, spalte_2 in Spalten : spalte_1 != spalte_2) {
    or(spalte in {spalte_1, spalte_2}) Entscheidung[zeile, spalte, zahl] == 0;
  }

  forall(spalte in Spalten, zahl in Zahlen, zeile_1 in Zeilen, zeile_2 in Zeilen : zeile_1 != zeile_2) {
    or(zeile in {zeile_1, zeile_2}) Entscheidung[zeile, spalte, zahl] == 0;
  }

  forall(q in {1, 2}, zahl in Zahlen, <zeile_1, spalte_1> in Quadranten[q], <zeile_2, spalte_2> in Quadranten[q] : <zeile_1, spalte_1> != <zeile_2, spalte_2>) {
    or(<zeile, spalte> in {<zeile_1, spalte_1>, <zeile_2, spalte_2>}) Entscheidung[zeile][spalte][zahl] == 0;
  }

  forall (zeile in Zeilen, spalte in Spalten : vorgaben[zeile][spalte] != 0) {
    Entscheidung[zeile][spalte][vorgaben[zeile][spalte]] == 1;
  }
}

execute POST_PROCESS {
  writeln("Sudoku Lösung:");
  for(zeile in Zeilen) {
    for(spalte in Spalten) {
      for(zahl in Zahlen) {
        if (Entscheidung[zeile][spalte][zahl] == 1) {
          write(zahl, ", ");
        }
      }
    }
    writeln();
  }
}
