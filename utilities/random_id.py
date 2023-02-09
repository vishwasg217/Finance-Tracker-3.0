import uuid
import random


for x in range(22):
    id = uuid.uuid4()
    with open('id.txt', 'a') as f:
        f.write(str(id)[9:18]+"\n")





