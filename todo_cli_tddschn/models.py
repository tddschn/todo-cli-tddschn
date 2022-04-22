from sqlmodel import Field, Relationship, SQLModel

class TodoBase(SQLModel):
	description: str
	priority: str = Field(default='medium')
	status: str = Field(default='todo')
	project = Column(String)
	tags = Column(String)
	due_date = Column('Due Date', DateTime, nullable=True)

class Todo(SQLModel, table=True):
