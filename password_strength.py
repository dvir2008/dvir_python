import re
def password_strength():
    x = input("Enter a password: ")
    points = 0
    if len(x) > 8 and len(x) <= 11: #בדיקת אורך
        points += 1
    elif len(x) >= 12:
        points += 2
    if "12345678" in x or "admin" in x or "password" in x or "11111111" in x: #בדיקת מילים נפוצות כמו1-8 וadmin
        points -= 2 
    
    if bool(re.search(r'[A-Z]', x)):#בדיקת אותיות גדולות
        points += 1
    
    if bool(re.search(r'[a-z]', x)):#בדיקת אותיות קטנות
        points += 1
    
    if bool(re.search(r'\d', x)):#בדיקת מספרים
        points += 1
    
    if bool(re.search(r'\W',x)):#בדיקת תווים מיוחדים
        points += 1
    
    if points <= 0:                                   #בדיקת חוזק הסיסמה
        return "Weak password"
    
    elif points >= 1 and points <= 3:
        return "Medium password"
    
    return "Strong password"

print(password_strength())         
            