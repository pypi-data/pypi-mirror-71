from .config_chapter import ConfigChapter


class Publisher(ConfigChapter):
    validation_schema = {
        "type": "object",
        "required": [
            "author",
            "company"
        ],
        "properties": {
            "author": {
                "type": "string",
                "title": "Author of the Service",
                "description": "An explanation about the purpose of this instance.",
                "maxLength": 255
            },
            "company": {
                "type": "string",
                "title": "Author Company",
                "description": "Developer Company, Division etc.",
                "maxLength": 255
            },
        },
    }

    @staticmethod
    def from_yaml(input_dict):
        p = Publisher()
        if p.validate(input_dict, validation_schema=p.validation_schema):
            p.author = input_dict.get('author')
            p.company = input_dict.get('company')
            return p
