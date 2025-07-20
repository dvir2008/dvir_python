import sys

# --- ייצוג הלוח והכלים ---

# מילון הממפה אותיות לכלים
# (Space) = ריק, S = חייל, R = צריח, N = פרש, B = רץ, Q = מלכה, K = מלך
PIECE_SYMBOLS = {
    'r': 'R', 'n': 'N', 'b': 'B', 'q': 'Q', 'k': 'K', 's': 'S',
    'R': 'R', 'N': 'N', 'B': 'B', 'Q': 'Q', 'K': 'K', 'S': 'S',
    '': ' ' # ריבוע ריק
}

# הגדרת צבעי הכלים (לצורך זיהוי פנימי)
WHITE_PIECES = {'R', 'N', 'B', 'Q', 'K', 'S'}
BLACK_PIECES = {'r', 'n', 'b', 'q', 'k', 's'}

# מצב הלוח ההתחלתי (8x8)
# אותיות קטנות - שחור, אותיות גדולות - לבן
# השורה הראשונה (אינדקס 0) היא שורה 8 בשחמט (צד השחורים)
# השורה האחרונה (אינדקס 7) היא שורה 1 בשחמט (צד הלבנים)
board = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['s', 's', 's', 's', 's', 's', 's', 's'],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
]

# --- משתנים גלובליים למצב המשחק ---
current_player = 'white' # 'white' או 'black'

# --- פונקציות עזר ---

def print_board():
    """מדפיס את הלוח הנוכחי לטרמינל."""
    print("\n   a b c d e f g h")
    print("  -----------------")
    for r_idx, row in enumerate(board):
        display_row = [PIECE_SYMBOLS[p] for p in row]
        print(f"{8 - r_idx} |{' '.join(display_row)}| {8 - r_idx}")
    print("  -----------------")
    print("   a b c d e f g h\n")

def get_piece_at(row, col):
    """מחזיר את הכלי במיקום נתון (או מחרוזת ריקה אם אין כלי)."""
    if 0 <= row < 8 and 0 <= col < 8:
        return board[row][col]
    return '' # מחוץ ללוח

def is_valid_coordinate(coord_str):
    """בודק אם מחרוזת קואורדינטות (לדוגמה 'A1') תקינה."""
    if len(coord_str) != 2:
        return False
    col_char, row_char = coord_str[0].lower(), coord_str[1]
    
    if not ('a' <= col_char <= 'h' and '1' <= row_char <= '8'):
        return False
    return True

def parse_coordinate(coord_str):
    """ממיר מחרוזת קואורדינטות (לדוגמה 'A1') לאינדקסים (row, col)."""
    col = ord(coord_str[0].lower()) - ord('a')
    row = 8 - int(coord_str[1])
    return row, col

def is_players_piece(piece, player):
    """בודק אם הכלי שייך לשחקן הנוכחי."""
    if player == 'white':
        return piece in WHITE_PIECES
    elif player == 'black':
        return piece in BLACK_PIECES
    return False

def is_opponent_piece(piece, player):
    """בודק אם הכלי שייך ליריב."""
    if piece == '': return False # ריבוע ריק אינו כלי יריב
    if player == 'white':
        return piece in BLACK_PIECES
    elif player == 'black':
        return piece in WHITE_PIECES
    return False

# --- פונקציית מהלך המשחק המרכזית ---
def make_move(start_coord_str, end_coord_str):
    """
    מבצע מהלך בלוח השחמט.
    (כרגע ללא בדיקות חוקיות מהלך ספציפיות לכלי).
    """
    global current_player

    if not is_valid_coordinate(start_coord_str) or not is_valid_coordinate(end_coord_str):
        print("קואורדינטות לא חוקיות. אנא השתמש בפורמט כמו 'A2' 'A3'.")
        return False

    start_row, start_col = parse_coordinate(start_coord_str)
    end_row, end_col = parse_coordinate(end_coord_str)

    piece_to_move = get_piece_at(start_row, start_col)
    destination_piece = get_piece_at(end_row, end_col)

    if piece_to_move == '':
        print("אין כלי במיקום ההתחלה.")
        return False

    if not is_players_piece(piece_to_move, current_player):
        print(f"זה לא הכלי של {current_player}. אנא הזז כלי משלך.")
        return False

    if is_players_piece(destination_piece, current_player):
        print("אינך יכול להזיז כלי לריבוע עם כלי משלך.")
        return False
    
    # --- בדיקות בסיסיות מאוד (ללא חוקי שחמט אמיתיים) ---
    # בשלב זה, כל תנועה היא 'חוקית' כל עוד:
    # 1. אתה מזיז כלי משלך.
    # 2. אינך מזיז אותו לריבוע עם כלי משלך.
    # 3. המהלך מתרחש על הלוח.

    # העברת הכלי
    board[end_row][end_col] = piece_to_move
    board[start_row][start_col] = '' # השאר את המיקום ההתחלתי ריק

    print(f"המהלך {start_coord_str} ל- {end_coord_str} בוצע בהצלחה.")
    return True

def switch_player():
    """מחליף את השחקן הנוכחי."""
    global current_player
    if current_player == 'white':
        current_player = 'black'
    else:
        current_player = 'white'

# --- לולאת המשחק הראשית ---
def run_game():
    print("ברוך הבא למשחק שחמט פשוט!")
    print("כדי להזיז כלי, הקלד קואורדינטות התחלה וסיום (לדוגמה: A2 A3).")
    print("הקלד 'יציאה' כדי לצאת מהמשחק.")

    while True:
        print_board()
        print(f"תורו של השחקן {current_player}.")

        try:
            move_input = input("הכנס מהלך (לדוגמה A2 A3): ").strip().upper()

            if move_input == "יציאה":
                print("המשחק נגמר. להתראות!")
                sys.exit()

            parts = move_input.split()
            if len(parts) != 2:
                print("פורמט מהלך שגוי. אנא הקלד שתי קואורדינטות מופרדות ברווח.")
                continue

            start_coord, end_coord = parts[0], parts[1]

            if make_move(start_coord, end_coord):
                switch_player() # רק אם המהלך בוצע בהצלחה, העבר תור
            else:
                print("נסה מהלך אחר.")

        except Exception as e:
            print(f"שגיאה בלתי צפויה: {e}. אנא נסה שוב.")
            # למטרת דיבוג, אפשר להדפיס את השגיאה המלאה: traceback.print_exc()

# --- הפעלת המשחק ---
if __name__ == "__main__":
    run_game()