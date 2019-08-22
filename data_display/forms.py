from django import forms
from data_display.utils.constants import INDEPENDENT, INTERSECTION, UNION, MAP, ISELECT, ESELECT, CSV
from data_display import models
import inspect


def populate_choices_from_existing_tables():
    # populate choices fields from models
    choices = []
    for key, val in models.__dict__.items():
        if inspect.isclass(val):
            choices.append((key, key))

    return choices


def get_import_form_from_type(form_type):
    return {
        ISELECT: ImportSelectForm,
        INDEPENDENT: IndependentImportForm,
        INTERSECTION: IntersectionImportForm,
        UNION: UnionImportForm,
        MAP: MapImportForm
    }[form_type]()


def get_export_form_from_type(form_type):
    return {
        ESELECT: ExportSelectForm,
        CSV: ExportCSVForm
    }[form_type]()


class QueryTable(forms.Form):
    table = forms.ChoiceField(label="table",
    choices=[('Students', 'Students'),
             ('Projects', 'Projects'),
             ('Teams', 'Teams'),
             ('Not For Profits', 'Not For Profits')])
    filter = forms.CharField(label="filter", max_length=100, required=False)


class SettingsForm(forms.Form):
    rows_per_page = forms.ChoiceField(label="rows per page",
    choices=[(10,'10'),(25,'25'),(50,'50'),(100,'100')])


class ImportSelectForm(forms.Form):
    form_type = ISELECT
    import_type = forms.ChoiceField(label="Import Type",
                                    choices=[(INDEPENDENT, 'Independent'),
                                             (INTERSECTION, 'Intersection'),
                                             (UNION, 'Union'),
                                             (MAP, 'Map')])


class ImportForm(forms.Form):
    url = forms.URLField()


class IndependentImportForm(ImportForm):
    form_type = INDEPENDENT
    pass


class IntersectionImportForm(ImportForm):
    form_type = INTERSECTION

    choices = populate_choices_from_existing_tables()

    existing_table = forms.ChoiceField(label='Existing Table',
                                       choices=choices)


class UnionImportForm(ImportForm):
    form_type = UNION
    pass


class MapImportForm(ImportForm):
    form_type = MAP
    pass


class ExportSelectForm(forms.Form):
    form_type = ESELECT
    export_type = forms.ChoiceField(label="File Type",
                                    choices=[(CSV, 'csv'),
                                             ('xls', 'xls'),
                                             ('txt', 'txt'),
                                             ('json', 'json')])


class ExportCSVForm(forms.Form):
    form_type = CSV

    choices = populate_choices_from_existing_tables()

    existing_table = forms.ChoiceField(label='Existing Table',
                                       choices=choices)


class ConfirmThingForm(forms.Form):
    confirmed = forms.BooleanField(required=True,
                                   widget=forms.RadioSelect(choices=[('yes', 'Yes'),
                                                                     ('no', 'No')]))


class SummariesForm(forms.Form):
    table = forms.ChoiceField(label="table",
                              choices=[('Students', 'Students'), ('Projects', 'Projects'), ('Teams', 'Teams'),
                                       ('Not For Profits', 'Not For Profits')])
