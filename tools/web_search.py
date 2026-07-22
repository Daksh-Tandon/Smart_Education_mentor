from langchain_community.tools.tavily_search import TavilySearchResults
import os

from dotenv import load_dotenv
load_dotenv()
search_tool = TavilySearchResults(
    max_results=3,
    tavily_api_key=os.getenv("TAVILY_API_KEY")
)

def search_web(query: str):
    return search_tool.invoke(query)