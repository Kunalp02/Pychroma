from chromadb import Documents, EmbeddingFunction, Embeddings
from chromadb.utils import embedding_functions
from django.contrib.auth import authenticate, login
from django.core.paginator import EmptyPage, Paginator
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from .forms import LoginForm, MetadataFilterForm, PaginationForm, SearchForm
from .utils import get_chroma_client, is_superuser, superuser_required


class MyEmbeddingFunction(EmbeddingFunction[Documents]):
    def __call__(self, input: Documents) -> Embeddings:
        sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="BAAI/bge-large-en-v1.5")
        embeddings = sentence_transformer_ef(input)
        return embeddings


custom = MyEmbeddingFunction()


@method_decorator(superuser_required, name="dispatch")
class ChromaLoginView(View):
    template_name = "chroma_admin.html"

    def get(self, request):
        if request.user.is_authenticated and is_superuser(request.user):
            return redirect(reverse("dashboard"))

        form = LoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None and is_superuser(user):
                login(request, user)
                return redirect(reverse("dashboard"))
            else:
                return HttpResponseForbidden(
                    "You do not have permission to access this page."
                )
        else:
            return render(
                request,
                self.template_name,
                {"form": form, "error_message": "Invalid login credentials"},
            )


@method_decorator(superuser_required, name="dispatch")
class DashboardView(View):
    template_name = "dashboard.html"

    def get(self, request):
        status = "Disconnected"
        try:
            chroma_client = get_chroma_client()
            status = "Connected"
            list_of_collections = chroma_client.list_collections()
            print(list_of_collections)
            context_data = []

            return render(
                request,
                self.template_name,
                {
                    "context_data": context_data,
                    "list_of_collections": list_of_collections,
                    "status": status,
                    "host": "localhost",
                    "port": 8000
                },
            )
        except Exception:
            return render(
                request,
                self.template_name,
                {
                    "status": status
                }
            )


@method_decorator(superuser_required, name="dispatch")
class CollectionView(View):
    template_name = "collection_view.html"

    def get(self, request, collection_name):
        try:
            chroma_client = get_chroma_client()
        except ValueError:
            return HttpResponseForbidden("Please Check if chroma server is running")

        list_of_collections = chroma_client.list_collections()
        openai_ef = custom

        try:
            collection = chroma_client.get_collection(
                name=collection_name, embedding_function=openai_ef
            )
        except ValueError:
            return HttpResponseForbidden(
                f"Collection {collection_name} does not exist."
            )
        search_form = SearchForm(request.GET)
        page_form = PaginationForm(request.GET, prefix="page")
        metadata_form = MetadataFilterForm(request.GET)

        if search_form.is_valid() and page_form.is_valid() and metadata_form.is_valid():
            if search_form.cleaned_data.get("search_query"):
                query_text = search_form.cleaned_data["search_query"]

                # Getting metadata filters from the form
                metadata_filters = {
                    key: value for key, value in metadata_form.cleaned_data.items() if value
                }
                # metadata_filters = {
                #     "source": "web",
                #     "novel" : "xyz"
                # }

                if len(metadata_filters) >= 2:
                    where_clause = {
                        "$and": [
                            {key: {"$eq": value}} for key, value in metadata_filters.items()
                        ]
                    }
                elif metadata_filters:
                    key, value = next(iter(metadata_filters.items()))
                    where_clause = {key: {"$eq": value}}
                else:
                    where_clause = {}

                r_collection = collection.query(
                    query_texts=[query_text],
                    where=where_clause,
                    include=["documents", "embeddings", "metadatas"],
                )
                # print(r_collection)
                data = list(
                    zip(
                        r_collection["ids"][0],
                        r_collection["embeddings"][0],
                        r_collection["documents"][0],
                        r_collection["metadatas"][0],
                    )
                )
            else:
                ids = collection.get()["ids"]
                r_collection = collection.get(
                    include=["embeddings", "documents", "metadatas"]
                )
                data = list(
                    zip(
                        ids,
                        r_collection.get("embeddings", []),
                        r_collection.get("documents", []),
                        r_collection.get("metadatas", []),
                    )
                )

            paginator = Paginator(data, 10)
            page = page_form.cleaned_data.get("page") or 1
            try:
                context_data = paginator.page(page)
            except EmptyPage:
                # Redirecting users to the last valid page
                return redirect(request.path + f"?page={paginator.num_pages}")

            return render(
                request,
                self.template_name,
                {
                    "context_data": context_data,
                    "selected_collection": collection_name,
                    "list_of_collections": list_of_collections,
                    "page_form": page_form,
                    "search_form": search_form,
                    "metadata_form": metadata_form,
                },
            )
        else:
            return HttpResponseForbidden("Form validation failed")
