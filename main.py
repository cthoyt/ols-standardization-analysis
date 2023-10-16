from operator import itemgetter
from pathlib import Path
from textwrap import dedent

import bioregistry
import click
import yaml
from ols_client import Client, TIBClient, client_resolver
from tqdm import tqdm

HERE = Path(__file__).parent.resolve()
DATA = HERE.joinpath("docs", "_data")
DATA.mkdir(exist_ok=True, parents=True)
PATH = DATA.joinpath("results.yml")


def main():
    results = []

    client_classes: list[tuple[type[Client, str, str | None]]] = [
        (client_cls, client_cls.__name__.removesuffix("Client"), None)
        for client_cls in sorted(client_resolver, key=lambda c: c.__name__)
        if client_cls is not TIBClient
    ]

    # Note that the TIB server is a fork of the base OLS and includes additional functionality
    # for having collections
    client_classes.extend(
        [
            (
                TIBClient,
                "NFDI4Cat",
                "ontologies/filterby?schema=collection&classification=NFDI4CAT&exclusive=false",
            ),
            (
                TIBClient,
                "NFDI4Chem",
                "ontologies/filterby?schema=collection&classification=NFDI4CHEM&exclusive=false",
            ),
        ]
    )

    for client_cls, name, part in client_classes:
        print("getting", name)
        client: Client = client_cls()
        standard = {}
        nonstandard = {}
        unregistered = {}
        try:
            if part is not None:
                records = list(client.get_paged(part, key="ontologies"))
            else:
                records = list(client.get_ontologies())
        except Exception as e:
            click.secho(f"Failed on {client_cls}\n{e}", fg="red")
            continue
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

        base_browse_url = client.base_url.removesuffix("/").removesuffix("/api")
        results.append(
            {
                "name": name,
                "nonstandard_percent": round(100 * nonstandard_percent, 1),
                "standard_percent": round(100 * standard_percent, 1),
                "unregistered_percent": round(100 * unregistered_percent, 1),
                "nonstandard": nonstandard,
                "unregistered": unregistered,
                "standard": standard,
                "total": n_records,
                "base_url": base_browse_url,
            }
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
        yaml.safe_dump(
            sorted(results, key=itemgetter("name")),
            indent=2,
            sort_keys=True,
            allow_unicode=True,
        )
    )


if __name__ == "__main__":
    main()
