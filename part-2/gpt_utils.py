from pdf_wrapper import PDFQuestionAnswering
from web_wrapper import WebQuestionAnswering
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_core.tools import Tool
def google_tool():
    google_search = GoogleSearchAPIWrapper()
    google_tool = Tool(
        name="google-search",
        description="Search Google for recent results.",
        func=google_search.run
    )
    return google_tool

def web_tool():
    web_search = WebQuestionAnswering()
    web_tool = Tool(
        name="web-search",
        description="Search web data for information",
        func=web_search.run
    )
    return web_tool

def pdf_tool():
    pdf_search = PDFQuestionAnswering()
    pdf_tool = Tool(
        name="pdf-search",
        description="Search PDF for relevant information",
        func=pdf_search.run
    )
    return pdf_tool

