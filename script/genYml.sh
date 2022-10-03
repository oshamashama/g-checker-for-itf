rm reqYml/*
yq -y .  src/reqJson/cisIR20.json > reqYml/cisIR20.yml
yq -y .  src/reqJson/cisID20.json > reqYml/cisID20.yml
yq -y .  src/reqJson/coins19.json > reqYml/coins19.yml
yq -y .  src/reqJson/coins20.json > reqYml/coins20.yml
yq -y .  src/reqJson/coins21.json > reqYml/coins21.yml
yq -y .  src/reqJson/mast20.json > reqYml/mast20.yml
yq -y .  src/reqJson/math20.json > reqYml/math20.yml
yq -y .  src/reqJson/psych20.json > reqYml/psych20.yml

