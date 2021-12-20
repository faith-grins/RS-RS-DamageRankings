from sqlalchemy import create_engine
from data.model import Ability


db_file = 'rsrs_damage_backend.db'


def create_db():
    engine = create_engine(f"sqlite+pysqlite:///{db_file}", echo=True)
    Ability.ORM_Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_db()
