from pydantic import BaseModel
import requests
from pydantic_models import QueryRequest

class PDFQuestionAnswering(BaseModel):
    name: str = "Pdf Question Answering"
    description: str = "Useful for getting relavent information from pdf"

    def run(self, query: str) -> str:
        try:
            print(query)
            request_data=QueryRequest(input=query)
            response = requests.post(f"http://127.0.0.1:8000/search_query_in_pdf", json=request_data.dict())
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            # Handle request errors
            return {"error": f"Request failed: {str(e)}"}
        except Exception as e:
            # Handle other exceptions
            return {"error": str(e)}
