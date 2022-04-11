rm src/reqJson/*
yq -o json . reqYml/cisIR20.yml | jq --indent 4 '' > src/reqJson/cisIR20.json
yq -o json . reqYml/cisID20.yml | jq --indent 4 '' > src/reqJson/cisID20.json
yq -o json . reqYml/coins19.yml | jq --indent 4 '' > src/reqJson/coins19.json
yq -o json . reqYml/coins20.yml | jq --indent 4 '' > src/reqJson/coins20.json
yq -o json . reqYml/coins21.yml | jq --indent 4 '' > src/reqJson/coins21.json
yq -o json . reqYml/mast20.yml | jq --indent 4 '' > src/reqJson/mast20.json
yq -o json . reqYml/math20.yml | jq --indent 4 '' > src/reqJson/math20.json
yq -o json . reqYml/psych20.yml | jq --indent 4 '' > src/reqJson/psych20.json

