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
a = Ability(name="Best Ability")
c = Creature(name="Pepe", hp=50, image="11", description="A thing.",
             attack=10, defense=10, speed=1)

a.save()
c.ability = a
c.save()

a = Ability(name="Second Best Ability, but still good")
c = Creature(name="Bill", hp=50, image="35", description="Another thing.",
             attack=10, defense=10, speed=1)

a.save()
c.ability = a
c.save()

pass
