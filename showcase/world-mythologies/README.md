# World Mythologies

Greek, Norse, Hindu, Japanese (Shinto) and Maya figures on one shared model. Gods, heroes, realms and weapons from different traditions can be queried side by side. Several of these are living traditions, so entries are descriptive.

## What's inside

- **`Tradition`**: a mythology, with its region and written sources (Theogony, Prose Edda, Puranas, Kojiki, Popol Vuh).
- **`Figure`**: anyone in a myth. `Deity`, `Hero` and `Creature` are kinds of `Figure`.
- **`Domain`**: a fixed list of what a figure rules over, such as `Death`, `Sky` or `Craft`. A figure can have several.
- **`Realm`**: a place such as Mount Olympus.
- **`Artifact`**: a legendary item and the figure who wields it.
- **Relations**: `parentOf`, `spouseOf`, `avatarOf`, `dwellsIn`.
- **Rules**: `parent_is_ancestor` and `ancestor_chain` derive `ancestorOf` from `parentOf`.

## Try it

- Run `death_figures` to list death deities across all traditions.
- Run `gaia_descendants` to get every descendant of Gaia, at any depth, using the derived `ancestorOf`.
- Run `domains_by_tradition_count` to see which domains show up in the most traditions.
- Run `artifacts_and_wielders` to list legendary weapons and who holds them.

## Learn more

- `one of:` enumerations (`Domain`)
- Rules that build a transitive closure (`ancestor_chain`)
- `group by` with `count distinct` in a query
