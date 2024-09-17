from pdf_wrapper import PDFSearchAPIWrapper
from web_wrapper import WebSearchAPIWrapper
from langchain_community.utilities import GoogleSearchAPIWrapper
# from langchain_core.tools import Tool
from langchain.tools.base import StructuredTool
def google_tool():
    google_search = GoogleSearchAPIWrapper()
    google_tool = StructuredTool.from_function(
        name="google-search",
        description="Search Google for recent results.",
        func=google_search.run
    )
    return google_tool

def web_tool():
    web_search = WebSearchAPIWrapper()
    web_tool = StructuredTool.from_function(
        name="web-search",
        description="Search web data for information",
        func=web_search.run
    )
    return web_tool

def pdf_tool():
    pdf_search = PDFSearchAPIWrapper()
    pdf_tool = StructuredTool.from_function(
        name="pdf-search",
        description="Search PDF for relevant information",
        func=pdf_search.run
    )
    return pdf_tool

