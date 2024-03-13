from rest_framework.throttling import SimpleRateThrottle
from rest_framework.settings import api_settings
from . import models
import datetime
from rest_framework.request import Request
from .utils import get_api_key


class APIKeyThrottle(SimpleRateThrottle):
    """
    Throttle class to limit API requests based on API keys.
    This class can be subclassed to add custom logic.

    Attributes:
        API_KEY_HEADER (str): The HTTP header used to pass the API key. Obtained from api_settings, if not found, defaults to X_API_KEY
        API_KEY_IN_QUERY_PARAMS (bool): Flag to indicate if the key can also be passed in query params. Defaults to False as from a security pov, adjust at your own risk.
        scope_long (str): The rate of requests allowed per month. Scope_long should correspond to a key present in api_settings.THROTTLE_RATES
        model: The Django model class used for querying the API key. Update if you are using a subclassed model
    """
    API_KEY_HEADER = getattr(api_settings, 'API_KEY_HEADER', "X_API_KEY")
    API_KEY_IN_QUERY_PARAMS = False
    scope = None    # Subclasses should either override this attribute with a key that is present in SimpleRateThrottle.THROTTLE_RATES or instead set rate to True, see superclass for more info
    scope_long = None   # Subclasses should override this attribute if you plan on implementing monthly rate limits, key here should be in SimpleRateThrottle.THROTTLE_RATES
    model = models.APIKey   

    if scope_long and not (model and hasattr(model, "key")):
        raise NotImplementedError("API_KEY model must have a 'key' attribute.")
    
    def get_cache_key(self, request: Request, view):
        """
        Retrieve the cache key for the request.

        Args:
            request: The incoming HTTP request.
            view: The Django view being accessed.

        Returns:
            str: A unique cache key for the request.
        """
        return self.cache_format % {
            'scope': self.scope,
            'ident': get_api_key(request=request, api_key_header=self.API_KEY_HEADER, key_in_query_params=self.API_KEY_IN_QUERY_PARAMS)
        }
    
    def allow_request(self, request: Request, view) -> bool:
        """
        Determine if the request should be allowed based on throttle limits.
        """
        if not super().allow_request(request, view):
            return False

        if self.scope_long:
            key = get_api_key(request=request, api_key_header=self.API_KEY_HEADER, key_in_query_params=self.API_KEY_IN_QUERY_PARAMS)
            filter_kwargs = {'created_at__gte': datetime.datetime.now() - datetime.timedelta(days=30)}  # Users may decide to subclass this and implement custom days (i.e December has 31 days)
            key_obj = self.model.objects.filter(key=key).first()
            if key_obj and key_obj.requests.filter(**filter_kwargs).count() >= self.get_scope_long_rate(request):
                return False
            models.Request.objects.create(api_key=key_obj)      # Adds a request

        return True
    
    def get_scope_long_rate(self, request: Request) -> int:
        """
        Retrieve the request rate limit for a long scope.

        Args:
            request: The incoming HTTP request.

        Returns:
            int: The number of requests allowed per month.

        Raises:
            NotImplementedError: If self.scope_long is not present in self.THROTTLE_RATES
            ValueError: If 'scope_long' is not an integer.
        """
        if self.scope_long:
            if not getattr(self.THROTTLE_RATES, self.scope_long, None):
                raise NotImplementedError(f"{self.scope_long} was not found in self.THROTTLE_RATES")
            
            try:
                return int(self.THROTTLE_RATES.get(self.scope_long))
            except ValueError:
                raise ValueError("scope_long must be an integer that corresponds to number of requests allowed a month.")
