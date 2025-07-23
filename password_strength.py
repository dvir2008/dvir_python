import re

def password_strength():
    x = input("Enter a password: ")
    points = 0
    if len(x) > 8 and len(x) <= 11: #בדיקת אורך
        points += 1
    elif len(x) >= 12:
        points += 2
    
    milim_nefotzot = ["12345678","admin","password","11111111"]

    milim_nefotzot_t_o_f = False
    for i in range(len(milim_nefotzot)):
        if x in milim_nefotzot[i]:
            milim_nefotzot_t_o_f = True
            break
    
    if milim_nefotzot_t_o_f:
        points -= 2
    
    if bool(re.search(r'[A-Z]', x)):#בדיקת אותיות גדולות
        points += 1
    
    if bool(re.search(r'[a-z]', x)):#בדיקת אותיות קטנות
        points += 1
    
    if bool(re.search(r'\d', x)):#בדיקת מספרים
        points += 1
    
    if bool(re.search(r'\W',x)):#בדיקת תווים מיוחדים
        points += 1
    
    if points <= 0: #בדיקת חוזק הסיסמה
        return "Weak password"
    
    elif points >= 1 and points <= 3:
        return "Medium password"
    
    return "Strong password"

print(password_strength())