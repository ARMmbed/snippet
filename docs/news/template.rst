{# This is a custom template for towncrier md #}

{% for section in sections %}
{% set underline = underlines[0] %}
{% if section %}
## {{section}}

{% endif %}
{% if sections[section] %}
{% for category, val in definitions.items() if category in sections[section] %}
### {{ definitions[category]['name'] }}

{% if definitions[category]['showcontent'] %}
{% for text, values in sections[section][category]|dictsort(by='value') %}
- {{ text }} ({{ values|sort|join(', ') }})

{% endfor %}
{% else %}
- {{ sections[section][category]['']|sort|join(', ') }}

{% endif %}
{% if sections[section][category]|length == 0 %}

No significant changes.

{% else %}
{% endif %}
{% endfor %}
{% else %}

No significant changes.

{% endif %}
{% endfor %}
