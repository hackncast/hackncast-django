from django.db.models.query import QuerySet


class BaseModelQuerySet(QuerySet):
    """QuerySet base dos models do sistema"""

    def actives(self):
        return self.filter(is_active=True)
