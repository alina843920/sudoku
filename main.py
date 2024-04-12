class Sudoku:
    def __init__(self, board: list[list[int | None]]) -> None:
        """
        Sudoku initializer

        Args:
            board (list[list[int | None]]): The initial board: list of rows. Each row is a list of 9 integers or None.
        """

        # We need to store column-wise to make indexing logical

        self.initial_board = [
            [int(e) if e else None for e in column] for column in zip(*board)
        ]
        self.solution = [
            [int(e) if e else None for e in column] for column in zip(*board)
        ]

    def check(self) -> bool:
        """
        Check if the board is valid.

        Returns:
            bool: True if the board is valid, False otherwise.
        """

        return all(
            valid
            for idx in range(9)
            for valid in [
                self.check_row(idx),
                self.check_column(idx),
            ]
        ) and all(self.check_nine_square(x, y) for x in range(3) for y in range(3))

    def get_row(self, idx: int) -> list[int]:
        """
        Get the row at the given index.

        Args:
            idx (int): The index of the row.

        Returns:
            list[int]: The row.
        """
        return [column[idx] for column in self.solution]

    def get_column(self, idx: int) -> list[int]:
        """
        Get the column at the given index.

        Args:
            idx (int): The index of the column.

        Returns:
            list[int]: The column.
        """
        return self.solution[idx]

    def get_nine_square(self, x: int, y: int) -> list[list[int]]:
        """
        Get the 3x3 square at the given index.

        Args:
            x (int): The x index of the 3x3 square.
            y (int): The y index of the 3x3 square.

        Returns:
            list[list[int]]: The 3x3 square.
        """
        return [row[3 * y : 3 * y + 3] for row in self.solution[3 * x : 3 * x + 3]]

    def check_row(self, row: int) -> bool:
        """
        Check if the row is valid.

        Args:
            row (int): The index of the row.

        Returns:
            bool: True if the row is valid, False otherwise.
        """
        return set(self.get_row(row)) == set(range(1, 10))

    def check_column(self, column: int) -> bool:
        """
        Check if the column is valid.

        Args:
            column (int): The index of the column.

        Returns:
            bool: True if the column is valid, False otherwise.
        """
        return set(self.get_column(column)) == set(range(1, 10))

    def check_nine_square(self, x: int, y: int) -> bool:
        """
        Check if the 3x3 square is valid.

        Args:
            x (int): The x index of the 3x3 square.
            y (int): The y index of the 3x3 square.

        Returns:
            bool: True if the 3x3 square is valid, False otherwise.
        """

        return set(value for row in self.get_nine_square(x, y) for value in row) == set(
            range(1, 10)
        )

    def solve(self):
        def is_valid_move(x, y, num):
            for i in range(9):
                if self.solution[x][i] == num:
                    return False
                if self.solution[i][y] == num:
                    return False
                if self.solution[(x // 3) * 3 + i // 3][(y // 3) * 3 + i % 3] == num:
                    return False
            return True

        def solve_sudoku():
            for i in range(9):
                for j in range(9):
                    if self.solution[i][j] is None:
                        for num in range(1, 10):
                            if is_valid_move(i, j, num):
                                self.solution[i][j] = num
                                if solve_sudoku():
                                    return True
                                self.solution[i][j] = None
                        return False
            return True

        solve_sudoku()
        return self.solution

    def __repr__(self) -> str:
        interleave = lambda line, data: f"{line}{data}" * 2 + line

        horizontal_line = (
            lambda left_corner, horizontal_line, thin_center_corner, center_corner, right_corner: f"{left_corner}{interleave(interleave(horizontal_line * 3, thin_center_corner), center_corner)}{right_corner}\n"
        )

        green = lambda x: f"\033[32m{x}\033[0m"
        yellow = lambda x: f"\033[33m{x}\033[0m"

        # yellow = green = lambda x: f"{x}"

        table: str = (
            horizontal_line("╔", "═", "╤", "╦", "╗")
            + interleave(
                interleave(
                    "║ %s │ %s │ %s " * 3 + "║\n",
                    horizontal_line("╟", "─", "┼", "╫", "╢"),
                ),
                horizontal_line("╠", "═", "╪", "╬", "╣"),
            )
            + horizontal_line("╚", "═", "╧", "╩", "╝")
        ) % tuple(
            (green(x_solved) if x_solved else " ") if x_initial is None else x_initial
            for row_solved, row_initial in zip(
                zip(*self.solution), zip(*self.initial_board)
            )
            for x_solved, x_initial in zip(row_solved, row_initial)
        )

        x_coords = 4 * " " + (3 * " ").join(yellow(i) for i in range(9))

        coordinated_table = "\n".join(
            [x_coords]
            + list(
                f"{yellow(i//2) if i%2 else ' '} {row}"
                for i, row in enumerate(table.splitlines())
            )
        )

        return coordinated_table


if __name__ == "__main__":
    _ = None
    s = Sudoku(
         [
             [4, 1, _, 3, _, 6, _, 9, 7],
             [6, _, _, 7, _, _, _, 5, _],
             [_, _, _, _, _, _, _, _, _],
             [_, _, 9, _, 7, 3, _, _, 2],
             [_, _, 8, _, _, _, 9, _, _],
             [7, _, _, 9, 8, _, 6, _, _],
             [_, _, _, _, _, _, _, _, _],
             [_, 3, _, _, _, 8, _, _, 6],
             [9, 5, _, 6, _, 7, _, 3, 8],
         ]

    )

    print(s)

    s.solve()
    print(s)
