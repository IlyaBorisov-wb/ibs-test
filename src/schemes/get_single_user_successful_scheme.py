GET_SINGLE_USER_SUCCESSFUL_SCHEME = {
    '$schema': 'https://json-schema.org/draft/2020-12/schema',
    "type": "object",
    "properties": {
        "data": {
            "type": "object",
            "properties": {
                "id": {"type": "number"},
                "email": {"type": "string"},
                "first_name": {"type": "string"},
                "last_name": {"type": "string"},
                "avatar": {"type": "string"},
            },
            "required": ["id", "email", "first_name", "last_name", "avatar"],
        },
    }
}