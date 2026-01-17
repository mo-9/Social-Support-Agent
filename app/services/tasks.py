from app.core.celery_app import celery_app
from app.agents.workflow import social_support_app

@celery_app.task(name="process_application")
def process_application_task(application_id: str, documents_paths: list):
    
    initial_state = {
        "application_id": application_id,
        "documents_paths": documents_paths,
        "raw_text": "",
        "extracted_data": {},
        "risk_score": "LOW",
        "relevant_laws": "",
        "enablement_plan": "",
        "final_decision": {}
    }
    
    final_state = social_support_app.invoke(initial_state)
    
    return final_state