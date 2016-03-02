
load("/root/zing/Chapter_2/create_data.js");
db.people.drop();
db.people.insert(people);

/*
$gt, $gte, $lt, $lte, $ne, $in, $nin, $or, $and, $not,
$all, $size, $slice, $elemMatch, $where

.limit
.sort
.skip
.snapshot (this means we do not iterate through the files
holding our records, but rather through id's, takes longer though)

lazy so order of the first three above doesn't matter
*/

function writeResults(cursor,number=10) {
  for (i=0;i<number;i++) {
    person = cursor.next();
    printjson(person);
  }
}

/* working people */
function Query1() {
  query = {"age" : {"$gte" : 16, "$lte" : 65}};
  cursor = db.people.find(query, {"age" : 1, "name": 1, "_id" : 0}).sort({"age" : 1});
  print("youngest");
  writeResults(cursor);
  cursor = db.people.find(query, {"age" : 1, "name": 1, "_id" : 0}).sort({"age" : -1});
  print("oldest");
  writeResults(cursor);
}

/* not a kant */
function Query2() {
  query = {"name.last" : {"$ne" : "kant"}};
  cursor = db.people.find(query, {"name" : 1, "_id" : 0});
  writeResults(cursor);
}

/* someone with a girls name */
function Query3() {
  query = {"name.first" : {"$in" : ['amy', 'sally', 'rose',
  'georgia', 'carla', 'hellen',]}};
  cursor =db.people.find(query, {"name.first" : 1, "_id" : 0}).sort({"age" : 1});
  writeResults(cursor);
}

/* anyone who DOESN'T have a pretensious name */
function Query4() {
  query = {"name.last" : {"$nin" : ['bach', 'mozart', 'einstein', 'kant',
  'dirac']}};
  cursor = db.people.find(query, {"name.last" : 1, "_id" : 0})
  writeResults(cursor);
}

/* banana xor apple */
function Query5() {
  query = {"$or" : [{"$and" : [{"fruit" : "banana"}, {"fruit" : {"$not" : {"$in": ["apple"]}}}]}, {"$and" : [{"fruit" : "apple"}, {"fruit" : {"$not" : {"$in": ["apple"]}}}]}]};
  cursor = db.people.find(query, {"fruit" : 1,  "_id" : 0});
  writeResults(cursor, 10);
}

/* both apple and banana */
function Query6() {
  query = {"fruit" : {"$all" : ["apple", "banana"]}};
  cursor = db.people.find(query, {"fruit" : 1,  "_id" : 0});
  writeResults(cursor, 5);
}

/* I just want the first fruit from everyone */
function Query7() {
  query = {};
  cursor = db.people.find(query, {"fruit" : {"$slice" : 1}});
  writeResults(cursor, 10);
}

/* elemMatch looks at each element and applies all logic. Then if one
element passes, the whole thing passes */

/* names of four letters */
function my_where() {
  if (this.name.first.length == 4) {
    return true;
  }
  else {
    return false;
  }
}
function Query8() {
  query = {"$where" : my_where};
  cursor = db.people.find(query, {"name.first" : 1, "_id" : 0});
  writeResults(cursor, 30);
}

/* remove fruit on amy mozart to demonstrate $exists */
function Query9() {
  print("removing amy mozart's fruit list")
  db.people.update({"name" : {"first" : "amy", "last" : "mozart"}}, {"$unset" : {"fruit" : 1}});
  print("now querying for anyone who doesn't have fruit")
  query = {"fruit" : {"$exists" : false}};
  cursor = db.people.find(query, {"name" : 1, "_id" : 0});
  writeResults(cursor, 1)
}

/* first fruit is lemon */
function Query10() {
  query = {"fruit.0" : "lemon"};
  cursor = db.people.find(query, {"fruit" : 1, "_id" : 0});
  while (cursor.hasNext()) {
    printjson(cursor.next());
  }
}
