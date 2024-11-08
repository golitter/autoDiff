import random
class A:
    def __init__(self):
        self.a = random.randint(0, 100)
    def __call__(self):
        print(f'random value of {random.randint(0, 100)}')
a = A()
a()