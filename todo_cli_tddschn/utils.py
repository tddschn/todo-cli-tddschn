import json
from sqlmodel import Session, select
from .database import engine
from .models import Project, Todo


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


def todo_to_dict_with_project_name(todo: Todo) -> dict:
    d = todo.__dict__
    d.pop('_sa_instance_state', None)
    # from icecream import ic
    # ic(d)
    attr_list_1 = ['id', 'description', 'priority', 'status']
    attr_list_2 = ['tags', 'due_date']
    d_ordered = {k: d[k] for k in attr_list_1}
    if d['project_id'] is not None:
        project_id = d['project_id']
        with Session(engine) as session:
            project = session.get(Project, project_id)
            assert project is not None
            d_ordered['project'] = project.name
    else:
        d_ordered['project'] = None

    d_ordered |= {k: d[k] for k in attr_list_2}

    return d_ordered


def serialize_tags(tags: list[str]) -> str:
    return json.dumps(tags)


def deserialize_tags(tags_s: str) -> list[str]:
    return json.loads(tags_s)
