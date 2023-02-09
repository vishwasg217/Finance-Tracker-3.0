import uuid
import random


for x in range(8):
    id = random.randrange(1200, 1800, random.randint(5, 100))
    with open('num.txt', 'a') as f:
        f.write(str(id)+"\n")