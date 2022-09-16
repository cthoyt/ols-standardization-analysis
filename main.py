from pathlib import Path
from textwrap import dedent

import bioregistry
import yaml
from ols_client import Client, client_resolver
from tqdm import tqdm

HERE = Path(__file__).parent.resolve()
DATA = HERE.joinpath("_data")
DATA.mkdir(exist_ok=True, parents=True)
PATH = DATA.joinpath("results.yml")


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
                nonstandard[prefix] = dict(title=title, standard=norm_prefix)

        standard_percent = len(standard) / n_records
        nonstandard_percent = len(nonstandard) / n_records
        unregistered_percent = len(unregistered) / n_records

        name = client_cls.__name__.removesuffix("Client")
        base_browse_url = client.base_url.removesuffix("/").removesuffix("/api")
        results[name] = {
            "nonstandard_percent": round(100 * nonstandard_percent, 1),
            "standard_percent": round(100 * standard_percent, 1),
            "unregistered_percent": round(100 * unregistered_percent, 1),
            "nonstandard": nonstandard,
            "unregistered": unregistered,
            "total": n_records,
            "base_url": base_browse_url,
        }
        rows.append(
            (client_cls.__name__, len(standard), len(nonstandard), len(unregistered))
        )
        tqdm.write(
            dedent(
                f"""\
        {name} ({base_browse_url})
        {"=" * (3 + len(name) + len(base_browse_url))}
        standard:     {len(standard)}/{n_records} ({standard_percent:.1%})
        nonstandard:  {len(nonstandard)}/{n_records} ({nonstandard_percent:.1%})
            {", ".join(sorted(nonstandard))}
        unregistered: {len(unregistered)}/{n_records} ({unregistered_percent:.1%})
            {", ".join(sorted(unregistered))}
        """
            )
        )

    PATH.write_text(
        yaml.safe_dump(results, indent=2, sort_keys=True, allow_unicode=True)
    )


if __name__ == "__main__":
    main()
