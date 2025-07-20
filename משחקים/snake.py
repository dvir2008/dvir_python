import turtle
import time
import random

delay = 0.1 # הגדרת מהירות המשחק (ככל שהמספר קטן יותר, המשחק מהיר יותר)

# הגדרת ניקוד
score = 0
high_score = 0
red_food_eaten_count = 0 # מונה כמה פעמים הנקודה האדומה נאכלה

# --- הגדרת מסך המשחק ---
wn = turtle.Screen()
wn.setup(width=600, height=600) # גודל המסך בפיקסלים
wn.bgcolor("black") # צבע רקע
wn.title("Snake Game") # כותרת החלון באנגלית
wn.tracer(0) # מכבה עדכוני מסך אוטומטיים (לביצועים טובים יותר)

# --- יצירת רשת רקע ---
grid_pen = turtle.Turtle()
grid_pen.speed(0) # מהירות אנימציה מקסימלית
grid_pen.color("gray") # צבע הרשת
grid_pen.penup()
grid_pen.hideturtle() # הסתרת הצב של הרשת
grid_pen.pensize(1) # עובי הקווים

# ציור קווים אנכיים
for x in range(-290, 300, 20):
    grid_pen.goto(x, 290)
    grid_pen.pendown()
    grid_pen.goto(x, -290)
    grid_pen.penup()

# ציור קווים אופקיים
for y in range(-290, 300, 20):
    grid_pen.goto(290, y)
    grid_pen.pendown()
    grid_pen.goto(-290, y)
    grid_pen.penup()

# --- יצירת ראש הנחש ---
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("green")
head.penup()
head.goto(0, 0)
head.shapesize(0.8) # גודל הנחש
head.direction = "stop"

# --- יצירת אוכל רגיל (אדום) ---
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.shapesize(0.8) # גודל האוכל
food.goto(0, 100)

# --- יצירת אוכל מיוחד (ירוק) ---
special_food = turtle.Turtle()
special_food.speed(0)
special_food.shape("circle")
special_food.color("lime") # צבע ירוק בהיר
special_food.penup()
special_food.shapesize(0.8)
special_food.goto(1000, 1000) # מיקום התחלתי מחוץ למסך
special_food.state = "hidden" # מצב האוכל המיוחד (מוסתר / גלוי)
special_food_spawn_time = 0 # זמן הופעת האוכל המיוחד

segments = [] # רשימה לאחסון חלקי גוף הנחש

# --- יצירת פאנל ניקוד ---
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

# --- פונקציות תנועה של הנחש ---
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

# --- קישורי מקשים לשליטה ---
wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")

# --- לולאת המשחק הראשית ---
while True:
    wn.update()

    # בדיקה אם הנחש פגע בקירות
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        time.sleep(1)
        head.goto(0, 0)
        head.direction = "stop"

        # הסתרת אוכל מיוחד אם קיים
        special_food.goto(1000, 1000)
        special_food.state = "hidden"
        red_food_eaten_count = 0 # איפוס מונה הנקודות האדומות

        for segment in segments:
            segment.goto(1000, 1000)
        segments.clear()

        score = 0
        delay = 0.1
        pen.clear()
        pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 24, "normal"))

    # --- בדיקה אם הנחש אכל את האוכל הרגיל (אדום) ---
    if head.distance(food) < 20:
        # העברת האוכל למקום אקראי
        x = random.randrange(-280, 280, 20)
        y = random.randrange(-280, 280, 20)
        food.goto(x, y)

        # הוספת מקטע חדש לגוף הנחש
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("gray")
        new_segment.penup()
        new_segment.shapesize(0.8)
        segments.append(new_segment)

        # הגדלת הניקוד והמהירות
        score += 10
        if delay > 0.05:
            delay -= 0.001
        
        if score > high_score:
            high_score = score
        
        red_food_eaten_count += 1 # הגדל את מונה אכילת האדומים

        # --- בדיקה אם ליצור אוכל מיוחד ---
        if red_food_eaten_count % 5 == 0 and special_food.state == "hidden":
            sx = random.randrange(-280, 280, 20)
            sy = random.randrange(-280, 280, 20)
            special_food.goto(sx, sy)
            special_food.state = "visible"
            special_food_spawn_time = time.time() # שמור את זמן הופעת האוכל המיוחד

        pen.clear()
        pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 24, "normal"))

    # --- בדיקה אם הנחש אכל את האוכל המיוחד (ירוק) ---
    if special_food.state == "visible" and head.distance(special_food) < 20:
        score += 30 # הגדל ניקוד ב-30
        
        # הוסף רק מקטע אחד לגוף (אם יש צורך, ניתן לשנות זאת)
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("gray")
        new_segment.penup()
        new_segment.shapesize(0.8)
        segments.append(new_segment)

        special_food.goto(1000, 1000) # העבר את האוכל המיוחד מחוץ למסך
        special_food.state = "hidden" # שנה את מצבו למוסתר

        if score > high_score:
            high_score = score
        
        pen.clear()
        pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 24, "normal"))

    # --- בדיקה אם עבר זמן האוכל המיוחד (7 שניות) ---
    if special_food.state == "visible" and (time.time() - special_food_spawn_time) > 7:
        special_food.goto(1000, 1000) # העבר את האוכל המיוחד מחוץ למסך
        special_food.state = "hidden" # שנה את מצבו למוסתר
        print("Special food disappeared!") # הודעת דיבאג (אפשר למחוק)

    # הזזת חלקי הגוף - מהסוף להתחלה
    for index in range(len(segments) - 1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)

    # הזזת מקטע 0 (הראשון בגוף) למיקום של הראש
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move() # הזזת ראש הנחש

    # בדיקה אם הנחש פגע בעצמו
    for segment in segments:
        if segment.distance(head) < 20:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"

            # הסתרת אוכל מיוחד אם קיים
            special_food.goto(1000, 1000)
            special_food.state = "hidden"
            red_food_eaten_count = 0 # איפוס מונה הנקודות האדומות

            for seg in segments:
                seg.goto(1000, 1000)
            segments.clear()

            score = 0
            delay = 0.1
            pen.clear()
            pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 24, "normal"))

    time.sleep(delay)

wn.mainloop()