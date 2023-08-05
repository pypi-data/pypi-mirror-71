from typing import *

from onlinejudge_template.generator._utils import get_analyzed


def class_name(data: Dict[str, Any]) -> str:
    definition = get_analyzed(data).topcoder_class_definition
    if definition is None:
        return 'theClassName'
    return definition.class_name


def method_name(data: Dict[str, Any]) -> str:
    definition = get_analyzed(data).topcoder_class_definition
    if definition is None:
        return 'theMethodName'
    return definition.method_name
