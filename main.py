# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "bioregistry",
#     "click",
#     "ols-client",
#     "pyyaml",
#     "tabulate",
#     "tqdm",
# ]
# ///


from operator import itemgetter
from pathlib import Path

import bioregistry
import click
import yaml
from ols_client import Client, client_resolver
from tqdm import tqdm
from tabulate import tabulate

HERE = Path(__file__).parent.resolve()
DATA = HERE.joinpath("docs", "_data")
DATA.mkdir(exist_ok=True, parents=True)
PATH = DATA.joinpath("results.yml")


def main():
    results = []

    client_classes: list[tuple[type[Client, str, str | None]]] = [
        (client_cls, client_cls.__name__.removesuffix("Client"), None)
        for client_cls in sorted(client_resolver, key=lambda c: c.__name__)
    ]

    # Note that the TIB server is a fork of the base OLS and includes additional functionality
    # for having collections
    # client_classes.extend(
    #     [
    #         (
    #             TIBClient,
    #             "NFDI4Cat",
    #             "ontologies/filterby?schema=collection&classification=NFDI4CAT&exclusive=false",
    #         ),
    #         (
    #             TIBClient,
    #             "NFDI4Chem",
    #             "ontologies/filterby?schema=collection&classification=NFDI4CHEM&exclusive=false",
    #         ),
    #     ]
    # )

    for client_cls, name, part in client_classes:
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
                unregistered[prefix] = dict(title=title, standard=norm_prefix)
            elif norm_prefix == prefix:
                standard[prefix] = dict(title=title, standard=norm_prefix)
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
        tqdm.write(f"{click.style(name, fg='green')} ({base_browse_url})")
        tqdm.write(f"{'=' * (3 + len(name) + len(base_browse_url))}")
        if standard:
            tqdm.write(
                f"standard:     {len(standard)}/{n_records} ({standard_percent:.1%})"
            )
        if nonstandard:
            tqdm.write(
                f"\nnonstandard:  {len(nonstandard)}/{n_records} ({nonstandard_percent:.1%})"
            )
            rows = [
                (prefix, data["title"], f"{base_browse_url}/ontologies/{prefix})")
                for prefix, data in sorted(nonstandard.items())
            ]
            tqdm.write(tabulate(rows, headers=["prefix", "name", "url"]))
        if unregistered:
            tqdm.write(
                f"\nunregistered: {len(unregistered)}/{n_records} ({unregistered_percent:.1%})"
            )
            rows = [
                (x, data["title"], f"{base_browse_url}/ontologies/{x}")
                for x, data in sorted(unregistered.items())
            ]
            tqdm.write(tabulate(rows, headers=["prefix", "name", "url"]))

        tqdm.write("")

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
