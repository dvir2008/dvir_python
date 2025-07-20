import turtle
import random
import time

# --- הגדרות משחק ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 0.5       # כוח הכבידה - כמה מהר הפירות נופלים
# FIX: הגדלת מהירות הקפיצה הראשונית כדי שהפירות יקפצו גבוה יותר
FRUIT_SPEED_INITIAL = 15 # הגדלנו מ-10 ל-15 (אפשר לנסות ערכים גבוהים יותר כמו 20 או 25)
MAX_MISSED_FRUITS = 5 # מספר הפירות המותר לפספס לפני Game Over

# רשימת צבעים וצורות לפירות
FRUIT_TYPES = [
    {"shape": "circle", "color": "red"},    # תפוח/תות
    {"shape": "square", "color": "orange"}, # תפוז/אפרסק
    {"shape": "triangle", "color": "yellow"}, # לימון
    {"shape": "circle", "color": "green"},  # אבטיח/קיווי
    {"shape": "square", "color": "purple"}  # ענבים/שזיף
]

score = 0
missed_fruits = 0
game_over = False

# --- הגדרת המסך ---
wn = turtle.Screen()
wn.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
wn.bgcolor("lightgray")
wn.title("Simple Fruit Ninja (Turtle Edition)")
wn.tracer(0) # כבה עדכוני מסך אוטומטיים

# --- יצירת הסכין (Ninja Blade) ---
blade = turtle.Turtle()
blade.speed(0)
blade.shape("triangle")
blade.color("black")
blade.shapesize(stretch_wid=0.8, stretch_len=0.8)
blade.penup()
blade.goto(0, -SCREEN_HEIGHT / 2 + 50) # מיקום התחלתי בתחתית המסך

# --- פאנל ניקוד ---
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("black")
pen.penup()
pen.hideturtle()
pen.goto(0, SCREEN_HEIGHT / 2 - 40)
pen.write(f"Score: {score}  Missed: {missed_fruits}/{MAX_MISSED_FRUITS}", align="center", font=("Courier", 18, "normal"))

# --- רשימת פירות פעילים ---
active_fruits = []

# --- פונקציות משחק ---

def move_blade_via_tkinter_bind(event):
    if not game_over:
        x = event.x - SCREEN_WIDTH / 2
        y = SCREEN_HEIGHT / 2 - event.y
        blade.goto(x, y)

def spawn_fruit():
    """יוצר פרי חדש ומשגר אותו כלפי מעלה."""
    if game_over: return

    fruit_settings = random.choice(FRUIT_TYPES)
    fruit = turtle.Turtle()
    fruit.speed(0)
    fruit.shape(fruit_settings["shape"])
    fruit.color(fruit_settings["color"])
    fruit.penup()
    
    # הגדלת גודל הפירות (כמו בתיקון הקודם)
    fruit_size_factor_base = 2.0 
    fruit_size_factor_rand = random.uniform(0.8, 1.2) 
    final_fruit_size = fruit_size_factor_base * fruit_size_factor_rand
    
    fruit.shapesize(stretch_wid=final_fruit_size, stretch_len=final_fruit_size)

    # מיקום התחלתי אקראי בתחתית המסך
    start_x = random.randint(-SCREEN_WIDTH // 2 + 50, SCREEN_WIDTH // 2 - 50)
    fruit.goto(start_x, -SCREEN_HEIGHT / 2 - 20) # מתחיל מתחת למסך

    # מהירות אנכית ואופקית אקראית
    # FRUIT_SPEED_INITIAL הוא הערך הבסיסי למהירות הקפיצה
    fruit_y_velocity = FRUIT_SPEED_INITIAL + random.uniform(-2, 2)
    fruit_x_velocity = random.uniform(-3, 3) # תנועה אופקית קלה
    
    active_fruits.append({"obj": fruit, "y_vel": fruit_y_velocity, "x_vel": fruit_x_velocity, "sliced": False})

def reset_game():
    """מאפס את כל מצב המשחק."""
    global score, missed_fruits, game_over

    score = 0
    missed_fruits = 0
    game_over = False

    for fruit_data in active_fruits:
        fruit_data["obj"].hideturtle()
    active_fruits.clear()

    pen.clear()
    pen.write(f"Score: {score}  Missed: {missed_fruits}/{MAX_MISSED_FRUITS}", align="center", font=("Courier", 18, "normal"))


# --- קישורי עכבר ומקשים ---
wn.listen()
wn.getcanvas().bind('<Motion>', move_blade_via_tkinter_bind)
wn.onkeypress(reset_game, "r") # איפוס המשחק בלחיצה על R

# --- לולאת המשחק הראשית ---
last_fruit_spawn_time = time.time()
fruit_spawn_interval = 1.5 # מרווח התחלתי בין פירות

while True:
    if not game_over:
        # --- יצירת פירות ---
        if time.time() - last_fruit_spawn_time > fruit_spawn_interval:
            spawn_fruit()
            fruit_spawn_interval = max(0.5, fruit_spawn_interval * 0.98) 
            last_fruit_spawn_time = time.time()

        # --- הזזת פירות ובדיקת חיתוך/נפילה ---
        fruits_to_remove = []
        for fruit_data in list(active_fruits): 
            fruit_obj = fruit_data["obj"]
            
            fruit_obj.sety(fruit_obj.ycor() + fruit_data["y_vel"])
            fruit_obj.setx(fruit_obj.xcor() + fruit_data["x_vel"])
            
            fruit_data["y_vel"] -= GRAVITY 

            # בדיקת חיתוך (מרחק מוגדל בגלל גודל הפירות)
            if not fruit_data["sliced"] and blade.distance(fruit_obj) < 45: 
                fruit_data["sliced"] = True
                score += 1
                pen.clear()
                pen.write(f"Score: {score}  Missed: {missed_fruits}/{MAX_MISSED_FRUITS}", align="center", font=("Courier", 18, "normal"))
                
                fruit_obj.hideturtle()
                fruits_to_remove.append(fruit_data) 

            # בדיקה אם הפרי יצא מהמסך בתחתית (פספוס)
            if fruit_obj.ycor() < -SCREEN_HEIGHT / 2 - 50 and not fruit_data["sliced"]:
                missed_fruits += 1
                pen.clear()
                pen.write(f"Score: {score}  Missed: {missed_fruits}/{MAX_MISSED_FRUITS}", align="center", font=("Courier", 18, "normal"))
                fruits_to_remove.append(fruit_data) 
                
                if missed_fruits >= MAX_MISSED_FRUITS:
                    game_over = True
                    pen.clear()
                    pen.write(f"GAME OVER! Score: {score}  Missed: {missed_fruits}/{MAX_MISSED_FRUITS}\nPress 'R' to Restart", align="center", font=("Courier", 18, "normal"))

            # בדיקה אם הפרי יצא מהמסך מלמעלה או מהצדדים
            if fruit_obj.ycor() > SCREEN_HEIGHT / 2 + 50 or \
               fruit_obj.xcor() < -SCREEN_WIDTH / 2 - 50 or \
               fruit_obj.xcor() > SCREEN_WIDTH / 2 + 50:
                if fruit_data not in fruits_to_remove: 
                     fruit_obj.hideturtle()
                     fruits_to_remove.append(fruit_data)

        # הסר את הפירות המסומנים מהרשימה
        for fruit_data in fruits_to_remove:
            if fruit_data in active_fruits: 
                fruit_data["obj"].hideturtle() 
                active_fruits.remove(fruit_data)

    wn.update() 
    time.sleep(0.01) 

wn.mainloop()