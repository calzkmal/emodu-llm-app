from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llm_app import handle_conversation

app = FastAPI()

# API Body
class LLMRequest(BaseModel):
    emosi: str
    penguatan: str
    pendekatan: str

# List of supported emotions
list_emosi = {'sad', 'angry', 'disgust', 'fear'}

# List of supported reinforcements
list_penguatan = {'attention', 'relevance', 'confidence', 'satisfaction'}

# List of supported arcs_model
list_pendekatan = {'positive', 'negative'}

@app.post("/emodu-llm")
async def llm_response(request: LLMRequest):
    """
    Handles requests to generate reinforcement text based on emotion, reinforcement type, and approach.
    """
    try:
        # Validate inputs using sets for faster lookup
        if request.emosi.lower() not in list_emosi:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid emotion '{request.emosi}'. Supported emotions are: {', '.join(list_emosi)}"
            )

        if request.penguatan.lower() not in list_penguatan:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid reinforcement '{request.penguatan}'. Supported reinforcements are: {', '.join(list_penguatan)}"
            )

        if request.pendekatan.lower() not in list_pendekatan:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid approach '{request.pendekatan}'. Supported approaches are: {', '.join(list_pendekatan)}"
            )

        # Call the handler function
        result = await handle_conversation(
            emosi=request.emosi.lower(),
            pendekatan=request.pendekatan.lower(),
            penguatan=request.penguatan.lower()
        )

        # Return a structured response
        return {
            "status": "success",
            "result": result
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        # Log the error for better debugging
        print(f"Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again later."
        )