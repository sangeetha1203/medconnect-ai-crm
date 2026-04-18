from fastapi import APIRouter
from app.services.langgraph_agent import graph
from app.database import SessionLocal, Interaction

router = APIRouter(
    prefix="/interaction",
    tags=["HCP Interaction"]
)

@router.post("/ai-log")
def ai_log_interaction(payload: dict):
    db = SessionLocal()

    result = graph.invoke({
        "input_text": payload["text"]
    })

    new_interaction = Interaction(
        notes=payload["text"],
        ai_summary=result["log_result"].get(
            "ai_extracted_result",
            "No summary generated"
        )
    )

    db.add(new_interaction)
    db.commit()
    db.refresh(new_interaction)

    return {
        "message": "Interaction saved successfully",
        "saved_id": new_interaction.id,
        "result": result
    }


@router.put("/edit/{interaction_id}")
def edit_interaction(interaction_id: int, payload: dict):
    db = SessionLocal()

    interaction = db.query(Interaction).filter(
        Interaction.id == interaction_id
    ).first()

    if not interaction:
        return {"error": "Interaction not found"}

    interaction.notes = payload.get(
        "notes",
        interaction.notes
    )

    interaction.ai_summary = payload.get(
        "summary",
        interaction.ai_summary
    )

    db.commit()
    db.refresh(interaction)

    return {
        "message": "Interaction updated successfully",
        "id": interaction.id,
        "notes": interaction.notes,
        "summary": interaction.ai_summary
    }


@router.get("/history")
def get_history():
    db = SessionLocal()

    interactions = db.query(Interaction).all()

    return {
        "history": [
            {
                "id": item.id,
                "notes": item.notes,
                "summary": item.ai_summary
            }
            for item in interactions
        ]
    }

@router.get("/search")
def search_interaction(keyword: str):
    db = SessionLocal()

    results = db.query(Interaction).filter(
        Interaction.notes.ilike(f"%{keyword}%")
    ).all()

    return {
        "results": [
            {
                "id": item.id,
                "notes": item.notes,
                "summary": item.ai_summary
            }
            for item in results
        ]
    }

@router.get("/score/{interaction_id}")
def get_opportunity_score(interaction_id: int):
    db = SessionLocal()

    interaction = db.query(Interaction).filter(
        Interaction.id == interaction_id
    ).first()

    if not interaction:
        return {"error": "Interaction not found"}

    notes_text = interaction.notes.lower()

    score = 65
    priority = "Medium"

    if "requested" in notes_text or "follow-up" in notes_text:
        score = 92
        priority = "High"
    elif "interested" in notes_text:
        score = 85
        priority = "High"

    return {
        "id": interaction.id,
        "opportunity_score": score,
        "priority": priority,
        "recommendation": "Prioritize follow-up visit"
    }


@router.delete("/delete/{interaction_id}")
def delete_interaction(interaction_id: int):
    db = SessionLocal()

    interaction = db.query(Interaction).filter(
        Interaction.id == interaction_id
    ).first()

    if not interaction:
        return {"error": "Interaction not found"}

    db.delete(interaction)
    db.commit()

    return {
        "message": "Interaction deleted successfully",
        "id": interaction_id
    }