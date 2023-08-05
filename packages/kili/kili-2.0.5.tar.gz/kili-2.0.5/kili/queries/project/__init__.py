from ...helpers import deprecate, format_result, fragment_builder
from .queries import gql_projects, GQL_PROJECTS_COUNT
from ...types import Project
from ...constants import NO_ACCESS_RIGHT


class QueriesProject:

    def __init__(self, auth):
        """
        Initializes the subclass

        Parameters
        ----------
        - auth : KiliAuth object
        """
        self.auth = auth

    @deprecate(
        """
        **New feature has been added : Query only the fields you want
        using the field argument, that accept a list of string organized like below.**
        The former default query with all fields is deprecated since 13/05/2020
        After 13/06/2020, the default queried fields will be :
        ['id', 'consensusTotCoverage', 'inputType', 'interfaceCategory', 'jsonInterface', 
        'maxWorkerCount', 'minAgreement', 'minConsensusSize', 'roles.id', 'roles.role', 
        'roles.user.email', 'roles.user.id', 'roles.user.name', 'title']
        To fetch more fields, for example the consensus fields, just add those :
        fields = ['id', 'consensusMark', 'consensusTotCoverage', 'createdAt', 'description', 
        'honeypotMark', 'inputType', 'interfaceCategory', 'jsonInterface', 'maxWorkerCount', 
        'minAgreement', 'minConsensusSize', 'numberOfAssets', 'numberOfAssetsWithSkippedLabels', 
        'numberOfRemainingAssets', 'numberOfReviewedAssets', 'numberOfRoles',
        'roles.id', 'roles.activated', 'roles.consensusMark', 'roles.honeypotMark', 'roles.lastLabelingAt', 
        'roles.numberOfAnnotations', 'roles.numberOfLabels', 'roles.role', 'roles.starred', 
        'roles.totalDuration', 'roles.user.email', 'titleAndDescription', 'useHoneyPot']
        """)
    def projects(self, project_id: str = None, search_query: str = None, updated_at_gte: str = None, updated_at_lte: str = None, skip: int = 0, fields: list = ['consensusMark', 'consensusTotCoverage', 'createdAt', 'description', 'honeypotMark', 'id', 'inputType', 'interfaceCategory', 'jsonInterface', 'maxWorkerCount', 'minAgreement', 'minConsensusSize', 'numberOfAssets', 'numberOfAssetsWithSkippedLabels', 'numberOfRemainingAssets', 'numberOfReviewedAssets', 'numberOfRoles',
                                                                                                                                                                'roles.activated', 'roles.consensusMark', 'roles.honeypotMark', 'roles.id', 'roles.lastLabelingAt', 'roles.numberOfAnnotations', 'roles.numberOfLabeledAssets', 'roles.numberOfLabels', 'roles.role', 'roles.starred', 'roles.totalDuration', 'roles.user.email', 'roles.user.id', 'roles.user.name', 'title', 'titleAndDescription', 'updatedAt', 'useHoneyPot'], first: int = 100):
        """
        Get projects with a search_query

        Parameters
        ----------
        - project_id : str, optional (default = None)
            Select a specific project through its project_id
        - search_query : str, optional (default = None)
            Returned projects have a title or a description that matches this string.
        - updated_at_gte : string, optional (default = None)
            Returned projects should have a label whose update date is greated or equal to this date.
            Formatted string should have format : "YYYY-MM-DD"
        - updated_at_lte : string, optional (default = None)
            Returned projects should have a label whose update date is lower or equal to this date.
            Formatted string should have format : "YYYY-MM-DD"
        - skip : int, optional (default = 0)
            Number of projects to skip (they are ordered by their creation)
        - fields : list of string, optional (default = ['consensusTotCoverage', 'id', 'inputType', 'interfaceCategory', 'jsonInterface', 'maxWorkerCount', 'minAgreement', 'minConsensusSize', 'roles.id', 'roles.role', 'roles.user.email', 'roles.user.id', 'roles.user.name', 'title'])
            All the fields to request among the possible fields for the projects, default for None are the non-calculated fields)
            Possible fields : see https://cloud.kili-technology.com/docs/python-graphql-api/graphql-api/#project
        - first : int , optional (default = 100)
            Maximum number of projects to return. Can only be between 0 and 100.

        Returns
        -------
        - a result object which contains the query if it was successful, or an error message else.
        """
        GQL_PROJECTS = gql_projects(fragment_builder(fields, Project))
        variables = {
            'where': {
                'id': project_id,
                'searchQuery': search_query,
                'updatedAtGte': updated_at_gte,
                'updatedAtLte': updated_at_lte,
            },
            'skip': skip,
            'first': first
        }
        result = self.auth.client.execute(GQL_PROJECTS, variables)
        return format_result('data', result)

    def count_projects(self, project_id: str = None, search_query: str = None, updated_at_gte: str = None, updated_at_lte: str = None):
        """
        Counts the number of projects with a search_query

        Parameters
        ----------
        - project_id : str, optional (default = None)
            Select a specific project through its project_id
        - search_query : str, optional (default = None)
            Returned projects have a title or a description that matches this string.
        - updated_at_gte : string, optional (default = None)
            Returned projects should have a label whose update date is greated or equal to this date.
            Formatted string should have format : "YYYY-MM-DD"
        - updated_at_lte : string, optional (default = None)
            Returned projects should have a label whose update date is lower or equal to this date.
            Formatted string should have format : "YYYY-MM-DD"

        Returns
        -------
        - a positive integer corresponding to the number of results of the query if it was successful, or an error message else.
        """
        variables = {
            'where': {
                'id': project_id,
                'searchQuery': search_query,
                'updatedAtGte': updated_at_gte,
                'updatedAtLte': updated_at_lte,
            }
        }
        result = self.auth.client.execute(GQL_PROJECTS_COUNT, variables)
        count = format_result('data', result)
        return count
