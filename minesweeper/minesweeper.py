import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells

        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells

        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        else:
            pass

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1) mark the cell as a move that has been made
        print(" ")
        print('-----------------NEW MOVE-----------------')
        print('MOVE: ', cell, 'count: ', count)
        self.moves_made.add(cell)

        # 2) mark the cell as safe
        self.mark_safe(cell)

        # 3) add a new sentence  to the AI's knowledge base
        #    based on the value of `cell` and `count`

        # a get all the neighbors of that cell (cells that are not known yet)
        neighbors = set()
        nearby_mines = []

        for i in range(cell[0] -1, cell[0] + 2):
            for j in range(cell[1] -1, cell[1] + 2):
                if i == cell[0] and j == cell[1]:
                    continue
                elif 0 <= i < self.height and 0 <= j < self.width  and (i,j) not in self.safes and (i,j) not in self.moves_made:
                    if (i,j) in self.mines:
                        nearby_mines.append((i,j))
                        continue
                    neighbors.add((i,j))
        print("Neighbors: ", neighbors )
        print(nearby_mines)


        new_sentence = Sentence(cells = neighbors, count = count - len(nearby_mines))
        self.knowledge.append(new_sentence)


        # 4) mark any additional cells as safes or mines if it can be concluded based on the AI knowledge base
        mines = set()
        safes = set()

        # for each sentence in the knowledge base
        for sentence in self.knowledge:

            # this populates the mine list if there are known mines otherwise known_mines returns an empty set and the loop doesn't run
            for mine in sentence.known_mines():
                mines.add(mine)
            # same for safes
            for safe in sentence.known_safes():
                safes.add(safe)
        # add to self.safe or self.mines
        for mine in mines:
            self.mines.add(mine)

        for safe in safes:
            self.safes.add(safe)

        # 5)add any new sentences to the AI's knowledge base if they can be inferred from existing knowledge
        # list of existing sentences
        to_add = []

        # for every sentence in the knowlwdge base
        for old_sentence in self.knowledge:

            # if the new sentence created is not null and the new sentence and the one we are comparing are different
            if new_sentence.cells != set() and old_sentence.cells != new_sentence.cells:

                # if the old one is a subset of the new
                if old_sentence.cells.issubset(new_sentence.cells):
                    to_add.append(Sentence(new_sentence.cells-old_sentence.cells, new_sentence.count-old_sentence.count))

                # if the new one is a subset of the old
                if new_sentence.cells.issubset(old_sentence.cells):
                    to_add.append(Sentence(old_sentence.cells-new_sentence.cells, old_sentence.count-new_sentence.count))

        # add new sentences
        for sentence in to_add:
            self.knowledge.append(sentence)

        # remove useless sentences from knowledge

        # remove sentences that have 0 cells
        for sentence in self.knowledge.copy():
            if len(sentence.cells) == 0:
                self.knowledge.remove(sentence)

        # remove sentences that have 0 mines
        for sentence in self.knowledge.copy():
            if sentence.count == 0:
                self.knowledge.remove(sentence)

        #remove sentences that have all mines
        for sentence in self.knowledge.copy():
            if len(sentence.cells) == sentence.count:
                self.knowledge.remove(sentence)


        print('Moves: ', self.moves_made)
        print("Safes with moves: ", self.safes)
        print("Safes not touched yet: ", self.safes - self.moves_made)
        print("Mines: ", self.mines)
        print('Knowledge Base:')
        for sentence in self.knowledge:
            print(sentence.cells, ' = ', sentence.count)
        print(' ')

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        legal = []

        # remove all the moves that have been made
        for i in self.safes:
            if i not in self.moves_made:
                legal.append(i)


        if len(legal) == 0:
            return None
        else:
            return legal[0]

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible = []
        for i in range(self.height):
            for j in range(self.width):
                possible.append((i,j))

        # remove all the moves that have mines
        # remove all the moves that have already been made
        for i in possible[:]:
            if i in self.mines or i in self.moves_made:
                possible.remove(i)

        # return a random move
        try:
            move = possible[random.randrange(len(possible))]
        except:
            return None
        return move
