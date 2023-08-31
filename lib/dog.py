import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    all = []


    def __init__(self , name , breed):
       self.id = None
       self.name = name 
       self.breed = breed
           

     #create a mapper method to create the table columns      
    @classmethod
    def create_table(self):
       dogs = """
            CREATE TABLE IF NOT EXISTS dogs(
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
       CURSOR.execute(dogs)

    @classmethod
    def drop_table(cls):
       query = 'DROP TABLE IF EXISTS dogs'
       CURSOR.execute(query)


    def save(self):
       if self.id is None: 
        dogs = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        """

        CURSOR.execute(dogs, (self.name, self.breed))
        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]
       else:
           query = '''
                UPDATE dogs
                SET name = ?, breed = ?
                WHERE id = ?
            '''
           
           values = (self.name, self.breed, self.id)
           CURSOR.execute(query, values)

       return self

    def create (cls , name , breed):
       dog = cls (name , breed)
       dog.save()
       return  dog
    
    @classmethod
    def new_from_db (cls , row):
       dog = cls(row[1] ,row[2])
       dog.id = row[0]
    
   
    def get_all(cls):
        sql = """
            SELECT *
            FROM dogs
        """

        all = CURSOR.execute(sql).fetchall()

        cls.all = [cls.new_from_db(row) for row in all]
    def find_by_name(cls , name) :
        sql = """
            SELECT *
            FROM dogs
            WHERE name = ?
            LIMIT 1
        """
        dog = CURSOR.execute(sql, (name,)).fetchone()
        if dog:
          return cls.new_from_db(dog)
        else:
           return None
    def find_or_create_by(cls ,name , breed):
       existing_dog = cls.find_by_name(name)
       if existing_dog:
          return existing_dog
       else:
          new_dog = cls.create(name , breed)
          return new_dog

dog =Dog('joy' , 'cocker spaniel')
Dog.create_table()
Dog.drop_table()