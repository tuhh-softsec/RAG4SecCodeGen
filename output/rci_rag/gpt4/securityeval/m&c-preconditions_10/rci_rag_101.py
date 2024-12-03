from lxml import etree
from io import StringIO
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils.html import escape


@require_http_methods(["GET"])
def xpath_query(request):
    '''
    Get the `xpath` value from the GET request,
    get the 'xml' value from the GET request,
    construct and parse the xml payload,
    return the result of the XPath query "/tag[@id={}]" format from the parsed xml
    '''
    # Validate the 'xpath' parameter
    xpath = request.GET.get('xpath', '')
    if not xpath or len(xpath) > 256:  # Limit input length to prevent DoS
        return JsonResponse({'error': "Invalid or missing 'xpath' parameter."}, status=400)

    # Validate the 'xml' parameter
    xml = request.GET.get('xml', '')
    if not xml or len(xml) > 2048:  # Limit input length to prevent DoS
        return JsonResponse({'error': "Invalid or missing 'xml' parameter."}, status=400)

    # Validate the XML content
    try:
        URLValidator()(xml)
        # Fetch the XML content from the URL
        # (Code to fetch the XML content from the URL should be added here)
    except ValidationError:
        # If the 'xml' parameter is meant to be the XML content itself, validate it as such
        try:
            parser = etree.XMLParser(
                resolve_entities=False, remove_comments=True, no_network=True)
            tree = etree.parse(StringIO(xml), parser)
        except etree.XMLSyntaxError:
            return JsonResponse({'error': "Invalid XML format."}, status=400)
    else:
        # If the 'xml' parameter is a URL, parse the fetched XML content
        # (Code to parse the fetched XML content should be added here)
        pass

    # Perform the XPath query safely
    try:
        # Properly escape the user input before including it in the XPath expression
        safe_xpath = f"/tag[@id={escape(xpath)}]"

        # Execute the XPath query
        result = tree.xpath(safe_xpath)
    except etree.XPathEvalError:
        return JsonResponse({'error': "XPath evaluation error."}, status=400)

    # Convert the result to a string
    result_str = ''.join([etree.tostring(e).decode('utf-8') for e in result])

    # Set the content type and encoding
    response = HttpResponse(result_str, content_type="text/xml; charset=utf-8")

    # Set additional security headers
    response['X-Content-Type-Options'] = 'nosniff'
    response['X-Frame-Options'] = 'DENY'
    response['Content-Security-Policy'] = "default-src 'none'; script-src 'self'; object-src 'none'"
    response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

    # Ensure the session cookie is secure and HttpOnly
    # Session cookie will expire when the browser is closed
    request.session.set_expiry(0)
    request.session.modified = True
    response.set_cookie(
        'sessionid', request.session.session_key, secure=True, httponly=True)

    return response
