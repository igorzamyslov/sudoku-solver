from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import List, Optional, Iterator


@dataclass()
class Cell:
    value: Optional[int]
    column: int
    row: int

    def __repr__(self):
        return f"Cell(value={self.value}, column={self.column}, row={self.row})"

    @property
    def is_valid(self) -> bool:
        """ Checks that cell has a value """
        return self.value is not None


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


@dataclass()
class Square:
    """ Represents a square of a Field """
    rows: List[List[Cell]]

    def __repr__(self):
        return f"Square({self.rows})"

    @property
    def is_valid(self):
        """ Checks that every cell has a value and that every value is unique """
        return (
            all(cell.is_valid for row in self.rows for cell in row)
            and len(set(cell.value for row in self.rows for cell in row)) == 9)


@dataclass()
class Field:
    data: List[List[Cell]]

    def __repr__(self):
        return f"Field({self.data})"

    @property
    def is_valid(self):
        """ Checks that every row, column and square are correct """
        return (
            all(row.is_valid for row in self.rows)
            and all(column.is_valid for column in self.columns)
            # squares
        )

    @property
    def rows(self) -> Iterator[Line]:
        """ Return a list of rows """
        for row in self.data:
            yield Line(row)

    @property
    def columns(self) -> Iterator[Line]:
        """ Return a list of columns """
        for i in range(9):
            column_cells = []
            for row in self.data:
                column_cells.append(row[i])
            yield Line(column_cells)

    @property
    def squares(self) -> List[List[Square]]:
        """ Returns 3 lists (rows) of squares """
        squares_coordinates = [[0, 3], [3, 6], [6, 9]]
        squares_coordinates_combs = list(product(squares_coordinates, repeat=2))
        squares = []
        for i in range(3):
            squares_row = []
            for comb in squares_coordinates_combs[3 * i:3 * (i + 1)]:
                square_data = []
                for row in self.data[comb[0][0]:comb[0][1]]:
                    square_row = []
                    for cell in row[comb[1][0]:comb[1][1]]:
                        square_row.append(cell)
                    square_data.append(square_row)
                squares_row.append(Square(square_data))
            squares.append(squares_row)
        return squares

    @staticmethod
    def init_from_data(data: List[List[Optional[int]]]) -> Field:
        cells = []
        for row_index, row in enumerate(data):
            cell_row = []
            for column_index, value in enumerate(row):
                cell_row.append(Cell(value, column_index, row_index))
            cells.append(cell_row)
        return Field(cells)


if __name__ == '__main__':
    field_data = []
    step = 0
    for i in range(9):
        row = []
        for j in range(9):
            row.append(j)
        row = row[step:] + row[:step]
        field_data.append(row)
        step += 3
        if step >= 9:
            step -= 8
    for row in field_data:
        print(row)
    field = Field.init_from_data(field_data)

    print(field.is_valid)
    print()
    for row in field.rows:
        print(row.is_valid)
    print()
    for c in field.columns:
        print(c.is_valid)
    print()
    for row in field.squares:
        for square in row:
            print(square.is_valid)

