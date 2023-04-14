class MyClass:
    a = 1

    def __init__(self, b):
        self.b = b


class_1 = MyClass(2)
class_2 = MyClass(3)
MyClass.a = 2
print(class_1.a, class_1.b)
print(class_2.a, class_2.b)
