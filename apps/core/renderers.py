import json
import decimal
from datetime import date, datetime
from rest_framework.renderers import JSONRenderer

class ExtendedEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, complex):
            return [obj.real, obj.imag]
        elif isinstance(obj, decimal.Decimal):
            return str(obj)
        elif isinstance(obj, (date, datetime)):
            return obj.isoformat()
        elif isinstance(obj, str):
            # This ignores all non utf chars in the JSON
            # It helps then to avoid some conflicts with partners systems
            return bytes(obj, "utf-8").decode("utf-8", "ignore")
        elif not isinstance(obj, str):
            return str(obj)
        # TODO : Detect models and encode string json as '{"id": 1238, "model": "clients.BankClient"}'

        # Let the base class default method raise the TypeError
        return super().default(obj)

class ApiRenderer(JSONRenderer):
    charset = "utf-8"
    object_label = "object"
    pagination_object_label = "objects"
    pagination_object_count = "count"
    pagination_count_label = pagination_object_count  # To solve a bug

    def render(self, data, media_type=None, renderer_context=None):
        if getattr(data, "get", None):
            if {"status", "code", "message"}.issubset(data.keys()):
                return super().render(data, media_type, renderer_context)

            if data.get("results", None) is not None:
                # Handle Elasticsearch response format
                if data.get("pagination", None) is not None:
                    # Elasticsearch format: count is in pagination.count
                    count = data["pagination"].get("count", 0)
                else:
                    # Standard format: count is at top level
                    count = data.get("count", 0)

                results_return_data = {
                    self.pagination_object_label: data["results"],
                    self.pagination_count_label: count,
                }

                # Handle aggregations/facets
                if data.get("aggregations", None) is not None:
                    results_return_data["facets"] = data["aggregations"]
                elif data.get("facets", None) is not None:
                    results_return_data["facets"] = data["facets"]

                return json.dumps(results_return_data, cls=ExtendedEncoder)

            # If the view throws an error (such as the user can't be authenticated
            # or something similar), `data` will contain an `errors` key. We want
            # the default JSONRenderer to handle rendering errors, so we need to
            # check for this case.
            elif data.get("errors", None) is not None:
                return super().render(data, media_type, renderer_context)

        return json.dumps({self.object_label: data}, cls=ExtendedEncoder)


# This for retro-compatibility
ConduitJSONRenderer = ApiRenderer