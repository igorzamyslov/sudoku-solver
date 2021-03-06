from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import List, Optional, Iterator, Set, Tuple

# A list pairs of coordinates that define a Square
SQUARES_COORDINATES = list(product([[0, 3], [3, 6], [6, 9]], repeat=2))
ALLOWED_VALUES = {1, 2, 3, 4, 5, 6, 7, 8, 9, None}


@dataclass()
class Cell:
    value: Optional[int]
    column: int
    row: int

    def __post_init__(self):
        if self.value not in ALLOWED_VALUES:
            raise ValueError(f"{self.value} is not a valid value for a Cell")

    def __repr__(self):
        return f"Cell(value={self.value}, column={self.column}, row={self.row})"

    @property
    def is_valid(self) -> bool:
        """ Checks that cell has a value """
        return self.value is not None

    @property
    def square_coords(self) -> Tuple[int, int]:
        return self.column // 3, self.row // 3


@dataclass()
class Line:
    """ Represents either a column or a row of a Field """
    cells: List[Cell]  # 9 cells

    def __repr__(self):
        return f"Line({self.cells})"

    @property
    def is_valid(self):
        """ Checks that every cell has a value and that every value is unique """
        return (
            all(cell.is_valid for cell in self.cells)
            and len(set(cell.value for cell in self.cells)) == 9)

    def get_missing_values(self) -> Set[int]:
        populated_values = {cell.value for cell in self.cells if cell.value is not None}
        return ALLOWED_VALUES - {None} - populated_values


@dataclass()
class Square:
    """ Represents a square of a Field """
    rows: List[List[Cell]]
    column: int
    row: int

    def __repr__(self):
        return f"Square({self.rows})"

    @property
    def is_valid(self):
        """ Checks that every cell has a value and that every value is unique """
        return (
            all(cell.is_valid for row in self.rows for cell in row)
            and len(set(cell.value for row in self.rows for cell in row)) == 9)

    @property
    def cells(self) -> Iterator[Cell]:
        for row in self.rows:
            for cell in row:
                yield cell

    def get_missing_values(self) -> Set[int]:
        populated_values = {cell.value for row in self.rows for cell in row
                            if cell.value is not None}
        return ALLOWED_VALUES - {None} - populated_values

    def print(self):
        print(" ------- ")
        for i, row in enumerate(self.rows):
            print("|", end=" ")
            for j, cell in enumerate(row):
                print("-" if cell.value is None else cell.value, end=" ")
                if (j+1) % 3 == 0:
                    print("|", end=" ")
            print()
            if (i+1) % 3 == 0:
                print(" ------- ")


@dataclass()
class Field:
    data: List[List[Cell]]

    def __repr__(self):
        return f"Field({self.data})"

    @property
    def is_valid(self) -> bool:
        """ Checks that every row, column and square are correct """
        return (
            all(row.is_valid for row in self.rows)
            and all(column.is_valid for column in self.columns)
            and all(square.is_valid for square in self.squares))

    @property
    def has_empty_cells(self) -> bool:
        return any(cell.value is None for cell in self.cells)

    @property
    def cells(self) -> Iterator[Cell]:
        for row in self.data:
            for cell in row:
                yield cell

    @property
    def rows(self) -> Iterator[Line]:
        """ Return a list of rows """
        for i in range(9):
            yield self.get_row(i)

    @property
    def columns(self) -> Iterator[Line]:
        """ Return a list of columns """
        for i in range(9):
            yield self.get_column(i)

    @property
    def squares(self) -> Iterator[Square]:
        for i in range(3):
            for j in range(3):
                yield self.get_square(i, j)

    @property
    def squares_field(self) -> List[List[Square]]:
        """ Returns 3 lists (rows) of squares """
        squares = []
        for row in range(3):
            squares_row = []
            for column in range(3):
                squares_row.append(self.get_square(column, row))
            squares.append(squares_row)
        return squares

    @staticmethod
    def init_from_data(data: List[List[Optional[int]]]) -> Field:
        """ Initialise the Field from the List of Lists """
        cells = []
        for row_index, row in enumerate(data):
            cell_row = []
            for column_index, value in enumerate(row):
                cell_row.append(Cell(None if value == 0 else value, column_index, row_index))
            cells.append(cell_row)
        return Field(cells)

    def print(self):
        print(" ------- ------- ------- ")
        for i, row in enumerate(self.data):
            print("|", end=" ")
            for j, cell in enumerate(row):
                print("-" if cell.value is None else cell.value, end=" ")
                if (j + 1) % 3 == 0:
                    print("|", end=" ")
            print()
            if (i + 1) % 3 == 0:
                print(" ------- ------- ------- ")

    def get_row(self, index: int) -> Line:
        """ Get n-th row """
        return Line(self.data[index])

    def get_column(self, index: int) -> Line:
        """ Get n-th column """
        return Line([self.get_cell(index, i) for i in range(9)])

    def get_square(self, column: int, row: int) -> Square:
        """ Return a square from a 3x3 field """
        comb_index = row * 3 + column
        comb = SQUARES_COORDINATES[comb_index]
        square_data = []
        for cells_row in self.data[comb[0][0]:comb[0][1]]:
            square_row = []
            for cell in cells_row[comb[1][0]:comb[1][1]]:
                square_row.append(cell)
            square_data.append(square_row)
        return Square(square_data, column, row)

    def get_square_from_coordinates(self, column: int, row: int) -> Square:
        """ Return a Square for the given coordinates of a 9x9 field """
        return self.get_square(column // 3, row // 3)

    def get_cell(self, column: int, row: int) -> Cell:
        """ Return a cell from a 9x9 field"""
        return self.data[row][column]


if __name__ == '__main__':
    field_data = []
    step = 0
    for i in range(9):
        row = []
        for j in range(9):
            row.append(j+1)
        row = row[step:] + row[:step]
        field_data.append(row)
        step += 3
        if step >= 9:
            step -= 8

    field = Field.init_from_data(field_data)

    field.get_cell(0, 0).value = None
    field.get_cell(0, 1).value = None
    field.get_cell(0, 2).value = None
    field.get_cell(2, 0).value = None
    field.get_cell(2, 5).value = None
    field.get_cell(0, 6).value = None
    field.get_cell(5, 0).value = None
    field.get_cell(6, 0).value = None

    field.print()


    from solver import SudokuSolver
    # print(SudokuSolver._get_possible_value_tier_1(field, field.get_cell(2, 0)))
    print(SudokuSolver._get_possible_value_tier_2(field, field.get_cell(2, 0)))
