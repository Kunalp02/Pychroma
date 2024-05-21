import chromadb
from django.shortcuts import redirect


def get_chroma_client():
    return chromadb.HttpClient(
        host="localhost",
        port=8000,
    )


def is_superuser(user):
    return user.is_superuser


def superuser_required(view_func):
    def decorator(request, *args, **kwargs):
        if request.user.is_authenticated and is_superuser(request.user):
            return view_func(request, *args, **kwargs)
        else:
            login_url = f"{request.scheme}://{request.get_host()}/admin/"
            return redirect(login_url)

    return decorator

# def get_openai_embedding_function():
#     return embedding_functions.OpenAIEmbeddingFunction(
#         api_key=settings.OPENAI_API_KEY, model_name="text-embedding-ada-002"
#     )
