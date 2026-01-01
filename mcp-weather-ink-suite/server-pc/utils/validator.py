from pydantic import ValidationError
from models import EInkPayload

# Pydantic 校验逻辑封装

def validate_payload(data: dict) -> dict:
    """
    Validates the data against the EInkPayload schema.
    Returns the validated data as a dictionary (dumped model).
    """
    try:
        payload = EInkPayload(**data)
        return payload.model_dump()
    except ValidationError as e:
        print(f"Validation error: {e}")
        # In a real app, you might want to log this or raise a custom exception
        raise e
