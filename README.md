# OLS Standardization Analysis

Analysis of public OLS instances for conformity to Bioregistry standards.

View the results of the analysis at https://cthoyt.github.io/ols-standardization-analysis.

## Reproduction

The analysis can be reproduced with the following commands in the shell:

```console
$ git clone https://github.com/cthoyt/ols-standardization-analysis.git
$ cd ols-standardization-analysis
$ uv run --script main.py
```

## Deploy

```console
$ git clone https://github.com/cthoyt/ols-standardization-analysis.git
$ cd ols-standardization-analysis/docs
$ docker run --rm --volume="$PWD:/srv/jekyll" -p 4000:4000 -it jekyll/jekyll:4.2.0 jekyll serve
```
