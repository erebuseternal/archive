load("/root/zing/Chapter_2/create_data.js");
db.people.drop();
db.people.insert(people);

/*
$match - query
$project - like selection i query
            new_name : $old_name
            name : {expression}
              $add, $subtract, $multiply, $divide, $mod, $month, $day,
              etc.
              $substr, $concat, $toLower, $toUpper,
              logical
$group
        _id : field you want to group on
        name : {aggregation}
          $sum, $avg, $max, $min, $first, $last
$unwind : $field you wanna unwind. Creates a separate document for each element
of the array unwinded and adds all additional attributes to each said document

$sort, $limit, $skip are like query versions
*/

/* Match just takes a query as its argument, so no biggy there */

function PRINT(cursor) {
  while (cursor.hasNext()) {
    object = cursor.next()
    printjson(object)
  }
}

// just select names
function Ag1() {
  project = {"$project" : {"name" : 1, "_id" : 0}};
  cursor = db.people.aggregate(project);
  PRINT(cursor);
}

// get first names as first_name not name.first
function Ag2() {
  project = {"$project" : {"first_name" : "$name.first", "_id" : 0}};
  cursor = db.people.aggregate(project);
  PRINT(cursor);
}

// get distinct first names
function Ag3() {
  project = {"$project" : {"first_name" : "$name.first", "_id" : 0}};
  group = {"$group" : {"_id" : "$first_name"}};
  cursor = db.people.aggregate(project, group);
  PRINT(cursor);
}

// expression :P
function Ag4() {
  project = {"$project" : {"first_name" : {"$toUpper" : "$name.first"}}};
  group = {"$group" : {"_id" : "$first_name"}};
  cursor = db.people.aggregate(project, group);
  PRINT(cursor);
}

// initials
function Ag5() {
  project = {"$project" :
    {"initials" :
        {"$concat" : [
          {"$toUpper" :
            {"$substr" : ["$name.first", 0, 1]}
          }, ".",
          {"$toUpper" :
            {"$substr" : ["$name.last", 0, 1]}
          },"."]
        }, "_id" : 0, "first" : "$name.first", "last" : "$name.last"
      }
    };
  cursor = db.people.aggregate(project);
  PRINT(cursor);
}

// avg age maximum age and minimum age
function Ag6() {
  project = {"$project" : {"first_name" : "$name.first", "age" : 1}};
  group = {"$group" : {
    "_id" : "$first_name",
    "age_avg" : {"$avg" : "$age"},
    "age_max" : {"$max" : "$age"},
    "age_min" : {"$min" : "$age"}
    }
  };
  cursor = db.people.aggregate(project, group);
  PRINT(cursor);
}

// note difference between this and the next
function Ag7() {
  match = {"$match" : {"name" : {"first" : "amy", "last" : "smith"}}};
  unwind = {"$unwind" : "$fruit"};
  cursor = db.people.aggregate(match, unwind);
  PRINT(cursor);
}

function Ag8() {
  match = {"$match" : {"name" : {"first" : "amy", "last" : "smith"}}};
  project = {"$project" : {"fruit" : 1, "_id" : 0}};
  unwind = {"$unwind" : "$fruit"};
  cursor = db.people.aggregate(match, project, unwind);
  PRINT(cursor);
}

// find all of the fruits
function Ag9() {
  project = {"$project" : {"fruit" : 1, "_id" : 0}};
  unwind = {"$unwind" : "$fruit"};
  group = {"$group" : {"_id" : "$fruit"}};
  cursor = db.people.aggregate(project, unwind, group);
  PRINT(cursor);
}

// sort the fruits
function Ag10() {
  project = {"$project" : {"fruit" : 1, "_id" : 0}};
  unwind = {"$unwind" : "$fruit"};
  group = {"$group" : {"_id" : "$fruit"}};
  sort = {"$sort" : {"_id" : 1}};
  cursor = db.people.aggregate(project, unwind, group, sort);
  PRINT(cursor);
}
