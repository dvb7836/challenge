from collections import OrderedDict
import os
from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView

from challenge.settings import FETCHED_DATA_PATH, ITEMS_PER_PAGE
from star_wars_explorer.data_retriever import DataRetriever
from star_wars_explorer.data_loader import load_data
from star_wars_explorer.models import Collection
import petl as etl


def fetch_data(request):
    retriever = DataRetriever()
    retriever.run()

    return redirect("index")


class IndexView(ListView):
    model = Collection
    context_object_name = 'collections'
    template_name = "collection_list.html"


class CollectionView(TemplateView):
    template_name = "collection_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["filename"] = kwargs.get("filename")
        context["header"] = kwargs.get("header")
        context["table"] = kwargs.get("table")
        context["filters"] = kwargs.get("filters")
        context["page"] = int(kwargs.get("page", "-1"))

        return context

    def get(self, request, *args, **kwargs):
        page = int(request.GET.get('page', '1'))

        filename = kwargs.get("filename")
        data_path = os.path.join(FETCHED_DATA_PATH, filename)

        table = load_data(data_path)

        end_index = ITEMS_PER_PAGE + page if page == 1 else page * ITEMS_PER_PAGE + page - 1
        start_index = 1 if page == 1 else end_index - ITEMS_PER_PAGE

        kwargs["filters"] = table[0]
        kwargs["header"] = table[0]
        kwargs["table"] = table[start_index: end_index]
        kwargs["page"] = page if len(table) >= end_index else -1

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        filters = request.POST.getlist("filter")

        filename = kwargs.get("filename")
        data_path = os.path.join(FETCHED_DATA_PATH, filename)

        if not filters:
            return redirect("collection-view", filename=filename)

        table = load_data(data_path)
        aggregation = OrderedDict()
        aggregation['count'] = len
        aggregated_table = etl.aggregate(table, filters.pop() if len(filters) == 1 else filters, aggregation)

        kwargs["filters"] = table[0]
        kwargs["header"] = aggregated_table[0]
        kwargs["table"] = aggregated_table[1:]

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
