from django import forms


class QueryTable(forms.Form):
    table = forms.ChoiceField(label="table",
    choices=[('Students','Students'), ('Projects', 'Projects'), ('Teams', 'Teams'), ('Not For Profits', 'Not For Profits')])
    filter = forms.CharField(label="filter", max_length=100, required=False)


class SettingsForm():
    rows_per_page = forms.ChoiceField(label="rows per page",
    choices=[(10,'10'),(25,'25'),(50,'50'),(100,'100')])
