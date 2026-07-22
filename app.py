from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import util
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from db.history import history_py,history_get
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from ragcode.ragvec import set_vector_store,get_vector_store
import time
from graph.roadmap_graph import roadmap_graph
from graph.graphstruct import graph_app
from graph.quizgraph import quiz_graph
from graph.quizstate import QuizState
start = time.time()
from db.logincheck import login_check
from db.registercheck import reg_check



from dotenv import load_dotenv

import shutil
import os

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()
# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI()

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# -----------------------------
# Create Upload Folder
# -----------------------------
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -----------------------------
# Embedding Model
# -----------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -----------------------------
# Gemini LLM
# -----------------------------
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     temperature=0.3,
    
#  google_api_key=os.getenv("GOOGLE_API_KEY")
# )
llm = ChatOpenAI(
    model="google/gemma-3-12b-it",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPEN_ROUTER_KEY"),
)


# -----------------------------
# Home API
# -----------------------------
@app.get("/")
def home():
    return {"message": "Smart Education Mentor API Running"}



#login api
class Loginreq(BaseModel):
    email:str
    password:str

@app.post('/login')
def login(req:Loginreq):
    details=login_check(req.email,req.password)

    return details
      
# Register api
class Regreq(BaseModel):
   fullname: str
   email: str
   password: str
   Class: int
   board: str
   school: str

@app.post("/register")
def register(req:Regreq):
    dict1={"name":req.fullname,"email":req.email,"password":req.password,"class":req.Class,"School":req.school,"board":req.board}
    return reg_check(dict1)
    



# -----------------------------
# Upload PDF
# -----------------------------
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Load PDF
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    # Split PDF
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)
    if len(chunks) == 0:
        return {
        "error": "PDF text extraction failed. Chunks are empty."
       }

    # Create Vector Store
    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )
    vector_store.save_local("faiss_indexes/current")
    set_vector_store(vector_store)
    print("After set:", get_vector_store())

    return {
        "message": "PDF Uploaded Successfully",
        "pages": len(documents),
        "chunks": len(chunks)
    }

# -----------------------------
# Request Model
# -----------------------------
class ChatRequest(BaseModel):
    question: str

# -----------------------------
# Chat API
# -----------------------------
@app.post("/chat")
async def chat(request: ChatRequest):
    vector_store = FAISS.load_local(
    "faiss_indexes/current",
    embeddings,
    allow_dangerous_deserialization=True
)

    if vector_store is None:
        return {
            "error": "Please upload a PDF first."
        }

    # Retrieve relevant chunks
    results = vector_store.similarity_search(
        request.question,
        k=4
    )
    retrieval_time = time.time() - start

    # Create context
    context = "\n\n".join(
        doc.page_content for doc in results
    )

    prompt = f"""
You are an PDF Explainer.

Answer ONLY from the provided context.
give the summarization of the entire pdf in simple words
If the answer is not present in the context,
reply exactly:

"The answer is not available in the uploaded PDF."

Context:
{context}

Question:
{request.question}
"""

    response = llm.invoke(prompt)
    response_time = time.time() - start
   
    query_embedding = embeddings.embed_query(request.question)
    context_embedding = embeddings.embed_query(context)
    similarity = util.cos_sim(query_embedding,context_embedding).item()



    return {
        "question": request.question,
        "answer": response.content,
            "metrics":{

        "retrieval_time": retrieval_time,

        "response_time": response_time,

        "context_similarity": similarity,

        "chunks_retrieved": len(results)

    }
       
    }
class ExplainRequest(BaseModel):
    question: str
    student_class:int
    user_id:str

@app.post("/explain")
async def explain(req: ExplainRequest):

#     vector_store = FAISS.load_local(
#     "faiss_indexes/current",
#     embeddings,
#     allow_dangerous_deserialization=True

# )
    config = {
    "configurable": {
        "thread_id": req.user_id
    }
}
    result = graph_app.invoke({

        "question": req.question,

        "student_class": req.student_class,
        

    },config=config)

    return result

class QuizRequest(BaseModel):
    topic: str
    student_class: int

@app.post("/generate_quiz")
async def generate_quiz(request: QuizRequest):
    vector_store = FAISS.load_local(
    "faiss_indexes/current",
    embeddings,
    allow_dangerous_deserialization=True
)
    result = quiz_graph.invoke({

        "question": request.topic,

        "student_class": request.student_class

    })
    #result.pop("vector_store", None)

    return result
class RoadmapRequest(BaseModel):

    goal: str
    level: str
    duration: str
    student_class:int

@app.post("/roadmap")
async def generate_roadmap(request: RoadmapRequest):

    result = roadmap_graph.invoke({

        "goal": request.goal,

        "level": request.level,

        "duration": request.duration,
        "student_class":request.student_class

    })

    return result

class HistoryRequest(BaseModel):
    userid:str
    topic:str
    core:str
@app.post("/historyquestions")
async def generate_history(req:HistoryRequest):
    return history_py(req.userid,req.topic,req.core)
@app.get("/history/{userid}")
async def get_history(userid: str):
    return history_get(userid)