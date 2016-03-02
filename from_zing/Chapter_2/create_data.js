var first_names = ['amy', 'joe', 'greg', 'sally', 'rose', 'nathan', 'joseph',
'georgia', 'john', 'carla', 'hellen', 'mike', 'tristan', 'peter'];
var last_names = ['smith', 'bach', 'mozart', 'einstein', 'kant', 'johnson',
'carlsen', 'dirac'];
var hair_colors = ['red', 'blonde', 'brunette', 'white'];
var eye_colors = ['blue', 'grey', 'green', 'brown', 'black'];
var fruit_options = ['apple', 'banana', 'pineapple', 'lemon', 'strawberry', 'blueberry', 'grape'];

function random(number) {
  return Math.floor(number*Math.random() + 1);
}

var count = 0;
var people = []

for (x in first_names) {
  for (y in last_names) {
    var name = {'first' : first_names[x], 'last' : last_names[y]};
    var age = random(100);
    var hair = hair_colors[random(hair_colors.length) - 1];
    var eye = eye_colors[random(eye_colors.length) - 1];
    var fruits = [];
    while (fruits.length < 3) {
      var fruit = fruit_options[random(fruit_options.length) - 1];
      if (fruits.indexOf(fruit) == -1) {
        fruits.push(fruit);
      }
    }
    var document = {'name' : name, 'age' : age, 'hair' : hair, 'eye' : eye, 'fruit' : fruits};
    people.push(document);
    count += 1;
  }
}

print('' + count + ' records created and place in variable people');
