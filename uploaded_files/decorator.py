class calc:
    def __init__(self,value):
        self.value = value

    def __add__(self, num):
        if isinstance(num,int or float):
            self.value += num
            return self.value
        else:
            return 'please enter a integer or a float'
    
    def __sub__(self, num):
        if isinstance(num,int or float):
            self.value -=num
            return self.value
        else:
            return 'please enter a integer or a float'
    
    def molt(self,num):
        if isinstance(num,int or float):
            self.value *= num
            return self.value
        else:
            return 'please enter a integer or a float'

    def divi(self,num):
        if isinstance(num,int or float):
            self.value /= num
            return self.value
        else:
            return 'please enter a integer or a float'
    def squr(self,num):
        if isinstance(num,int or float):
            self.value **= num
            return self.value
        else:
            return 'please enter a integer or a float'
    def squroot(self):
            self.value **= 0.5
            return self.value
        
c = calc(5)
c.__add__(4)
print(c.value)
c.__sub__(3)
print(c.value)
c.squr(2)
print(c.value)
c.squroot()
print(c.value)