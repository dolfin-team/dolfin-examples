# Battery passport — showcase queries

Paste into the SPARQL tab of the public project.

## 1. Carbon footprint per kWh, best first

```sparql
PREFIX b: <https://www.dolfin.fr/showcase/battery-passport/battery#>
SELECT ?model ?maker ?chemistry ?kgCO2ePerKWh ?class WHERE {
  ?m a b:BatteryModel ; b:modelId ?model ; b:chemistry/b:code ?chemistry ;
     b:manufacturer/b:name ?maker ;
     b:carbonFootprint [ b:perKWh ?kgCO2ePerKWh ; b:performanceClass ?c ] .
  BIND(STRAFTER(STR(?c), "_") AS ?class)
} ORDER BY ?kgCO2ePerKWh
```

## 2. Which models already meet the 2031 recycled-content targets?

Targets (Art. 8): cobalt 16 %, lithium 6 %, nickel 6 %.

```sparql
PREFIX b: <https://www.dolfin.fr/showcase/battery-passport/battery#>
SELECT ?model ?material ?share ?target (IF(?share >= ?target, "yes", "no") AS ?meets2031) WHERE {
  VALUES (?mat ?target) { (b:CriticalMaterial_Cobalt 16.0) (b:CriticalMaterial_Lithium 6.0) (b:CriticalMaterial_Nickel 6.0) }
  ?m b:modelId ?model ; b:recycledContent [ b:material ?mat ; b:sharePercent ?share ] .
  BIND(STRAFTER(STR(?mat), "_") AS ?material)
} ORDER BY ?model ?material
```

## 3. Used EV batteries worth a second life (state of health 70–85 %)

```sparql
PREFIX b: <https://www.dolfin.fr/showcase/battery-passport/battery#>
SELECT ?passport ?model ?soh ?plant WHERE {
  ?bat a b:Battery ; b:passportId ?passport ; b:status b:BatteryStatus_Original ;
       b:stateOfHealthPercent ?soh ; b:plant/b:name ?plant ;
       b:model [ b:modelId ?model ; b:category b:BatteryCategory_ElectricVehicle ] .
  FILTER(?soh >= 70 && ?soh < 85)
} ORDER BY DESC(?soh)
```

## 4. Batteries per country of manufacture

```sparql
PREFIX b: <https://www.dolfin.fr/showcase/battery-passport/battery#>
SELECT ?country (COUNT(?bat) AS ?batteries) WHERE {
  ?bat a b:Battery ; b:plant/b:country/b:name ?country .
} GROUP BY ?country ORDER BY DESC(?batteries)
```
