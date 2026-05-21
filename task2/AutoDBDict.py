class AutoDBDict:
    def __init__(self) -> None:
        self.stmts = {}

    def set_stmt(self, object_type, stmt):
        self.stmts[object_type] = stmt

    def add_to_db(self, obj, session):
        db_object = session.exec(self.stmts[type(obj)](obj)).first()

        if not db_object:
            db_object = obj
            session.add(db_object)
            session.flush()

        return db_object