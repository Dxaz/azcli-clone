from azure.core.pipeline.policies import (RequestIdPolicy,
                                          HeadersPolicy,
                                          UserAgentPolicy,
                                          ProxyPolicy,
                                          ContentDecodePolicy,
                                          RedirectPolicy,
                                          RetryPolicy,
                                          CustomHookPolicy,
                                          NetworkTraceLoggingPolicy,
                                          DistributedTracingPolicy,
                                          HttpLoggingPolicy)
from azure.mgmt.core.policies import ARMAutoResourceProviderRegistrationPolicy, ARMChallengeAuthenticationPolicy, ARMHttpLoggingPolicy
from .constants import CACHED_CREDENTIAL

# RequestIdPolicy(**kwargs),
# headers_policy=HeadersPolicy(**kwargs),
# user_agent_policy=UserAgentPolicy(**kwargs),
# proxy_policy=ProxyPolicy(**kwargs),
# ContentDecodePolicy(**kwargs),
# ARMAutoResourceProviderRegistrationPolicy(),
# redirect_policy=RedirectPolicy(**kwargs),
# retry_policy=RetryPolicy(**kwargs),
# authentication_policy=ARMChallengeAuthenticationPolicy(self.credential, *self.credential_scopes, **kwargs),
# custom_hook_policy=CustomHookPolicy(**kwargs),
# logging_policy=NetworkTraceLoggingPolicy(**kwargs),
# DistributedTracingPolicy(**kwargs),
# http_logging_policy=ARMHttpLoggingPolicy(**kwargs),

class UnredactedHttpLoggingPolicy(ARMHttpLoggingPolicy, HttpLoggingPolicy):

    def _redact_header(self, key: str, value: str) -> str:
        return value
    
    def _redact_query_param(self, key: str, value: str) -> str:
        return value
    

    # def _redact_header(self, key: str, value: str) -> str:
    #     lower_case_allowed_header_names = [header.lower() for header in self.allowed_header_names]
    #     return value if key.lower() in lower_case_allowed_header_names else value
    
    # def _redact_query_param(self, key: str, value: str) -> str:
    #     lower_case_allowed_query_params = [param.lower() for param in self.allowed_query_params]
    #     return value if key.lower() in lower_case_allowed_query_params else value


CUSTOM_POLICIES= [
    RequestIdPolicy(),
    HeadersPolicy(),
    UserAgentPolicy(),
    ProxyPolicy(),
    ContentDecodePolicy(),
    ARMAutoResourceProviderRegistrationPolicy(),
    RedirectPolicy(),
    RetryPolicy(),
    ARMChallengeAuthenticationPolicy(CACHED_CREDENTIAL, "https://management.azure.com/.default"),
    CustomHookPolicy(),
    NetworkTraceLoggingPolicy(),
    DistributedTracingPolicy(),
    UnredactedHttpLoggingPolicy(),
]
