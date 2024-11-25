def to_dict(message: str) -> dict[str, list]:
    return {
        'detail': [
            {
                'loc': ['', 0],
                'msg': message,
                'type': 'error',
            },
        ],
    }
