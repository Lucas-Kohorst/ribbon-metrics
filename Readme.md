# Theta Vault Metrics
- [ribbon.finance](https://ribbon.finance)
- [Twitter](https://twitter.com/ribbonfinance)
- [Discord](https://discord.com/invite/85gcVafPyN)
- [Metrics](https://github.com/Lucas-Kohorst/theta-vault-metrics)

### Overview
[ribbon.finance](https://ribbon.finance) provides sustainable alpha for everyone. The primary product is the [theta vault](https://app.ribbon.finance/theta-vault/T-100-E) which earns yield by selling far out of the money covered calls. 

You can find metrics for the vault at [metrics.thetagang.info](http://metrics.thetagang.info/d/hH2ap5XGz/theta-vault?orgId=1)

### Development 
The metrics are gathered from the [Ribbon Subgraph](https://thegraph.com/explorer/subgraph/kenchangh/ribbon-finance?query=Example%20query) and then scraped via a [graphql-exporter](https://github.com/ricardbejarano/graphql_exporter). ETH price feeds are also pulled in via [cryptowat-exporter](https://github.com/nbarrientos/cryptowat_exporter).

Everything is scraped via [prometheus](https://prometheus.io/) and displayed in [grafana](https://grafana.com/)