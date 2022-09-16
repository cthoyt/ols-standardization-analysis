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
