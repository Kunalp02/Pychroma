from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())


class PaginationForm(forms.Form):
    page = forms.IntegerField(min_value=1, required=False)


class SearchForm(forms.Form):
    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "search-input", "placeholder": "Enter Search Query"}
        ),
    )


class MetadataFilterForm(forms.Form):
    plan_uuid = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "filter-input", "placeholder": "Plan uuid"}
        ),
    )
    topic_uuid = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "filter-input", "placeholder": "Topic uuid"}
        ),
    )

    topic_type = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "filter-input", "placeholder": "Topic type"}
        ),
    )
    topic_url = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "filter-input", "placeholder": "Topic url"}
        ),
    )

    topic_netloc = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "filter-input", "placeholder": "Topic netloc"}
        ),
    )
    task_uuid = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "filter-input", "placeholder": "Task uuid"}
        ),
    )
    task_type = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "filter-input", "placeholder": "Task type"}
        ),
    )
    task_url = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "filter-input", "placeholder": "Task url"}
        ),
    )
    task_netloc = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "filter-input", "placeholder": "Task netloc"}
        ),
    )
    product_uuid = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "filter-input", "placeholder": "Product uuid"}
        ),
    )
    product_url = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "filter-input", "placeholder": "Product url"}
        ),
    )
    product_netloc = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "filter-input", "placeholder": "Product netloc"}
        ),
    )
