from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DbBaseControl:
    """Базовый репозиторий"""
    def __init__(self, name, folder, base=None):
        """
        :param name: Имя базы данных :memory: - создаст базу в памяти
        :param dir: Директория
        :param base: базовый класс для создания моделей
        """
        self.name = name
        self.folder = folder
        # Создаем движок
        engine = create_engine('sqlite:///{}/{}'.format(self.folder, self.name), echo=False)
        # Создаем сессию
        Session = sessionmaker(bind=engine)
        session = Session()
        # Сохраняем текущую сессию
        self.session = session
        # Не забываем создать структуру базы данных
        base.metadata.create_all(engine)

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
