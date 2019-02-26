from typing import Optional, Union, List

from graphql import GraphQLNonNull, GraphQLScalarType, GraphQLObjectType, GraphQLList

import strawberry
from strawberry.type_converter import get_graphql_type_for_annotation


def test_union():
    @strawberry.type
    class A:
        x: int

    @strawberry.type
    class B:
        x: int

    field = get_graphql_type_for_annotation(Union[A, B], "Example")

    assert type(field) == GraphQLNonNull

    assert field.of_type.name == "Example"

    assert A.field in field.of_type.types
    assert B.field in field.of_type.types


def test_optional_scalar():
    field = get_graphql_type_for_annotation(Optional[str], "Example")

    assert type(field) == GraphQLScalarType
    assert field.name == "String"


def test_optional_object_type():
    @strawberry.type
    class A:
        x: int

    field = get_graphql_type_for_annotation(Optional[A], "Example")

    assert type(field) == GraphQLObjectType
    assert field.name == "A"


def test_list_of_scalar():
    field = get_graphql_type_for_annotation(List[str], "Example")

    assert type(field) == GraphQLList
    assert type(field.of_type) == GraphQLNonNull
    assert type(field.of_type.of_type) == GraphQLScalarType
    assert field.of_type.of_type.name == "String"

    field = get_graphql_type_for_annotation(List[Optional[str]], "Example")

    assert type(field) == GraphQLList
    assert type(field.of_type) == GraphQLScalarType
    assert field.of_type.name == "String"


def test_list_of_object_types():
    @strawberry.type
    class A:
        x: int

    field = get_graphql_type_for_annotation(List[A], "Example")

    assert type(field) == GraphQLList
    assert type(field.of_type) == GraphQLNonNull
    assert type(field.of_type.of_type) == GraphQLObjectType
    assert field.of_type.of_type.name == "A"

    field = get_graphql_type_for_annotation(List[Optional[A]], "Example")

    assert type(field) == GraphQLList
    assert type(field.of_type) == GraphQLObjectType
    assert field.of_type.name == "A"
