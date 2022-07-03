class Table:
    def __init__(self, table):
        self._table = table

    @property
    def name(self):
        return self._table.__name__

    @property
    def thead(self):
        all_fields = self._table._meta.fields
        return [
            field.verbose_name for field in all_fields if field.verbose_name != "ID"
        ]

    @property
    def tbody_sorted(self):
        columns = {}
        for row in self._table.objects.all().order_by("time__hour"):
            key, data = row.get_record()
            columns[key] = data

        return columns

    @property
    def tbody(self):
        columns = {}
        for row in self._table.objects.all():
            key, data = row.get_record()
            columns[key] = data

        return columns

    @property
    def inputFields(self):
        return self._table.inputFields
