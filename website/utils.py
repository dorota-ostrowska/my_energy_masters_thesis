def get_next_id(db, column_of_table):
    highest_existing_id = db.session.query(db.func.max(column_of_table)).scalar()
    if highest_existing_id is None:
        new_id = 1
    else:
        new_id = highest_existing_id + 1
    return new_id