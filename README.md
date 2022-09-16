# ols-standardization-analysis

Analysis of public OLS instances for conformity to Bioregistry standards.

## Reproduction

The analysis can be reproduced with the following commands in the shell:

```shell
git clone https://github.com/cthoyt/ols-standardization-analysis.git
cd ols-standardization-analysis
python -m pip install tox
tox
```

## Deploy

```shell
git clone https://github.com/cthoyt/ols-standardization-analysis.git
cd ols-standardization-analysis/docs
docker run --rm --volume="$PWD:/srv/jekyll" -p 4000:4000 -it jekyll/jekyll:latest jekyll serve
```
