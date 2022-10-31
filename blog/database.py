from sqlalchemy import create_engine, engine

engine = create_engine ('sqlite:///:memory:', echo=True)