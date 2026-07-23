from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import json,os


class EvaluationAgent:


    def __init__(self):

        # Judge LLM
        self.llm = ChatOpenAI(
           model="google/gemma-3-12b-it",
             base_url="https://openrouter.ai/api/v1",
             api_key=os.getenv("OPEN_ROUTER_KEY")
        )


    def faithfulness(self, question, answer, context):


        prompt = ChatPromptTemplate.from_template(
        """
        You are a RAG evaluation expert.

        Question:
        {question}

        Context:
        {context}

        Answer:
        {answer}


        Check if answer is completely supported by context.

        Give score:
        1 -> Fully supported
        0 -> Hallucinated information


        Return only JSON:

        {{
        "score":0 / 1,
        "reason":"explanation",
         "confidence_score": percentage,
         "correctness" :percentage
        }}

        """
        )


        response = self.llm.invoke(
            prompt.format(
                question=question,
                answer=answer,
                context="\n".join(context)
            )
        )
        content = response.content.strip()
        # Remove markdown fences
        content = content.replace("```json", "")
        content = content.replace("```", "").strip()


        return json.loads(content)



    def context_precision(self, question, context):


        prompt = ChatPromptTemplate.from_template(
        """
        You are a retrieval evaluator.


        Question:
        {question}


        Retrieved Documents:

        {context}


        Judge whether retrieved documents help answer
        the question.


        Score:

        1 = All documents relevant
        0 = None relevant


        Return JSON:

        {{
        "score":number,
        "reason":"explanation",
        "confidence_score": percentage,
        "correctness":percentage
        }}

        """
        )


        response = self.llm.invoke(
            prompt.format(
                question=question,
                context="\n\n".join(context)
            )
        )
        content = response.content.strip()
                # Remove markdown fences
        content = content.replace("```json", "")
        content = content.replace("```", "").strip()


        return json.loads(content)



    def evaluate(self,state):


        question = state["question"]

        answer = state["explanation"]

        context = state["verified_context"]



        faithfulness_result = self.faithfulness(
            question,
            answer,
            context
        )


        precision_result = self.context_precision(
            question,
            context
        )


        state["evaluation"]={

            "faithfulness":
            faithfulness_result,


            "context_precision":
            precision_result
        }


        return state