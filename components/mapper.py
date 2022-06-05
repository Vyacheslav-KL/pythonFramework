from abc import ABCMeta, abstractmethod

from components.exceptions import DbCommitException, DbDeleteException, \
    DbUpdateException, RecordNotFoundException


class BaseMapper(metaclass=ABCMeta):

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    @property
    @abstractmethod
    def table_name(self):
        pass

    @property
    @abstractmethod
    def model(self):
        pass

    def all(self):
        statement = f'SELECT * from {self.table_name}'
        self.cursor.execute(statement)
        columns = [i[0] for i in self.cursor.description]
        result = []

        for val in self.cursor.fetchall():
            obj = self.model(**{columns[i]: val[i] for i, _ in enumerate(val)})
            result.append(obj)
        return result

    def insert(self, **schema):
        statement = f"INSERT INTO {self.table_name} " \
                    f"({','.join(schema.keys())}) VALUES (?)"
        self.cursor.execute(statement, (','.join(schema.values()),))

        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj, **schema):
        schema = {str(key) + '=?': val for key, val in schema.items()}
        statement = f"UPDATE {self.table_name} SET {','.join(schema.keys())}" \
                    f"WHERE id=?"
        self.cursor.execute(statement, (','.join(schema.values()), obj.id))

        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.table_name} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))

        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)

    def get_by_id(self, id):
        statement = f"SELECT * FROM {self.table_name} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()

        try:
            id, name = result
            return self.model(id=id, name=name)
        except Exception:
            raise RecordNotFoundException(f"Record with id={id} not found")
        