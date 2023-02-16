from mongoengine import *


class Ability(Document):
    name = StringField(required=True, unique=True)
    effect_stat = IntField()
    effect_status = StringField()

    description = StringField()

    meta = {'strict': False}


class Creature(Document):
    name = StringField(required=True, unique=True)
    image = StringField()

    hp = IntField(default=50, required=True)
    attack = IntField(required=True)
    defense = IntField(required=True)
    speed = IntField(required=True)
    ability = ReferenceField(Ability)
    description = StringField()
    lore = StringField()

    meta = {'strict': False}

    def __repr__(self):
        ability_name = self.ability.name if self.ability else "No Ability yet"
        return f"<Creature {self.name} - Atk {self.attack}: {ability_name}>"


connect("Creatures")

Creature.drop_collection()
Ability.drop_collection()

# Your code goes here
a = Ability(name="Test")
a.save()

c = Creature(name="jdfkasdjs;", hp=3920, image="11")

a.save()
c.ability = a
c.save()

a = Ability()
c = Creature(name="jdfkasdjs;", hp=3920, image="11", description="dfs")

a.save()
c.ability = a
c.save()

pass
