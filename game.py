from character import Character

class Game():
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def welcome(self):
        print(f"Welcome to {self.title}")
        print(f"There are {Room.num_rooms} rooms to explore")
        print(f"There are {Room.num_enemies} enemies to defeat")
        print(f"There are {Room.num_items} items to find")

    #cls refers to the class that this method belongs to
    def credits(self):
        print(f"This game was created by {self.author}")


#puting Character in the brackets makes Enemy a child class of Character
class Enemy(Character):
    #if a method with the same name as an inherited method is created
    #the new method overwrites the inherited one
    def __init__(self, enemy_name, enemy_description, weakness):
        #super refers to the parent class
        super().__init__(enemy_name, enemy_description)
        self.weakness = weakness.lower()
    
    def fight(self, weapon):
        if weapon.lower() == self.weakness:
            print(f"You succeed in killing off {self.name} with the {weapon}")
            Room.num_enemies -= 1
            return True
        else:
            print(f"The {weapon} is of no use against {self.name}, you are mortaly wounded by {self.name}")
            return False


class Room():
    #class variable
    #no self. means it is not an instance variable
    #not being inside any methods means it is local to the class
    #instead of being local to a specific method
    num_rooms = 0
    num_items = 0
    num_enemies = 0

    #constructor for the class
    #is called whenever a new Room object needs to be created
    #self contains all the attributes assoicated with the object
    def __init__(self, room_name, room_description):
        #Room. refers to a class variable
        Room.num_rooms += 1
        #self. means it is an attribute of the object
        #if it was just name is would be a local variable, local to the __init__ function
        #instead it is local to the object and can be different for each instance of the object
        self.name = room_name
        self.description = room_description
        self.adjacent_rooms = {}
        #private attirubte
        #is exposed through the character getter
        self._character = None
        self._item = None

    #create a getter else we can't create a setter
    @property
    def character(self):
        return self._character
    #creates a setter
    #when someroom.character = somecharacterobject is ran
    #this function will take the character object and set self._character 
    @character.setter
    def character(self, char):
        self._character = char
        #only increases the enemy count if it is an instance of the Enemy class
        if isinstance(char, Enemy):
            Room.num_enemies += 1

    @property
    def item(self):
        return self._item
    @item.setter
    def item(self, name):
        self._item = name.lower()
        Room.num_items += 1

    def get_adjacent_rooms(self):
        for direction, room in self.adjacent_rooms.items():
            print(f"The {room.name} is to the {direction}")

    def show_description(self):
        print(f"It is {self.description}")

    def describe(self):
        print(f"You are in the {self.name}")
        self.show_description()
        if self.inhabited():
            print(f"{self.character.name} is here")
            print(f"{self.character.name} is {self.character.description}")
        self.get_adjacent_rooms()

    def inhabited(self):
        return bool(self.character is not None)
    def link_to(self, adjacent_room, direction):
        self.adjacent_rooms[direction] = adjacent_room

    def move_to(self, direction):
        try:
            return self.adjacent_rooms[direction]
        except KeyError:
            print(f"There is nothing to the {direction}")
            return self

    def take_item(self):
        self._item = None


opposite_direction = {"north": "south", "south":"north", "east":"west", "west":"east"}
def link(room_1, room_2, direction):
    direction = direction.lower()
    room_1.link_to(room_2, direction)
    room_2.link_to(room_1, opposite_direction[direction])

dave = Enemy("Dave", "a smelly zombie", "herrings")
dave.set_conversation("Something smells odd round here")

emily = Enemy("Emily", "a ghost of a young girl who lived here many moons ago", "mobile phone")
emily.set_conversation("When I was a little victorian girl I died of shock")

steve = Enemy("Steve", "a scout leader from the 1970s who accidently wondered into here and was never seen again", "sat nav")
steve.set_conversation("Does anyone know where Mount Snowdon is? It feels like I've been looking for it for decades")

enterance = Room("Servants Enterance", "an extremely narrow hallway with dirty white walls and benches coated with a thick layer of dust and grime")
enterance.item = "mobile phone"
kitchen = Room("Kitchen", "a damp, dim, and dirty room buzzing with flies")
kitchen.item = "sat nav"
#this is aggrgeation
kitchen.character = dave
ballroom = Room("Ballroom", "a vast room with a shiny white walls and a shiny wooden floor")
ballroom.item = "herrings"
ballroom.character = emily
dining_hall = Room("Dining hall", "a long room with a dark wooden table overflowing with golden trinkets")
dining_hall.character = steve

link(enterance, kitchen, "north")
link(kitchen, dining_hall, "west")
link(dining_hall, ballroom, "south")
link(ballroom, enterance, "east")

current_room = enterance
backpack = []

haunted_mansion = Game("The Haunted Mansion", "Rory Sharp")
haunted_mansion.welcome()
try:
    while True:
        print("")
        current_room.describe()

        item = current_room.item
        if item is not None:
            current_room.take_item()
            print(f"You managed to find a {item} on the floor, we'll keep hold of it in case it comes in usefull later")
            backpack.append(item)

        print("")
        if current_room.inhabited():
            want_to_talk = bool(input(f"Would you like to talk to {current_room.character.name}?  ")[0].lower() == "y")
            if want_to_talk:
                current_room.character.talk()

            want_to_fight = bool(input(f"Would you like to fight against {current_room.character.name}?  ")[0].lower() == "y")
            if want_to_fight:
                print("You currently have: ", end="", flush=True)
                for item in backpack:
                    print(item, end=" ", flush=True)
                print("")

                weapon = input("What weapon would you like to use?  ").lower()
                if weapon in backpack:
                    backpack.remove(item)
                    if current_room.character.fight(weapon):
                        #if a Character of class Character and not of class Enemy
                        #has its .fight() method called the .fight() will return true but hasn't been killed
                        if isinstance(current_room.character, Enemy):
                            current_room.character = None
                    else:
                        #ends the game
                        raise KeyboardInterrupt
                else:
                    print(f"Nice try but you don't have a {weapon}")

        if Room.num_enemies == 0:
            print("You killed all the enemies! You won!")
            raise KeyboardInterrupt

        current_room = current_room.move_to(input("In which direction would you like to move?  ").lower())
except KeyboardInterrupt:
    print("")
    print("Bye!")
    haunted_mansion.credits()