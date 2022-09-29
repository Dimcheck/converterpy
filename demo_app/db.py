import aiopg.sa
from sqlalchemy import MetaData, create_engine

from models import choice, question
from settings import config


DSN = 'postgresql://{user}:{password}@{host}:{port}/{database}'


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[question, choice])


def demo_data(engine):
    conn = engine.connect()
    conn.execute(question.insert(), [
        {'question_text': 'What\'s up?',
         'pub_date': '2022-12-15 17:17:49.629+02'}
    ])
    conn.execute(choice.insert(), [
        {'choice_text': 'Not much', 'votes': 0, 'question_id': 1},
        {'choice_text': 'Slava Ukraini', 'votes': 1, 'question_id': 1},
        {'choice_text': 'Coding time', 'votes': 0, 'question_id': 1},
    ])
    conn.close()


async def pg_context(app):
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize']
    )
    app['db'] = engine

    yield

    app['db'].close()
    await app['db'].wait_closed()


if __name__ == '__main__':
    db_url = DSN.format(**config['postgres'])
    engine = create_engine(db_url)

    create_tables(engine)
    demo_data(engine)
