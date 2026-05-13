---
name: fedora-releases
description: Use when asked to get the current Fedora releases
---

# Getting current Fedora releases

Run command:

```bash
curl -L https://fedoraproject.org/releases.json | jq -r '.[].version' | sort -r | uniq
```

# References

- https://docs.fedoraproject.org/en-US/releases/#_current_supported_releases
