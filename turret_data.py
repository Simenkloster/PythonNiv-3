
#I DENNE KAN DERE ENDRE PÅ HVOR STERKE TURRETSENE SKAL VÆRE I LEVEL 1 OG LEVEL 2

# Range = hvor langt de skyter
# Cooldown = Hvor lenge de må vente mellom hvert skudd
# Damage = Hvor mye damage den gjør med et skudd


#Liste over health på enemies: (Dere kan endre på dette i enemy_data.py, helt nederst i filen)
# Weak = 10 health
# Medium = 15 health
# Strong = 20 health
# Elite = 30 health


PANCAKE_TURRET_DATA = [
    
    #PANCAKE LEVEL 1
    {"range": 111, "cooldown": 1333, "damage": 3}, 
    
    #PANCAKE LEVEL 2
    {"range": 150, "cooldown": 800, "damage": 5}
]


SHOOTER_TURRET_DATA = [
    
    #SHOOTER LEVEL 1
    {"range": 234, "cooldown": 2000, "damage": 1},

    #SHOOTER LEVEL 2
    {"range": 350, "cooldown": 1500, "damage": 3}
    
]


STABBER_TURRET_DATA = [
    
    #STABBER LEVEL 1
    {"range": 60, "cooldown": 800, "damage": 2},

    #STABBER LEVEL 2
    {"range": 85, "cooldown": 550, "damage": 4}

]







#HER KAN DERE ENDRE PÅ HVA DET SKAL KOSTE Å KJØPE DE FORSKJELLIGE TURRETSENE

TURRETS_LIST = [
    {
        "name": "pancake",
        "cost": 100,
     },
     {
         "name": "stabber",
         "cost": 100
     },
     {
         "name": "shooter",
         "cost": 100
     }
]