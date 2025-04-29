from flask import abort

def validate_required_fields(data: dict, required_fields: list) -> None:
    """Проверяет наличие и непустоту обязательных полей"""
    for field in required_fields:
        value = data.get(field, '').strip()
        if not value:
            abort(400, f'Поле {field} не может быть пустым')
    
def validate_length(data: dict, limits: dict) -> None:
    """Проверяет максимальную длину полей"""
    for field, max_len in limits.items():
        value = data.get(field, '')
        if len(value) > max_len:
            abort(400, f'Максимальная длина поля {field} - {max_len} символов')
