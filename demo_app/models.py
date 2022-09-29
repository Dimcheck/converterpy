from sqlalchemy import (Column, Date, ForeignKey,
                        Integer, MetaData, String, Table)


"""
It is possible to configure tables in a declarative style like so:

class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True)
    question_text = Column(String(200), nullable=False)
    pub_date = Column(Date, nullable=False)

But it doesn't give much benefits later on. SQLAlchemy ORM doesn't work in asynchronous style
and as a result aiopg.sa doesn't support related ORM expressions such as
Question.query.filter_by(question_text='Why').first() or session.query(TableName).all().
"""

meta = MetaData()

question = Table(
    'question', meta,

    Column('id', Integer, primary_key=True),
    Column('question_text', String(200), nullable=False),
    Column('pub_date', Date, nullable=False)
)

choice = Table(
    'choice', meta,

    Column('id', Integer, primary_key=True),
    Column('choice_text', String(200), nullable=False),
    Column('votes', Integer, server_default='0', nullable=False),
    Column('question_id', Integer, ForeignKey('question.id', ondelete='CASCADE'))
)
