from sqlalchemy import Column, Integer, String, LargeBinary, Date
from db.session import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32), nullable=False, unique=True, index=True)
    password_hash = Column(LargeBinary(32), nullable=False)

    first_name = Column(String(64), nullable=True)
    second_name = Column(String(64), nullable=True)
    birth_date = Column(Date, nullable=True)
    email = Column(String(256), nullable=True)
    phone = Column(String(16), nullable=True)

    def update(self, **kwargs):
        """
        Обновление данных пользователя. Мы не можем обновить ни ID, ни логин, ни пароль через этот метод.
        Если передаются аргументы, не соответствующие разрешенным к изменению полям, они просто пропускаются.
        """

        for key, value in kwargs.items():
            if hasattr(self, key) and key not in ('id', 'username', 'password'):
                setattr(self, key, value)
