"""Another go at a Saturday Tetris hack.

Reference:
    tetris.wiki/Tetris_Guideline

For colors (which I got from chatGPT) asking for a Mexican theme colour scheme:
    Terracotta Orange: A warm, earthy orange that resembles traditional terracotta pottery.
    RGB: (204, 102, 51)
    Name: "Cantina Clay"

    Cactus Green: A vibrant green that you might see on desert flora.
    RGB: (0, 153, 76)
    Name: "Agave Green"

    Sunset Pink: A deep, rosy pink that captures the colors of a desert sunset.
    RGB: (225, 107, 140)
    Name: "Fiesta Fuchsia"

    Sky Blue: A clear, bright blue reminiscent of the expansive Mexican skies.
    RGB: (102, 204, 255)
    Name: "Azul Horizon"

    Adobe White: A soft, off-white with a hint of warmth, similar to adobe walls.
    RGB: (255, 248, 220)
    Name: "Pueblo White"

    Sandy Gold: A rich, golden yellow that evokes the hues of a sun-drenched desert.
    RGB: (255, 204, 51)
    Name: "Sol Dorado"

    Ocean Teal: A deep teal reflecting the depth and beauty of the ocean, often celebrated in coastal Mexican regions.
    RGB: (0, 128, 128)
    Name: "Mar Azteca"

    Vibrant Red: A bold and spicy red that brings to mind Mexican textiles and chili peppers.
    RGB: (204, 0, 0)
    Name: "Chili Rojo"
"""
import pygame
import random
import sys

# Constants
BLACK = (0, 0, 0)
NEAR_BLACK = (20, 10, 5)
CONTINA_CLAY = (204, 102, 51)

