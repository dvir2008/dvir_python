import turtle
import time
import random

# --- הגדרות משחק ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_LEVEL = -100 # קו הקרקע של הדינוזאור והקקטוסים

# דינוזאור וקפיצה
JUMP_HEIGHT = 15    # מהירות קפיצה ראשונית (כמה גבוה הוא מתחיל לעלות)
GRAVITY = 0.8       # כוח הכבידה (ככל שיותר גדול, הדינוזאור נופל מהר יותר)
dino_x_pos = -SCREEN_WIDTH / 4 # מיקום קבוע של הדינוזאור על ציר X

# אויבים (קקטוסים וציפורים)
CACTUS_SPEED_INITIAL = 10 # מהירות התחלתית של קקטוסים וציפורים
GAME_SPEED_INCREASE_FACTOR = 0.0005 # קצב הגברת מהירות המשחק עם הניקוד

# ניקוד
score = 0
high_score = 0
game_over = False
is_jumping = False
y_velocity = 0 # מהירות אנכית לקפיצה
current_game_speed = CACTUS_SPEED_INITIAL # מהירות המשחק הנוכחית

# מחזור יום/לילה
DAY_SCORE_THRESHOLD = 700 # ניקוד שבו מתחיל לילה
NIGHT_DURATION_SCORE = 300 # משך הלילה בניקוד
is_night = False
night_start_score = 0

# --- הגדרת המסך ---
wn = turtle.Screen()
wn.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
wn.bgcolor("skyblue") # צבע שמיים (יום)
wn.title("Dino Run (Turtle Edition)")
wn.tracer(0) # כבה עדכוני מסך אוטומטיים

# --- יצירת קו הקרקע ---
ground = turtle.Turtle()
ground.speed(0)
ground.shape("square")
ground.color("sienna") # צבע אדמה (יום)
ground.penup()
ground.shapesize(stretch_wid=1, stretch_len=SCREEN_WIDTH / 20)
ground.goto(0, GROUND_LEVEL - 10)

# --- יצירת הדינוזאור ---
dino = turtle.Turtle()
dino.speed(0)
dino.shape("square")
dino.color("forestgreen") # ירוק כהה (דינו)
dino.penup()
dino.shapesize(stretch_wid=2, stretch_len=1)
dino.goto(dino_x_pos, GROUND_LEVEL)

# --- רשימת אויבים (קקטוסים וציפורים) ---
obstacles = [] # רשימה מאוחדת לקקטוסים וציפורים

# --- פאנל ניקוד ---
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("black") # צבע טקסט (יום)
pen.penup()
pen.hideturtle()
pen.goto(0, SCREEN_HEIGHT / 2 - 40)
pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 18, "normal"))

# --- פונקציות משחק ---

def jump():
    """מפעיל את קפיצת הדינוזאור."""
    global is_jumping, y_velocity, game_over
    if not is_jumping and not game_over:
        is_jumping = True
        y_velocity = JUMP_HEIGHT # הגובה הראשוני של הקפיצה (מהירות כלפי מעלה)

def change_colors(is_night_mode):
    """משנה את צבעי הרקע והאובייקטים למצב יום/לילה."""
    if is_night_mode:
        wn.bgcolor("#2F3F4A") # כחול כהה (לילה)
        ground.color("#4A3F2F") # חום כהה יותר לאדמה
        dino.color("darkgreen") # דינו מעט כהה יותר
        pen.color("lightgray")  # טקסט בהיר ללילה
        # לשנות צבעי קקטוסים וציפורים קיימים
        for obs in obstacles:
            if obs.shape() == "square": # קקטוס
                obs.color("gray")
            else: # ציפור (משולש)
                obs.color("lightgray")
    else: # מצב יום
        wn.bgcolor("skyblue")
        ground.color("sienna")
        dino.color("forestgreen")
        pen.color("black")
        for obs in obstacles:
            if obs.shape() == "square": # קקטוס
                obs.color("brown")
            else: # ציפור
                obs.color("black")


def reset_game():
    """מאפס את כל מצב המשחק."""
    global score, game_over, is_jumping, y_velocity, current_game_speed
    global is_night, night_start_score

    score = 0
    game_over = False
    is_jumping = False
    y_velocity = 0
    current_game_speed = CACTUS_SPEED_INITIAL # איפוס מהירות משחק
    is_night = False
    night_start_score = 0
    change_colors(False) # וודא שהרקע חוזר ליום

    dino.goto(dino_x_pos, GROUND_LEVEL)

    # הסרת כל האויבים הקיימים
    for obs in obstacles:
        obs.hideturtle()
        obs.clear()
    obstacles.clear()

    pen.clear()
    pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 18, "normal"))

# --- קישורי מקשים ---
wn.listen()
wn.onkeypress(jump, "space") # קפיצה בלחיצה על מקש רווח
wn.onkeypress(reset_game, "r") # איפוס המשחק בלחיצה על R

# --- לולאת המשחק הראשית ---
last_obstacle_spawn_time = time.time()
score_update_time = time.time()

