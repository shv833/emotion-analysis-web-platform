from django_hosts import patterns, host


host_patterns = patterns(
    "",
    host(r"^(|.*api.*)$", "backend.urls.api", name="api"),
    host(r".*admin.*", "backend.urls.admin", name="admin"),
)
