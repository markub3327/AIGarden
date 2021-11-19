class Table:
    def __init__(self, table):
        self._table = table


    @property
    def name(self):
        return self._table.__name__

    @property
    def thead(self):
        all_fields = self._table._meta.fields
        return [field.verbose_name for field in all_fields if field.verbose_name != "ID"]

    @property
    def tbody(self):
        columns = {}
        for row in self._table.objects.all():
            key, data = row.get_record()
            columns[key] = data

        # [t.strftime("%H:%M") for t in WateringSchedule.objects.all().order_by('time__hour').values_list('time', flat=True)]

        return columns

    @property
    def inputTypes(self):
        return self._table.input_types
