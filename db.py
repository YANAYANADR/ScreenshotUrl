from sqlalchemy import (create_engine, String,
                        text, select,update, func)
from sqlalchemy.orm import (DeclarativeBase, Mapped,
                            mapped_column, Session)
import logging
import psycopg2

# logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

#code to only be used in test!!!! vvv
#
# eng = create_engine("postgresql://postgres:1234@localhost:5432/postgres",
#                     isolation_level="AUTOCOMMIT")
#
# with Session(eng) as sess:
#     try:
#         sess.execute(text('CREATE DATABASE links'))
#         log.info('База создана')
#     except Exception as e:
#         log.info(f'База уже существует')
# ^^^^ end of test code pls remove later

eng = create_engine("postgresql://postgres:1234@db:5432/links")

# Db classes
class Base(DeclarativeBase):
    pass


class LinkTable(Base):
    __tablename__ = 'link_table'
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String())
    path: Mapped[str] = mapped_column(String())


Base.metadata.create_all(eng)


def insert_link(url, path):
    with Session(eng) as s:
        li = LinkTable(url=url, path=path)
        s.add(li)
        s.flush()
        s.commit()


def link_exists(url):
    with Session(eng) as s:
        out = s.execute(select(func.count(1))
                        .where(LinkTable.url == url)).first()[0]
        return out>0


def return_path(url):
    with Session(eng) as s:
        out = s.execute(select(LinkTable.path)
                        .where(LinkTable.url == url)).first()[0]
        return out

def change_path(url,path):
    with Session(eng) as s:
        s.execute(update(LinkTable).where(LinkTable.url==url).values(path=path))
        s.commit()


# if __name__ == '__main__':
#     # insert_link('testurl','testpath')
#     print(change_path('testurl','bebe'))
#     pass
