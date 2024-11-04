from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Recipeクラスを定義
class Recipe(BaseModel):
    # 材料一覧: リスト型を指定
    ingredients: list[str] = Field(description="ingredients of the dish")
    # 手順: リスト型を指定
    steps: list[str] = Field(description="steps to make the dish")


output_parser = PydanticOutputParser(pydantic_object=Recipe)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "ユーザーが入力した料理のレシピを考えてください。\n\n{format_instructions}"),
        ("human", "{dish}"),
    ]
)

prompt_with_format_instructions = prompt.partial(
    format_instructions = output_parser.get_format_instructions() # Recipeのフォーマットを指定
)

model = ChatOpenAI(mkdel="gpt-4o-mini", temperature=0).bind(
    response_format={"type": "json_object"}
)

chain = prompt_with_format_instructions | model | output_parser

recipe = chain.invoke({"dish": "カレー"})
print(type(recipe))
print(recipe)
