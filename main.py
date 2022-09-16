import json
from textwrap import dedent

import pystow
from ols_client import Client, client_resolver
from tqdm import tqdm

import bioregistry

PATH = pystow.join("bioregistry", name="ols_experiment.json")


def main():
    results = {}
    rows = []
    for client_cls in sorted(client_resolver, key=lambda c: c.__name__):
        client: Client = client_cls()
        standard = {}
        nonstandard = {}
        unregistered = {}
        records = list(client.get_ontologies())
        n_records = len(records)
        for record in records:
            prefix = record["ontologyId"]
            title = record["config"]["title"]
            norm_prefix = bioregistry.normalize_prefix(prefix)
            if norm_prefix is None:
                unregistered[prefix] = title
            elif norm_prefix == prefix:
                standard[prefix] = title
            else:
                nonstandard[prefix] = title

        results[client_cls.__name__] = {
            "nonstandard": sorted(nonstandard),
            "unregistered": sorted(unregistered),
        }
        rows.append((client_cls.__name__, len(standard), len(nonstandard), len(unregistered)))
        tqdm.write(
            dedent(
                f"""\
        {client_cls.__name__} ({client.base_url})
        {"=" * len(client_cls.__name__)}
        standard:     {len(standard)}/{n_records} ({len(standard) / n_records:.1%})
        nonstandard:  {len(nonstandard)}/{n_records} ({len(nonstandard) / n_records:.1%})
            {", ".join(sorted(nonstandard))}
        unregistered: {len(unregistered)}/{n_records} ({len(unregistered) / n_records:.1%})
            {", ".join(sorted(unregistered))}
        """
            )
        )
    PATH.write_text(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
