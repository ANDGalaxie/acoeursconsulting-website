from django import template

register = template.Library()


class CaptureNode(template.Node):
    def __init__(self, nodelist, name):
        self.nodelist = nodelist
        self.name = name

    def render(self, context):
        context[self.name] = self.nodelist.render(context).strip()
        return ""


@register.tag
def capture(parser, token):
    """Render inherited metadata blocks once for both HTML and Open Graph."""
    bits = token.split_contents()
    if len(bits) != 2 or not bits[1].isidentifier():
        raise template.TemplateSyntaxError("capture requires one variable name")
    nodelist = parser.parse(("endcapture",))
    parser.delete_first_token()
    return CaptureNode(nodelist, bits[1])
