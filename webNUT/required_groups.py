from .settings import REQUIRED_GROUP
from django_python3_ldap.utils import format_search_filters

def custom_format_search_filters(ldap_fields):
    # Add in simple filters.
    if REQUIRED_GROUP is not None:
        ldap_fields["memberOf"] = REQUIRED_GROUP
     
    # Call the base format callable.
    search_filters = format_search_filters(ldap_fields)
    # Advanced: apply custom LDAP filter logic.
    #search_filters.append("(|(memberOf=xyz))")
    # All done!
    return search_filters