def edit_interaction_tool(interaction_id: int, updated_note: str):
    return {
        "interaction_id": interaction_id,
        "updated_note": updated_note,
        "message": "Interaction updated successfully"
    }