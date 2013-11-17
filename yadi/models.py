__author__ = 'nishara'


from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

engine = create_engine('postgresql://postgres:123456@localhost:5432/Cinema', echo=True)

class ReformatQuery():
    def reformat(self,sqlQuery):
        q = []
        word = sqlQuery.split()
        letters = set('._')
        for w in word:
                if letters & set(w):
                    subList = w.split('._')
                    b = inspect(movie)
                    attributes = b.attrs.keys()
                    i = int (subList[1])
                    s = subList[0] + '.' + attributes[i]
                    q.append(s)
                else:
                    q.append(w)
        q = " ".join(str(x) for x in q)
        print "Processed Query\n" + q+"\n"
        return q


class movie(Base):
    __tablename__ = 'movie'
    title = Column(String, primary_key=True)
    director = Column(String)
    length_mins = Column(Integer)
    release_date = Column(String)



class featuring(Base):
    __tablename__ = 'featuring'
    title = Column(String, primary_key=True)
    actor = Column(String)
    a_role = Column(String)


