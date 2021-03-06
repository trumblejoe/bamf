from functools import reduce
import operator

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView, DetailView

from comics.models import Team


PAGINATE = 30


class TeamList(LoginRequiredMixin, ListView):
    model = Team
    paginate_by = PAGINATE


class TeamDetail(LoginRequiredMixin, DetailView):
    model = Team

    def get_context_data(self, **kwargs):
        context = super(TeamDetail, self).get_context_data(**kwargs)
        team = self.get_object()
        context['issue_list'] = (
            team.issue_set.all()
            .select_related('series')
            .only('slug', 'cover', 'number', 'status', 'series__name')
        )
        return context


class SearchTeamList(TeamList):

    def get_queryset(self):
        result = super(SearchTeamList, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list)))

        return result
