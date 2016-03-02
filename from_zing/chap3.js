
load("/root/zing/Chapter_2/create_data.js");
db.people.drop();
db.people.insert(people);

/*
db.collection.update(query, update_document, is_upsert, for_all_matches)

$inc, $set, $unset, $addToSet, $push, $pull, $pop, $each, $slice, $sort
document.attribute, list.index
*/

function query_print(query, to_keep, num=1) {
  cursor = db.people.find(query, to_keep);
  for (i=0;i<num;i++) {
    printjson(cursor.next());
  }
}

/* Update 1 */
function Update1() {
  query = {"name" : {"first" : "amy", "last" : "mozart"}};
  query_print(query, {"age" : 1, "name.first" : 1, "_id" : 0});
  print(db.people.update(query, {"$inc" : {"age" : 1}}));
  query_print(query, {"age" : 1, "name.first" : 1, "_id" : 0});
}

function Update2() {
  query = {};
  query_print(query, {"age" : 1, "name.first" : 1, "_id" : 0}, 10);
  print(db.people.update(query, {"$inc" : {"age" : 1}}, false, true))
  query_print(query, {"age" : 1, "name.first" : 1, "_id" : 0}, 10);
}

function Update3() {
  query = {"name" : {"first" : "greg", "last" : "smith"}};
  query_print(query, {"hair" : 1, "name.first" : 1, "_id" : 0});
  print(db.people.update(query, {"$set" : {"hair" : "green"}}));
  query_print(query, {"hair" : 1, "name.first" : 1, "_id" : 0});
}

function Update4() {
  query = {"name" : {"first" : "greg", "last" : "smith"}};
  query_print(query, {});
  print(db.people.update(query, {"$unset" : {"hair" : 1}}));
  query_print(query, {});
}

function Update5() {
  query = {"name" : {"first" : "hellen", "last" : "kant"}};
  query_print(query, {"name.first" : 1, "_id" : 0, "fruit" : 1});
  /* slice must occur with each */
  print(db.people.update(query, {"$push" : {"fruit" : {"$each" : ["starfruit"], "$slice" : -3}}}));
  query_print(query, {"name.first" : 1, "_id" : 0, "fruit" : 1});
}

function Update6() {
  query = {"name" : {"first" : "sally", "last" : "kant"}};
  query_print(query, {"name.first" : 1, "_id" : 0, "fruit" : 1});
  print(db.people.update(query, {"$addToSet" : {"fruit" : {"$each" : ["dragon fruit", "grape", "pear"]}}}))
  query_print(query, {"name.first" : 1, "_id" : 0, "fruit" : 1});
}

function Update7() {
  query = {"name.last" : "kant"};
  query_print(query, {"name" : 1, "_id" : 0}, 10);
  print(db.people.update(query, {"$set" : {"name.last" : "hume"}}, false, true));
  query = {"name.last" : "hume"};
  query_print(query, {"name" : 1, "_id" : 0}, 10);
}

function Update8() {
  doc1 = {"rating" : 10, "quote" : "Don't take life to seriously, You'll never escape it alive anyway.", "author" : "unknown"};
  doc2 = {"rating" : 2, "quote" : "Never forget that only dead fish swim with the stream", "author" : "malcolm muggeridge"};
  query = {"name" : {"first" : "joe", "last" : "smith"}};
  query_print(query, {});
  print(db.people.update(query, {"$push" : {"comments" : {"$each" : [doc1, doc2]}}}));
  query_print(query, {});
}

function Update9() {
  doc = {"rating" : 8, "quote" : "Only the wisest and stupidest of men never change.", "author" : "Confucious"};
  query = {"name" : {"first" : "joe", "last" : "smith"}};
  query_print(query, {"_id" : 0, "name.first" : 1, "comments" : 1});
  print(db.people.update(query, {"$push" : {"comments" : {"$each" : [doc], "$sort" : {"rating" : -1}}}}));
  query_print(query, {"_id" : 0, "name.first" : 1, "comments" : 1});
}

function Update10() {
  query = {"name" : {"first" : "joe", "last" : "smith"}};
  query_print(query, {"_id" : 0, "name.first" : 1, "comments" : 1});
  print(db.people.update(query, {"$set" : {"comments.0.rating" : 100}}));
  query_print(query, {"_id" : 0, "name.first" : 1, "comments" : 1});
}
