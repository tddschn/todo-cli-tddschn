import json
# from todo_cli_typer import TodoItem


def merge_desc(desc_l: list[str]) -> str:
    return ' '.join(desc_l)


# def serialize_todo(todo: TodoItem) -> dict:
#     return {
#         'id': todo.id,
#         'description': todo.description,
#         'priority': todo.priority.value,
#         'status': todo.status.value,
#         'project': todo.project,
#         'tags': todo.tags,
#         'due_date': todo.due_date,
#     }


def row2dict(row) -> dict:
    d = row.__dict__
    d.pop('_sa_instance_state', None)
    # from icecream import ic
    # ic(d)
    d_ordered = {
        k: d[k]
        for k in [
            'id', 'description', 'priority', 'status', 'project', 'tags',
            'due_date'
        ]
    }
    return d_ordered


def serialize_tags(tags: list[str]) -> str:
    return json.dumps(tags)


def deserialize_tags(tags_s: str) -> list[str]:
    return json.loads(tags_s)
