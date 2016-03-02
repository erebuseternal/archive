first_names = ['amy', 'joe', 'greg', 'sally', 'rose', 'nathan', 'joseph',
'georgia', 'john', 'carla', 'hellen', 'mike', 'tristan', 'peter']
last_names = ['smith', 'bach', 'mozart', 'einstein', 'kant', 'johnson',
'carlsen', 'dirac']
middle = 'abcdefghijklmnopqrstuvwxyz'
hair_colors = ['red', 'blonde', 'brunette', 'white']
eye_colors = ['blue', 'grey', 'green', 'brown', 'black']
fruits = ['apple', 'banana', 'pineapple', 'lemon', 'strawberry', 'blueberry', 'grape']

from random import randint

names = []
people = []
lines = []

while len(names) < len(first_names) * len(last_names) * 26:
    i = randint(0, len(first_names) - 1)
    h = randint(0, 25)
    j = randint(0, len(last_names) - 1)
    name = (first_names[i], middle[h], last_names[j])
    if name not in names:
        names.append(name)
        age = randint(0, 100)
        hair_color = hair_colors[randint(0, len(hair_colors) - 1)]
        eye_color = eye_colors[randint(0, len(eye_colors) - 1)]
        favorite_fruits = []
        while len(favorite_fruits) < 3:
            k = randint(0, len(fruits) - 1)
            fruit = fruits[k]
            if fruit not in favorite_fruits:
                favorite_fruits.append(fruit)
        person = [first_names[i], middle[h], last_names[j], age, hair_color, eye_color]
        person.extend(favorite_fruits)
        line = ''
        for element in person:
            line = '%s,%s' % (line, element)
        line = line[1:] + '\n'
        lines.append(line)
file = open('people.csv', 'w')
file.writelines(lines)
