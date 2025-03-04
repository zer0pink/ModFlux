from peewee import *
from modflux.config import DATABASE_FILE

from modflux import migrate

# Initialize database
db = SqliteDatabase(DATABASE_FILE, pragmas={"foreign_keys": 1})


class BaseModel(Model):
    class Meta:
        database = db
        legacy_table_names = False


class Game(BaseModel):
    id = AutoField()

    name = CharField()

    # TODO: Enum
    game_id = CharField(null=True)

    game_path = CharField()
    mod_path = CharField()
    download_path = CharField()
    overwrite_path = CharField()
    work_path = CharField()


class ModVersion(BaseModel):
    id = AutoField()

    nexus_mod_id = IntegerField()
    nexus_file_id = IntegerField(null=True)
    version = CharField(null=True)

    path = CharField()
    game = ForeignKeyField(Game, backref="game_id")


class Mod(BaseModel):
    id = AutoField()

    name = CharField()
    load_order = IntegerField(null=True)
    active = BooleanField(null=True)

    nexus_mod_id = IntegerField(null=True)
    version = ForeignKeyField(ModVersion, backref="version_id")

    latest_version = CharField(null=True)

    tags = CharField(null=True)

    game = ForeignKeyField(Game, backref="game_id")


migrate.run()

db.connect()
