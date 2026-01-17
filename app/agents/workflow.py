import joblib
import pandas as pd
from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.utils.ocr import extract_text_from_file
from app.services.vector_store import search_laws
import json
import os


llm = ChatOllama(model="llama3.2:1b", format="json", temperature=0)


try:
    risk_model = joblib.load('app/services/risk_model.pkl')
    print("✅ Risk Model loaded successfully.")
except:
    risk_model = None
    print("⚠️ Warning: Risk model not found. Please run 'train_risk_model.py' first.")


class AgentState(TypedDict):
    application_id: str
    documents_paths: List[str]
    raw_text: str               
    extracted_data: Dict[str, Any] 
    risk_score: str             
    relevant_laws: str          
    enablement_plan: str        
    final_decision: Dict[str, Any] 


def ocr_node(state: AgentState):
    print("--- STEP 1: OCR & MULTIMODAL PROCESSING ---")
    full_text = ""
    for path in state['documents_paths']:
        # دالة OCR اللي كتبناها في utils
        full_text += extract_text_from_file(path) + "\n"
    return {"raw_text": full_text}

def extraction_node(state: AgentState):
    print("--- STEP 2: DATA EXTRACTION (LLM) ---")
    parser = JsonOutputParser()
    prompt = PromptTemplate(
        template="Extract JSON with keys (full_name, total_income (int), family_size (int), job_title, skills) from the following text. If a value is missing or unclear, set it to 0 or 'Unknown'.\n\nText:\n{text}",
        input_variables=["text"],
    )
    chain = prompt | llm | parser
    try:
        data = chain.invoke({"text": state['raw_text']})
    except Exception as e:
        print(f"Extraction Error: {e}")
        data = {"full_name": "Unknown", "total_income": 0, "family_size": 1, "job_title": "Unemployed"}
    
    return {"extracted_data": data}

def risk_node(state: AgentState):
    print("--- STEP 3: ML RISK SCORING ---")
    data = state['extracted_data']
    risk_label = "LOW"
    
    if risk_model:
        try:
            input_data = pd.DataFrame([[
                float(data.get('total_income', 0)), 
                int(data.get('family_size', 1))
            ]], columns=['income', 'family_size'])
            
            prediction = risk_model.predict(input_data)[0]
            risk_label = "HIGH" if prediction == 1 else "LOW"
        except Exception as e:
            print(f"ML Error: {e}")
    
    print(f"📊 Calculated Risk: {risk_label}")
    return {"risk_score": risk_label}

def rag_node(state: AgentState):
    print("--- STEP 4: LEGAL COMPLIANCE CHECK (RAG) ---")
    query = f"Rules for income {state['extracted_data'].get('total_income')} and document content: {state['raw_text'][:100]}"
    results = search_laws(query)
    laws = "\n".join([doc.page_content for doc in results])
    return {"relevant_laws": laws}

def enablement_node(state: AgentState):
    print("--- STEP 5: ECONOMIC ENABLEMENT PLANNING ---")
    data = state['extracted_data']
    
    prompt = PromptTemplate(
        template="""
        Based on the applicant's profile, suggest a brief 'Economic Enablement Plan'.
        Profile -> Job: {job}, Skills: {skills}
        
        Task: Suggest 2 suitable job roles and 1 upskilling course to improve their income.
        Output: A simple text summary.
        """,
        input_variables=["job", "skills"],
    )
    chain = prompt | llm 
    plan = chain.invoke({
        "job": data.get('job_title', 'Unemployed'),
        "skills": data.get('skills', 'None')
    })
    return {"enablement_plan": plan.content if hasattr(plan, 'content') else str(plan)}

def decision_node(state: AgentState):
    print("--- STEP 6: FINAL DECISION ORCHESTRATION ---")
    
    prompt = PromptTemplate(
        template="""
        You are a Senior Social Support Officer. Make a final decision on this application.
        
        1. Applicant Data: {data}
        2. ML Risk Score: {risk} (CRITICAL: If HIGH, treat with caution or Reject)
        3. Legal Laws: {laws} (CRITICAL: If laws forbid product images/fraud, Reject)
        4. Enablement Plan: {plan}
        
        Output strictly valid JSON:
        {{
            "status": "APPROVED" or "REJECTED" or "SOFT_DECLINE",
            "financial_support_amount": 0 (if rejected) or Amount,
            "enablement_recommendation": "Copy the plan here",
            "reasoning": "Explain the decision referencing Risk Score and Laws."
        }}
        """,
        input_variables=["data", "risk", "laws", "plan"],
    )
    chain = prompt | llm | JsonOutputParser()
    
    try:
        decision = chain.invoke({
            "data": json.dumps(state['extracted_data']),
            "risk": state['risk_score'],
            "laws": state['relevant_laws'],
            "plan": state['enablement_plan']
        })
    except:
        decision = {"status": "ERROR", "reasoning": "Failed to generate decision json"}
    
    return {"final_decision": decision}

workflow = StateGraph(AgentState)

workflow.add_node("ocr", ocr_node)
workflow.add_node("extract", extraction_node)
workflow.add_node("risk_ml", risk_node)
workflow.add_node("rag", rag_node)
workflow.add_node("enablement", enablement_node)
workflow.add_node("decide", decision_node)

workflow.set_entry_point("ocr")
workflow.add_edge("ocr", "extract")
workflow.add_edge("extract", "risk_ml")
workflow.add_edge("risk_ml", "rag")
workflow.add_edge("rag", "enablement")
workflow.add_edge("enablement", "decide")
workflow.add_edge("decide", END)

social_support_app = workflow.compile()