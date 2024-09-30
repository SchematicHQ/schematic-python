# This file was auto-generated by Fern from our API Definition.


from schematic.core.query_encoder import encode_query


def test_query_encoding_deep_objects() -> None:
    assert encode_query({"hello world": "hello world"}) == [("hello world", "hello world")]
    assert encode_query({"hello_world": {"hello": "world"}}) == [("hello_world[hello]", "world")]
    assert encode_query({"hello_world": {"hello": {"world": "today"}, "test": "this"}, "hi": "there"}) == [
        ("hello_world[hello][world]", "today"),
        ("hello_world[test]", "this"),
        ("hi", "there"),
    ]


def test_query_encoding_deep_object_arrays() -> None:
    assert encode_query({"objects": [{"key": "hello", "value": "world"}, {"key": "foo", "value": "bar"}]}) == [
        ("objects[key]", "hello"),
        ("objects[value]", "world"),
        ("objects[key]", "foo"),
        ("objects[value]", "bar"),
    ]
    assert encode_query(
        {"users": [{"name": "string", "tags": ["string"]}, {"name": "string2", "tags": ["string2", "string3"]}]}
    ) == [
        ("users[name]", "string"),
        ("users[tags]", "string"),
        ("users[name]", "string2"),
        ("users[tags]", "string2"),
        ("users[tags]", "string3"),
    ]


def test_encode_query_with_none() -> None:
    encoded = encode_query(None)
    assert encoded == None
