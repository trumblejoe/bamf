from functools import reduce
import operator

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView, DetailView

from comics.models import Series


PAGINATE = 30


class SeriesList(LoginRequiredMixin, ListView):
    model = Series
    paginate_by = PAGINATE
    queryset = (
        Series.objects
        .prefetch_related('issue_set')
    )


class SeriesDetail(LoginRequiredMixin, DetailView):
    model = Series
    queryset = (
        Series.objects
        .prefetch_related('issue_set')
        .select_related('publisher')
    )


class SearchSeriesList(SeriesList):

    def get_queryset(self):
        result = super(SearchSeriesList, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list)))

        return result