while True:
    if not game_over:
        # --- טיפול בקפיצה ---
        if is_jumping:
            dino.sety(dino.ycor() + y_velocity)
            y_velocity -= GRAVITY # הפחתה במהירות עקב כבידה

            if dino.ycor() <= GROUND_LEVEL: # אם הדינוזאור נוחת על הקרקע
                dino.sety(GROUND_LEVEL)
                is_jumping = False
                y_velocity = 0

        # --- יצירת אויבים (קקטוסים וציפורים) ---
        # אויבים יופיעו במרווחי זמן אקראיים
        if time.time() - last_obstacle_spawn_time > random.uniform(1.2, 3): # מרווח בין 1.2 ל-3 שניות
            new_obstacle = turtle.Turtle()
            new_obstacle.speed(0)
            new_obstacle.penup()

            obstacle_type = random.choice(["cactus", "bird"]) # בחירה אקראית

            if obstacle_type == "cactus":
                new_obstacle.shape("square")
                new_obstacle.shapesize(stretch_wid=random.uniform(1.5, 2.5), stretch_len=0.5)
                new_obstacle.goto(SCREEN_WIDTH / 2, GROUND_LEVEL + new_obstacle.shapesize()[0] * 10 - 10)
                new_obstacle.color("brown" if not is_night else "gray") # צבע לפי יום/לילה
            else: # bird
                new_obstacle.shape("triangle") # ייצוג לציפור
                new_obstacle.shapesize(stretch_wid=0.8, stretch_len=1.2) # גודל יחסי של ציפור
                # מיקום אקראי בגובה הטיסה
                bird_y_pos = random.choice([GROUND_LEVEL + 50, GROUND_LEVEL + 80])
                new_obstacle.goto(SCREEN_WIDTH / 2, bird_y_pos)
                new_obstacle.color("black" if not is_night else "lightgray") # צבע לפי יום/לילה
            
            obstacles.append(new_obstacle)
            last_obstacle_spawn_time = time.time()

        # --- הזזת אויבים ובדיקת התנגשות ---
        for obs in list(obstacles): # העתק את הרשימה כדי למנוע שגיאות בעת מחיקה
            obs.setx(obs.xcor() - current_game_speed)

            # בדיקת התנגשות
            # המרחק יכול להיות שונה לקקטוס וציפור בהתאם לצורה.
            # נשתמש בטווח כללי.
            # dino_half_width = dino.shapesize()[1] * 10 # רוחב 20, חצי 10
            # dino_half_height = dino.shapesize()[0] * 10 # גובה 40, חצי 20
            # obs_half_width = obs.shapesize()[1] * 10
            # obs_half_height = obs.shapesize()[0] * 10

            # בדיקה גסה של חפיפה בין המלבנים (עבור דיוק רב יותר נצטרך חישובים מורכבים יותר)
            # אם יש חפיפה אופקית ואנכית
            dino_left = dino.xcor() - (dino.shapesize()[1] * 10)
            dino_right = dino.xcor() + (dino.shapesize()[1] * 10)
            dino_bottom = dino.ycor() - (dino.shapesize()[0] * 10)
            dino_top = dino.ycor() + (dino.shapesize()[0] * 10)

            obs_left = obs.xcor() - (obs.shapesize()[1] * 10)
            obs_right = obs.xcor() + (obs.shapesize()[1] * 10)
            obs_bottom = obs.ycor() - (obs.shapesize()[0] * 10)
            obs_top = obs.ycor() + (obs.shapesize()[0] * 10)

            # תנאי חפיפה:
            # (rect1.left < rect2.right and rect1.right > rect2.left and
            #  rect1.top > rect2.bottom and rect1.bottom < rect2.top)
            if (dino_left < obs_right and dino_right > obs_left and
                dino_top > obs_bottom and dino_bottom < obs_top):
                
                game_over = True
                pen.clear()
                pen.write(f"GAME OVER! Score: {score}  High Score: {high_score}\nPress 'R' to Restart", align="center", font=("Courier", 18, "normal"))
                break # יציאה מהלולאה הפנימית אם יש התנגשות

            # הסרת אויבים שיצאו מהמסך
            if obs.xcor() < -SCREEN_WIDTH / 2 - 50:
                obs.hideturtle()
                obstacles.remove(obs)

        # --- עדכון ניקוד והגברת מהירות ---
        if time.time() - score_update_time > 0.05: # עדכן ניקוד כל 0.05 שניה
            score += 1
            if score > high_score:
                high_score = score
            
            current_game_speed += GAME_SPEED_INCREASE_FACTOR # הגברת מהירות המשחק באופן הדרגתי

            pen.clear()
            pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 18, "normal"))
            score_update_time = time.time()
        
        # --- מחזור יום/לילה ---
        if not is_night and score >= DAY_SCORE_THRESHOLD:
            is_night = True
            night_start_score = score
            change_colors(True) # עבור ללילה
            print("לילה ירד...")
        elif is_night and score >= night_start_score + NIGHT_DURATION_SCORE:
            is_night = False
            DAY_SCORE_THRESHOLD += 700 # הגדל את סף הלילה הבא
            change_colors(False) # עבור ליום
            print("הבוקר עלה...")


    wn.update() # עדכון המסך
    time.sleep(0.01) # השהייה קטנה לשליטה במהירות הלולאה

# --- השארת החלון פתוח ---
wn.mainloop()