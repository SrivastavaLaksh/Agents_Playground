#specify the model name
model_name="ollama_chat/llama3.2"


from sqlalchemy import (
    Column,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    insert,
    inspect,
    text,
)

#create an in-memory SQLite database
engine = create_engine("sqlite:///:memory:")
metadata_obj = MetaData()

# create city SQL table
table_name = "receipts"
receipts = Table(
    table_name,
    metadata_obj,
    Column("receipt_id", Integer, primary_key=True),
    Column("customer_name", String(16), primary_key=True),
    Column("price", Float),
    Column("tip", Float),
)
metadata_obj.create_all(engine)

rows = [
    {"receipt_id": 1, "customer_name": "Alan Payne", "price": 12.06, "tip": 1.20},
    {"receipt_id": 2, "customer_name": "Alex Mason", "price": 23.86, "tip": 0.24},
    {"receipt_id": 3, "customer_name": "Woodrow Wilson", "price": 53.43, "tip": 5.43},
    {"receipt_id": 4, "customer_name": "Margaret James", "price": 21.11, "tip": 1.00},
]
for row in rows:
    stmt = insert(receipts).values(**row)
    with engine.begin() as connection:
        cursor = connection.execute(stmt)

inspector = inspect(engine)
columns_info = [(col["name"], col["type"]) for col in inspector.get_columns("receipts")]

table_description = "Columns:\n" + "\n".join([f"  - {name}: {col_type}" for name, col_type in columns_info])
print(table_description)

from smolagents import tool


#specify the tool 
@tool
def sql_engine(query: str) -> str:
    """
    Allows you to perform SQL queries on the table. Returns a string representation of the result.
    The table is named 'receipts'. Its description is as follows:
        Columns:
        - receipt_id: INTEGER
        - customer_name: VARCHAR(16)
        - price: FLOAT
        - tip: FLOAT

    Args:
        query: The query to perform. This should be correct SQL.
    """

    output = "" # Initialize an empty string to store the output
    with engine.connect() as con: # Connect to the database
        rows = con.execute(text(query)) # Execute the query and store the result in rows
        for row in rows:
            output += "\n" + str(row)
    return output


#Import the agent library
from smolagents import CodeAgent,LiteLLMModel

#Use LiteLLMModel to load ollama api
model =LiteLLMModel(
    model_id=model_name,
    api_base="http://localhost:11434",
    #api_key="your-api-key",
    num_ctx=8192,
)


#create the agent
agent = CodeAgent(
    tools=[sql_engine],
    model=model
)

query=input("Enter your query: ")

agent.run(query)
#agent.run("Can you give me the name of the client who got the most expensive receipt?")
