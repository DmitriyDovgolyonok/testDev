db = db.getSiblingDB("animal_db");
db.animal_tb.drop();

db.animal_tb.insertMany([
    {
        "key": "Dima",
        "value": "Kozlov",
    },
    {
        "key": "Vadim",
        "value": "Lol"
    },
    {
        "key": "Tiger",
        "value": "Lion"
    },
]);