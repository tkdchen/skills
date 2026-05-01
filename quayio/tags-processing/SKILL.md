---
name: tags-processing
description: Used when asking to operate image tags via Quay.io API, e.g. list tags from a specific image repository.
---

# Quay.io Tag Operations

Use `curl` to query Quay.io tag API. Process responses with `jq` if needed.

## API Endpoint

**GET** `/api/v1/repository/{repository}/tag/`

- `{repository}`: Repository path without `quay.io/` prefix
  - Example: `quay.io/konflux-ci/buildah` → `konflux-ci/buildah`

## Query Parameters (all optional)

- `onlyActiveTags=true`: Filter to active tags only
- `filter_tag_name=<op>:<pattern>`: Filter by name (`like` for SQL LIKE, `eq` for exact match)
- `specificTag=<name>`: Get specific tag details

## Examples

```bash
# All tags
curl https://quay.io/api/v1/repository/konflux-ci/buildah/tag/

# Active tags only
curl "https://quay.io/api/v1/repository/konflux-ci/buildah/tag/?onlyActiveTags=true"

# Active tags starting with "v1"
curl "https://quay.io/api/v1/repository/konflux-ci/buildah/tag/?onlyActiveTags=true&filter_tag_name=like:v1%"
```

**Ref**: https://docs.redhat.com/en/documentation/red_hat_quay/3.14/html/red_hat_quay_api_reference/tag#listrepotags
