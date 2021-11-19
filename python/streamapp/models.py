from django.db import models


class Settings(models.Model):
    selectedMode = models.CharField(max_length=20, verbose_name="Selected mode")
    refreshInterval = models.PositiveIntegerField(
        default=1000, verbose_name="Refresh interval"
    )


class WateringSchedule(models.Model):
    time = models.TimeField(verbose_name="Time")

    input_types = ["time"]
    input_required = ["1"]

    def get_record(self):
        return self.pk, [self.time.strftime("%H:%M:%S")]


class GardenPlan(models.Model):
    p_type = models.CharField(max_length=20, verbose_name="Type")
    p_variety = models.CharField(max_length=20, verbose_name="Variety")
    p_planting_date = models.DateField(verbose_name="Planting (date)")
    p_location = models.JSONField(verbose_name="Location")

    input_types = ["str", "str", "date", "str"]
    input_required = ["1", "1", "1", "0"]

    def get_record(self):
        return self.pk, [
            self.p_type,
            self.p_variety,
            self.p_planting_date.strftime("%d.%m.%Y"),
            self.p_location,
        ]


class PlantSpecification(models.Model):
    p_type = models.CharField(max_length=20, verbose_name="Type")
    p_variety = models.CharField(max_length=20, verbose_name="Variety")
    p_num_of_seeds_in_1g = models.PositiveIntegerField(
        verbose_name="Number of seeds in 1g"
    )
    p_planting_date = models.JSONField(verbose_name="Planting (month)")
    p_planting_temp = models.JSONField(verbose_name="Planting temperature (°C)")
    p_planting_depth = models.JSONField(verbose_name="Planting depth (cm)")
    p_germination_time = models.JSONField(verbose_name="Germination (days)")
    p_harvest_time = models.JSONField(verbose_name="Harvest (days)")
    p_harvest_date = models.JSONField(verbose_name="Harvest (month)")
    p_length_of_root = models.JSONField(verbose_name="Length of root (cm)")
    p_watering_time = models.TimeField(verbose_name="Watering (duration)")
    p_class = models.CharField(max_length=20, verbose_name="Class")

    input_types = [
        "str",
        "str",
        "int",
        "range_month",
        "range",
        "range",
        "range",
        "range",
        "range_month",
        "range",
        "time",
        "str",
    ]
    input_required = ["1", "1", "0", "1", "1", "1", "1", "1", "1", "0", "1", "1"]

    def get_record(self):
        return self.pk, [
            self.p_type,
            self.p_variety,
            self.p_num_of_seeds_in_1g,
            self.p_planting_date,
            self.p_planting_temp,
            self.p_planting_depth,
            self.p_germination_time,
            self.p_harvest_time,
            self.p_harvest_date,
            self.p_length_of_root,
            self.p_watering_time.strftime("%H:%M:%S"),
            self.p_class,
        ]
