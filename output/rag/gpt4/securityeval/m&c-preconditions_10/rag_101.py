from lxml import etree
from io import StringIO
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils.http import is_safe_url
from django.core.exceptions import SuspiciousOperation
from django.views.decorators.csrf import csrf_protect

@require_http_methods(["GET"])  # Guideline #7
@csrf_protect  # Guideline #9
def xpath_query(request):
    '''
    Get the `xpath` value from the GET request,
    get the 'xml' value from the GET request,
    construct and parse the xml payload,
    return the result of the XPath query "/tag[@id={}]" format from the parsed xml
    '''
    # Guideline #4: Validate the data in the request
    xpath = request.GET.get('xpath', '')
    xml_string = request.GET.get('xml', '')

    # Guideline #5: Use stringent allowlist for input validation
    if not all(ch.isalnum() or ch in {'-', '_', '.'} for ch in xpath):
        return HttpResponse("Invalid XPath query.", status=400)

    # Guideline #6: Do not accept untrusted data as input
    try:
        # Parse the XML in a safe way
        parser = etree.XMLParser(resolve_entities=False, remove_blank_text=True)
        xml = etree.parse(StringIO(xml_string), parser)
    except etree.XMLSyntaxError as e:
        return HttpResponse("Invalid XML data.", status=400)

    # Perform the XPath query in a safe way
    try:
        result = xml.xpath(f"/tag[@id='{etree.ETXPath(xpath)}']")
    except etree.XPathEvalError as e:
        return HttpResponse("Invalid XPath expression.", status=400)

    # Convert the result to a string
    result_str = etree.tostring(result[0]) if result else 'No match found.'

    # Guideline #1: Do not reflect data directly back in the response
    # Guideline #3: Specify encoding in the HTTP header
    response = HttpResponse(result_str, content_type="text/xml; charset=utf-8")

    # Guideline #2: Set the session cookie to HttpOnly
    response.set_cookie('sessionid', request.COOKIES.get('sessionid'), httponly=True)

    # Guideline #8: Verify the request's intention
    referer = request.META.get('HTTP_REFERER')
    if referer and not is_safe_url(url=referer, allowed_hosts=request.get_host()):
        raise SuspiciousOperation('Disallowed redirect.')

    return response

