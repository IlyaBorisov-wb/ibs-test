POST_REGISTER_SUCCESSFUL_SCHEME = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "id": {
            "type": "integer"
        },
        "token": {
            "type": "string"
        }
    },
    "required": [
        "id",
        "token"
    ]
}