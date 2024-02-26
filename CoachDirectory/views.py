from django.db.models import Q, Avg

from django.shortcuts import render

from django.views.generic import ListView

from Users.models import Coach

class CoachListView(ListView):
    model = Coach
    template_name = 'CoachDirectory/coach_list.html'
    context_object_name = 'coaches'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', '')
        specializations_filter = self.request.GET.get('specializations', '')
        location_filter = self.request.GET.get('location', '')

        if search_query:
            queryset = queryset.filter(
                Q(full_name__icontains=search_query) |
                Q(qualifications__icontains=search_query)
            )

        if specializations_filter:
            queryset = queryset.filter(specializations__icontains=specializations_filter)

        if location_filter:
            queryset = queryset.filter(location__icontains=location_filter)

        queryset = queryset.annotate(average_rating=Avg('reviews__rating'))
        
        queryset = queryset.order_by('-average_rating')

        return queryset
