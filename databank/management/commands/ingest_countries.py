import pandas as pd
import json
from databank.models import Country
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        data = pd.read_csv(r"./databank/management/commands/countries.csv")

        data = data[['Country Name', 'Country Code', '2021']]

        shapes = json.load(open(r"./databank/management/commands/country_shapes.geojson", 'r'))
        shapes = pd.DataFrame(shapes['features'])

        shapes['country_name'] = shapes['properties'].apply(lambda x: x['cntry_name'])
        shapes['country_code'] = shapes['properties'].apply(lambda x: x['iso3'])
        shapes.loc[shapes.country_name == "Czech Republic", "country_code"] = "CZE"
        shapes.loc[shapes.country_name == "Laos", "country_code"] = "LAO"
        shapes.loc[shapes.country_name == "South Korea", "country_code"] = "KOR"
        shapes.loc[shapes.country_name == "Grenada", "country_code"] = "GRD"
        shapes.loc[shapes.country_name == "Federated States of Micronesia", "country_code"] = "FSM"
        shapes.loc[shapes.country_name == "Norway", "country_code"] = "NOR"
        shapes.loc[shapes.country_name == "Mayotte", "country_code"] = "MYT"
        shapes.loc[shapes.country_name == "Swaziland", "country_code"] = "SWZ"
        shapes.loc[shapes.country_name == "North Korea", "country_code"] = "PRK"
        shapes.loc[shapes.country_name == "France", "country_code"] = "FRA"

        shapes = shapes.merge(data, right_on='Country Code', left_on='country_code', how='left')

        for index, row in shapes.iterrows():
            country = Country.objects.create(
                name=row['country_name'],
                code=row['country_code'],
                area=row['2021']
            )
            content_file = ContentFile(json.dumps(row['geometry']))
            country.shape.save(f'{row["country_code"]}.geojson', content_file)
            country.save()
