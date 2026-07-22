from langchain_openai import ChatOpenAI
from graph.roadmapstate import RoadmapState
import os
import json
from dotenv import load_dotenv
load_dotenv()
llm = ChatOpenAI(
    model="google/gemma-3-12b-it",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPEN_ROUTER_KEY")
)



def roadmap_generator(state: RoadmapState):
    print("===== Roadmap Generator =====")
    prompt = f"""
    You are an expert AI Learning Roadmap Generator.

Generate a personalized study roadmap.
for a {state['student_class']} student in detailed 
Goal:
{state["goal"]}

Current Level:
{state["level"]}

Duration:
{state["duration"]}

Study Time:
{state["hours_per_day"]} hours/day

Instructions:
- Divide the roadmap into weekly phases.
- Each phase should have:
  - title
  - description
- Keep descriptions concise (2-3 sentences).
- Do NOT include introductions or conclusions.
- Return ONLY valid JSON.
- Do NOT use markdown.
- Do NOT wrap the JSON inside code blocks.

Return JSON exactly in this format:

{{
  "roadmap": [
    {{
      "title": "Week 1",
      "description": "Learn the basic concepts of the subject."
    }},
    {{
      "title": "Week 2",
      "description": "Practice fundamental problems and strengthen concepts."
    }},
    {{
      "title": "Week 3",
      "description": "Study advanced topics with examples."
    }},
    {{
      "title": "Week 4",
      "description": "Revise everything and solve mock tests."
    }}
  ]
}}"""
    response = llm.invoke(prompt)
    text = response.content
    text = text.replace("```json", "").replace("```", "").strip()
    roadmap = json.loads(text)
    return {
        "roadmap": roadmap["roadmap"]

    }