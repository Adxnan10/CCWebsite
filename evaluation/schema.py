from typing import Dict, Any
from django.db.models.base import Model

import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphene_file_upload.scalars import Upload
from graphql import GraphQLError
from graphene_django_crud.types import DjangoGrapheneCRUD, resolver_hints
from graphene_django_crud.utils import is_required

from django.contrib.auth.models import User, Group
from graphql_auth.constants import Messages
from graphql_auth.decorators import login_required
from . import models
from .utils import is_owner




class InstructorType(DjangoGrapheneCRUD):
    '''
    A type for the `evaluation.Instructor` model. 
    '''

    class Meta:
        model = models.Instructor

    @classmethod
    def before_create(cls, parent, info, instance, data):
        user: User = info.context.user
        if user.has_perm("evaluation.add_instructor"):
            raise GraphQLError("You don't have permission")
        return
    
    @classmethod
    def before_update(cls, parent, info, instance, data):
        user: User = info.context.user
        if not user.has_perm("evaluation.update_instructor"):
            raise GraphQLError("You don't have permission")
        return
    
    @classmethod
    def before_delete(cls, parent, info, instance, data):
        user: User = info.context.user
        if user.has_perm("evaluation.delete_instructor"):
            raise GraphQLError("You don't have permission")
        return


class EvaluationType(DjangoGrapheneCRUD):
    """
    A type for the `evaluation.Evaluation` model. 
    """

    class Meta:
        model = models.Evaluation

    @classmethod
    def before_create(cls, parent, info, instance, data) -> None:
        pk = data['instructor']['connect']['id']['equals']
        
        if models.Evaluation.objects.filter(user=info.context.user, instructor__pk=pk):
            raise GraphQLError("You have evaluated this instructor before, you can edit it in My Evaluations")
        return

    # Forbid user to change other users' evaluation
    @classmethod
    @is_owner
    def before_update(cls, parent, info, instance, data) -> None:
        return
            
    @classmethod
    @is_owner
    def before_delete(cls, parent, info, instance, data) -> None:
        return



# Main entry for all the query types
# Now only provides all Instructor & Evaluation objects
class Query(ObjectType):

    evaluation = EvaluationType.ReadField()
    evaluations = EvaluationType.BatchReadField()

    instructor = InstructorType.ReadField()
    instructors = InstructorType.BatchReadField()


# Main entry for all Mutation types
class Mutation(ObjectType):

    evaluation_create = EvaluationType.CreateField()
    evaluation_update = EvaluationType.UpdateField()
    evaluation_delete = EvaluationType.DeleteField()

    instructor_create = InstructorType.CreateField()
    instructor_update = InstructorType.UpdateField()
    instructor_delete = InstructorType.DeleteField()