AGAVE_GREEN = (0, 153, 76)
FIESTA_FUCHSIA = (225, 107, 140)
AZUL_HORIZON = (102, 204, 255)
PUEBLO_WHITE = (255, 248, 220)
SOL_DORADO = (255, 204, 51)
MAR_AZTECA = (0, 128, 128)
CHILI_ROJO = (204, 0, 0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SURFACE_WIDTH = 200
SCOREBOARD_LEFT_OFFSET = 20
SCOREBOARD_WIDTH = 200
SCOREBOARD_HEIGHT = 150
SCOREBOARD_FONT_SIZE = 52
SCOREBOARD_PLACEMENT = (20, 30)
NUM_BLOCKS_WIDTH = 10
NUM_BLOCKS_HEIGHT = 20
SURFACE_HEIGHT = 400
FPS = 60
TETROMINO_BLOCK_SIZE = 20
BOTTOM_OF_BOARD = 20

GAME_STATE_NEW_TETROMINO = 0
GAME_STATE_FALLING = 1
GAME_STATE_GAME_OVER = -1

START_POSITION_LEFT_OFFSET = 3
START_POSITION_TOP_offset = 0

TETROMINO_ORIENTATION_0 = 0
TETROMINO_ORIENTATION_270 = 1
TETROMINO_ORIENTATION_180 = 2
TETROMINO_ORIENTATION_90 = 3

MOVE_CANNOT_BE_DONE = 0
MOVE_ENDS_GAME = 1
MOVE_CAN_BE_DONE = 2
MOVE_SETTLES_BLOCK = 3

MOVE_LEFT = -1
MOVE_RIGHT = 1

EMPTY_BLOCK = -1
IS_ROTATING = True

NONE, SINGLE, DOUBLE, TRIPLE, TETRIS = 0, 100, 300, 500, 800


class TetrominoTypes:
    """Each type of Tetromino with a color and turning orientations"""
    TETROMINO_T = {
        'orientations': {
            0: [(0, 0), (1, 0), (2, 0), (1, 1)],
            1: [(1, -1), (0, 0), (1, 0), (1, 1)],
            2: [(1, 0), (0, 1), (1, 1), (2, 1)],
            3: [(1, -1), (1, 0), (2, 0), (1, 1)]
        },
        'color': CHILI_ROJO
    }
    TETROMINO_I = {
        'orientations': {
            0: [(0, 0), (1, 0), (2, 0), (3, 0)],
            1: [(2, -1), (2, 0), (2, 1), (2, 2)],
            2: [(0, 0), (1, 0), (2, 0), (3, 0)],
            3: [(2, -1), (2, 0), (2, 1), (2, 2)],
        },
        'color': AGAVE_GREEN
    }
    TETROMINO_J = {
        'orientations': {
            0: [(0, 0), (1, 0), (2, 0), (2, 1)],
            1: [(1, -1), (1, 0), (0, 1), (1, 1)],
            2: [(0, 0), (0, 1), (1, 1), (2, 1)],
            3: [(1, -1), (2, -1), (1, 0), (1, 1)]
        },
        'color': FIESTA_FUCHSIA
    }
    TETROMINO_L = {
        'orientations': {
            0: [(0, 0), (1, 0), (2, 0), (0, 1)],
            1: [(0, -1), (1, -1), (1, 0), (1, 1)],
            2: [(2, 0), (0, 1), (1, 1), (2, 1)],
            3: [(1, -1), (1, 0), (1, 1), (2, 1)]
        },
        'color': AZUL_HORIZON
    }
    TETROMINO_O = {
        'orientations': {
            0: [(1, 0), (2, 0), (1, 1), (2, 1)],
            1: [(1, 0), (2, 0), (1, 1), (2, 1)],
            2: [(1, 0), (2, 0), (1, 1), (2, 1)],
            3: [(1, 0), (2, 0), (1, 1), (2, 1)]
        },
        'color': PUEBLO_WHITE
    }
    TETROMINO_S = {
        'orientations': {
            0: [(1, 0), (2, 0), (0, 1), (1, 1)],
            1: [(0, -1), (0, 0), (1, 0), (1, 1)],
            2: [(1, 0), (2, 0), (0, 1), (1, 1)],
            3: [(0, -1), (0, 0), (1, 0), (1, 1)]
        },
        'color': SOL_DORADO
    }
    TETROMINO_Z = {
        'orientations': {
            0: [(0, 0), (1, 0), (1, 1), (2, 1)],
            1: [(2, -1), (1, 0), (2, 0), (1, 1)],
            2: [(0, 0), (1, 0), (1, 1), (2, 1)],
            3: [(2, -1), (1, 0), (2, 0), (1, 1)]
        },
        'color': MAR_AZTECA
    }


class TetrominoChoices:
    """The Tetrominos that we have in an easy way to pick one randomly"""
    CHOICES = [
        TetrominoTypes.TETROMINO_Z,
        TetrominoTypes.TETROMINO_S,
        TetrominoTypes.TETROMINO_I,
        TetrominoTypes.TETROMINO_L,
        TetrominoTypes.TETROMINO_O,
        TetrominoTypes.TETROMINO_J,
        TetrominoTypes.TETROMINO_T
    ]


class TetrominoBoard:
    """Control the board as a set of blocks.

    A tetromino basically only exists when it's falling.  When it settles,
    it simply becomes a block.
    """
    def __init__(self):
        self.board = [self._empty_line_utility() for _ in range(NUM_BLOCKS_HEIGHT)]
        self._falling_tetromino = None
        self._falling_tetromino_orientation = TETROMINO_ORIENTATION_0
        self._falling_tetromino_top_offset = None
        self._falling_tetromino_left_offset = None

    @staticmethod
    def _empty_line_utility():
        return [EMPTY_BLOCK for _ in range(NUM_BLOCKS_WIDTH)]

    def _is_move_possible(self, new_positions, old_positions, move_is_spin=False):
        """Check if move is possible.

        The way that this works is just taking the ghost of where the block would move
        and seeing if that's valid.

        :param new_positions: List of tuples containing the blocks where the tetromino will go.
        :param old_positions: List of tuples containing the positions the tetromino currently is.
        :return: validity of the move.
        """
        for top, left in new_positions:

            # The move would go off the screen
            if left < 0 or left >= NUM_BLOCKS_WIDTH or top > BOTTOM_OF_BOARD:
                return MOVE_CANNOT_BE_DONE

            # The move would land the block
            if top == BOTTOM_OF_BOARD:
                return MOVE_SETTLES_BLOCK

            # The move would land on another piece
            if self.board[top][left] != EMPTY_BLOCK and (top, left) not in old_positions:
                if move_is_spin:
                    return MOVE_CANNOT_BE_DONE

                return MOVE_SETTLES_BLOCK

        return MOVE_CAN_BE_DONE

    def _update_board_remove(self, positions):
        """Remove blocks per position

        :param positions: List of tuples of positions to be turned into empty blocks.
        """
        for top, left in positions:
            self.board[top][left] = EMPTY_BLOCK

    def _update_board_add(self, positions, color):
        """Add blocks to the board.  A position is a block if it has a color.

        :param positions: List of tuples of positions to be turned into tetromino blocks.
        :param color: Tuple of the RGB colors to assign to the squares.
        """
        for top, left in positions:
            self.board[top][left] = color

    def _update_orientation(self):
        """Start a new active tetromino in the game.

        :return: potential new orientation.
        """
        orientations = [
            TETROMINO_ORIENTATION_0,
            TETROMINO_ORIENTATION_270,
            TETROMINO_ORIENTATION_180,
            TETROMINO_ORIENTATION_90
        ]
        potential_orientation = orientations[0]
        current_index = orientations.index(self._falling_tetromino_orientation)

        if current_index < (len(orientations) - 1):
            potential_orientation = orientations[current_index + 1]

        return potential_orientation

    def rotate_tetromino(self):
        """If possible, rotate tetromino"""
        potential_orientation = self._update_orientation()

        positions_old = [
            (top + self._falling_tetromino_top_offset, left + self._falling_tetromino_left_offset)
            for left, top in self._falling_tetromino['orientations'][self._falling_tetromino_orientation]
        ]
        positions_new = [
            (top + self._falling_tetromino_top_offset, left + self._falling_tetromino_left_offset)
            for left, top in self._falling_tetromino['orientations'][potential_orientation]
        ]

        if self._is_move_possible(positions_new, positions_old, IS_ROTATING) == MOVE_CAN_BE_DONE:
            self._update_board_remove(positions_old)
            self._update_board_add(
                positions_new,
                self._falling_tetromino['color'])

            self._falling_tetromino_orientation = potential_orientation

    def move_tetromino(self, direction):
        """Move the falling tetromino left or right

        :param direction: Int, Direction offset to apply to the falling tetromino.
        """
        positions_old = [
            (top + self._falling_tetromino_top_offset, left + self._falling_tetromino_left_offset)
            for left, top in self._falling_tetromino['orientations'][self._falling_tetromino_orientation]
        ]
        positions_new = [
            (top + self._falling_tetromino_top_offset, left + self._falling_tetromino_left_offset + direction)
            for left, top in self._falling_tetromino['orientations'][self._falling_tetromino_orientation]
        ]

        if self._is_move_possible(positions_new, positions_old) == MOVE_CAN_BE_DONE:
            self._update_board_remove(positions_old)
            self._update_board_add(
                positions_new,
                self._falling_tetromino['color'])

            self._falling_tetromino_left_offset += direction

    def start_new_tetromino(self):
        """Start a new active tetromino in the game.

        :return: Move outcome
        """
        self._falling_tetromino_top_offset = START_POSITION_TOP_offset
        self._falling_tetromino_left_offset = START_POSITION_LEFT_OFFSET
        self._falling_tetromino = random.choice(TetrominoChoices.CHOICES)
        self._falling_tetromino_orientation = TETROMINO_ORIENTATION_0

        positions = [
            (top + self._falling_tetromino_top_offset, left + self._falling_tetromino_left_offset)
            for left, top in self._falling_tetromino['orientations'][self._falling_tetromino_orientation]
        ]

        if self._is_move_possible(positions, list()) == MOVE_CAN_BE_DONE:
            self._update_board_add(
                positions,
                self._falling_tetromino['color'])
            return MOVE_CAN_BE_DONE

        return MOVE_ENDS_GAME

    def falling_tetromino(self):
        """Let the current tetromino fall, if it has space to fall into.

        :return: Move outcome
        """
        positions_old = [
            (top + self._falling_tetromino_top_offset, left + self._falling_tetromino_left_offset)
            for left, top in self._falling_tetromino['orientations'][self._falling_tetromino_orientation]
        ]
        positions_new = [
            (top + self._falling_tetromino_top_offset + 1, left + self._falling_tetromino_left_offset)
            for left, top in self._falling_tetromino['orientations'][self._falling_tetromino_orientation]
        ]
        
        move_possible_outcome = self._is_move_possible(positions_new, positions_old)

        if move_possible_outcome == MOVE_SETTLES_BLOCK:
            return MOVE_SETTLES_BLOCK

        if move_possible_outcome == MOVE_CAN_BE_DONE:
            self._update_board_remove(positions_old)
            self._falling_tetromino_top_offset += 1
            self._update_board_add(
                positions_new,
                self._falling_tetromino['color'])

        return move_possible_outcome

    def update_lines_and_score(self):
        """Update score if any lines are complete.

        Any lines that score are removed.  Empty lines are added at the top to replace them.

        Scores
        ======
        Single  100 × level
        Double  300 × level
        Triple  500 × level
        Tetris  800 × level

        :return: The score this round.
        """
        scores = (NONE, SINGLE, DOUBLE, TRIPLE, TETRIS)
        scoring_lines = 0
        indexes_to_remove = []

        for index, level in enumerate(self.board):
            if all(block != -1 for block in level):
                scoring_lines += 1
                indexes_to_remove.append(index)

        if scoring_lines:
            for index in reversed(indexes_to_remove):
                del self.board[index]

            self.board = [self._empty_line_utility() for _ in range(scoring_lines)] + self.board

        return scores[scoring_lines]


def update(play_state):
    """Update what happens in the game in this round.

    :param play_state: State of play
    :return: Updated state
    """
    state = play_state
    score = 0

    if play_state == GAME_STATE_NEW_TETROMINO:
        move_success = board.start_new_tetromino()
        if move_success == MOVE_CAN_BE_DONE:
            state = GAME_STATE_FALLING
        else:
            state = GAME_STATE_GAME_OVER

    elif play_state == GAME_STATE_FALLING:
        move_success = board.falling_tetromino()
        if move_success == MOVE_CAN_BE_DONE:
            state = GAME_STATE_FALLING
        elif move_success == MOVE_SETTLES_BLOCK:
            state = GAME_STATE_NEW_TETROMINO
        else:
            state = GAME_STATE_GAME_OVER

    if state == GAME_STATE_NEW_TETROMINO:
        score = board.update_lines_and_score()

    return state, score


def add_game_rectangle(color, block_offset_height, block_offset_width, width):
    """Utility to add rectangles.

    :param color: Tuple, RGB for the color to apply.
    :param block_offset_height: Int, top offset.
    :param block_offset_width: Int, left offset.
    :param width: Int. Width of border.  Zero to fill block.
    """
    pygame.draw.rect(
        inner_surface,
        color,
        (block_offset_width * TETROMINO_BLOCK_SIZE,
         block_offset_height * TETROMINO_BLOCK_SIZE,
         TETROMINO_BLOCK_SIZE,
         TETROMINO_BLOCK_SIZE),
        width)


def draw(game_screen, display_score, font):
    """Draw updated screen.

    :param game_screen: Pygame display object for screen.
    :param display_score: Int.  Current score.
    :param font: Pygame font object for score board.
    """
    game_screen.fill(CONTINA_CLAY)
    game_screen.blit(inner_surface, ((SCREEN_WIDTH - SURFACE_WIDTH) // 2, (SCREEN_HEIGHT - SURFACE_HEIGHT) // 2))
    game_screen.blit(score_board, (SCOREBOARD_LEFT_OFFSET, (SCREEN_HEIGHT - SURFACE_HEIGHT) // 2))

    score_board.fill(NEAR_BLACK)
    score_board_data = font.render(f"{display_score}", True, CONTINA_CLAY)
    score_board.blit(score_board_data, SCOREBOARD_PLACEMENT)

    for block_offset_width in range(0, NUM_BLOCKS_WIDTH):
        for block_offset_height in range(0, NUM_BLOCKS_HEIGHT):
            block_color = BLACK
            setting = board.board[block_offset_height][block_offset_width]

            if setting != EMPTY_BLOCK:
                block_color = setting

            # Draw blocks
            add_game_rectangle(block_color, block_offset_height, block_offset_width, 0)
            # Outline blocks, just for looks.
            add_game_rectangle(NEAR_BLACK, block_offset_height, block_offset_width, 1)

    pygame.display.update()


def key_events(keys, score):
    """Handle input from player.

    :param keys: Pygame event key object.
    :param score: Current game score to return on termination of game.
    """
    if keys[pygame.K_UP]:
        board.rotate_tetromino()
    if keys[pygame.K_LEFT]:
        board.move_tetromino(MOVE_LEFT)
    if keys[pygame.K_RIGHT]:
        board.move_tetromino(MOVE_RIGHT)
    if keys[pygame.K_q]:
        terminate(score)


def terminate(score, message='Game Over'):
    """End game

    TODO: create end game screen.

    :param score: Int.  Game score on termination.
    :param message: String.  Message to display on game termination.
    """
    print(f"{message} | Score {score}")
    # Clean up
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris Clone Attempt')

    inner_surface = pygame.Surface((SURFACE_WIDTH, SURFACE_HEIGHT))
    inner_surface.fill(BLACK)

    score_board = pygame.Surface((SCOREBOARD_WIDTH, SCOREBOARD_HEIGHT))
    score_board.fill(NEAR_BLACK)
    game_font = pygame.font.SysFont('didot.ttc', SCOREBOARD_FONT_SIZE)

    board = TetrominoBoard()
    game_state = GAME_STATE_NEW_TETROMINO

    clock = pygame.time.Clock()

    game_score = 0
    clock_counter = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate(game_score)
            if event.type == pygame.KEYDOWN:
                key_events(pygame.key.get_pressed(), game_score)

        # TODO: There's probably a better way to stagger time in pygame.  This is my solution for now.
        if clock_counter % 15 == 0:
            clock_counter = 0
            game_state, score_this_round = update(game_state)
            game_score += score_this_round

            if game_state == GAME_STATE_GAME_OVER:
                running = False
                terminate(game_score)

        clock_counter += 1

        draw(screen, game_score, game_font)

        pygame.display.flip()
        clock.tick(FPS)
