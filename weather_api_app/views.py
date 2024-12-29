from django.shortcuts import render
from django.core.cache import cache
from django_ratelimit.decorators import ratelimit
from django.http import JsonResponse
from decouple import config
import json
import requests

api_key = config("API_KEY")

# Create your views here.
@ratelimit(key="ip", rate="100/m", method="GET", block=False)
def index(request):
    if getattr(request, "limited", False):
        return JsonResponse({"error": "Rate limit exceeded"}, status=429)
    if request.method == "POST":
        location = request.POST.get("location")
        
        if not cache.get(location):
            response = requests.request("GET", f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?unitGroup=us&key={api_key}&contentType=json")
            # check error in api
            if response.status_code!=200:
                error = f"Unexpected Status code: {response.status_code}"
                return render(request, "index.html", {"error": error})
            jsonData = response.json()
            cache.set(location, json.dumps(jsonData), timeout=60*15)
        cache_data = json.loads(cache.get(location))
        return render(request, "index.html", {"data": cache_data})
    return render(request, "index.html")