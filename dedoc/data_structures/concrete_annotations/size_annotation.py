from flask_restplus import fields, Api, Model

from dedoc.data_structures.annotation import Annotation


class SizeAnnotation(Annotation):
    def __init__(self, start: int, end: int, value: str):
        try:
            float(value)
        except ValueError:
            raise ValueError("the value of size annotation should be a number")
        super().__init__(start=start, end=end, name="size", value=value)

    @staticmethod
    def get_api_dict(api: Api) -> Model:
        return api.model('SizeAnnotation', {
            'start': fields.Integer(description='annotation start index', required=True, example=0),
            'end': fields.Integer(description='annotation end index', required=True, example=4),
            'value': fields.String(description='the size of the text in points (1/72 of an inch)',
                                   required=True,
                                   example="18.5")
        })
