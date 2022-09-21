---
layout: home
title: OLS Standardization Analysis
---
This page summarize various OLS instances' prefixes'
conformance to the Bioregistry standard.

<table>
<thead>
<tr>
    <th>Instance</th>
    <th># Standard</th>
    <th>% Standard</th>
    <th># Non-standard</th>
    <th>% Non-standard</th>
    <th># Unknown</th>
    <th>% Unknown</th>
</tr>
</thead>
<tbody>
{% for record in site.data.results %}
<tr>
    <td><a href="{{ record.base_url }}">{{ record.name }}</a></td>
    <td>{{ record.standard | size }}</td>
    <td>{{ record.standard_percent }}</td>
    <td>{{ record.nonstandard | size }}</td>
    <td>{{ record.nonstandard_percent }}</td>
    <td>{{ record.unregistered | size }}</td>
    <td>{{ record.unregistered_percent }}</td>
</tr>
{% endfor %}
</tbody>
</table>

{% for record in site.data.results %}

## {{ record.name }}

{% if record.unregistered.size > 0 %}

### Unregistered

<ul>
{% for subrecord in record.unregistered %}
<li>
    <a href="{{ record.base_url }}/ontologies/{{ subrecord[0] }}"><code>{{ subrecord[0] }}</code></a>
    ({{ subrecord[1] }})
</li>
{% endfor %}
</ul>

{% endif %}

{% if record.nonstandard.size > 0 %}

### Non-standard

<ul>
{% for subrecord in record.nonstandard %}
<li>
    <a href="{{ record.base_url }}/ontologies/{{ subrecord[0] }}"><code>{{ subrecord[0] }}</code></a> ({{ subrecord[1].title }})
    could be standardized to <a href="https://bioregistry.io/{{ subrecord[1].standard }}"><code>{{ subrecord[1].standard }}</code></a>
</li>
{% endfor %}
</ul>
{% endif %}

{% endfor %}
