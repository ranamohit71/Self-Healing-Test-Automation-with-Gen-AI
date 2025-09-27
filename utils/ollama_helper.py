from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, model_validator
import json

class LocatorSuggestion(BaseModel):
    by: str = Field(description="Selenium By type (ID, NAME, XPATH, CSS_SELECTOR)")
    value: str = Field(description="The best locator value string")

def get_best_locator_from_llm(html: str, element_name: str):

    """
    Use LangChain with Ollama to get best locator for a given element.
    Returns tuple: (by_type, value)
    """

    parser = PydanticOutputParser(pydantic_object=LocatorSuggestion)

    template_text = """
    You are an expert Selenium test automation engineer.

    Analyze the given HTML and find the BEST unique locator for the element named: {element_name}.
    
    HTML: {html}
    
    Rules:
    - Priority of locators is: ID > NAME > XPATH > CSS_SELECTOR.
    - Use only locators explicitly present in the HTML provided.
    - If the locator type or value cannot be found, set it to null.
    - Never guess, infer, or create locators not present in the HTML.
    - Output must strictly follow the JSON schema below.
    - When an element is found with ID, it does not have #

    Return only the JSON and don't provide any other explanation or text.

    Schema:
    {format_instructions} """

    template = PromptTemplate(
        template=template_text,
        input_variables=["element_name", "html"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    #Initialize the LLM model - used Ollama model
    llm = ChatOllama(model="llama3.1:8b", temperature=0)
    
    #create the prompt and pass the input variables at run time.
    prompt = template.format(element_name=element_name, html=html)   

    #invoke the llm
    response = llm.invoke(prompt)
    #print(response.content)
    
    #parse the json output and convert that to tuple
    data = json.loads(response.content)

    print(data)
    
    my_tuple = (data["by"], data["value"])

    #print(my_tuple)
    #print(type(my_tuple))
    #return tuple to calling function for further action
    return my_tuple
