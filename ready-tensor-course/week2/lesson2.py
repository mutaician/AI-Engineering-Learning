from typing import List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv


class Product(BaseModel):
    name: str = Field(description="The name of the product")
    price: float = Field(description="The product's price.")
    features: List[str] = Field(description="Product's features")
    category: str = Field(description="Product category. One of [Beverages, Dairy, Grocery]")
    
model = ChatOpenAI(model='gpt-5-nano', temperature=0)

prompt = ChatPromptTemplate.from_template(
    "Generate product information for: {description}"
)

chain = prompt | model.with_structured_output(Product)

result = chain.invoke({"description": "a new organic almond milk"})
print(result.model_dump())
    
    