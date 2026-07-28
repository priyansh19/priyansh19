# Portfolio v3 — Development Branch

This branch (`claude/portfolio-v3-dev-098gsa`) is the isolated workspace for building
**v3** of the portfolio. All existing code was carried over from `master` intact.

## Deployment freeze (do not deploy until v1 of v3 is ready)

The live portfolio is the GitHub **profile README** served from the **`master`** branch:

- `README.md` (on `master`) — embeds `dark_mode.svg` / `light_mode.svg`
- `generate.py` — refreshes the stats inside those SVGs
- `.github/workflows/build.yml` — the deployment: a daily cron (`0 4 * * *`) that
  regenerates stats and auto-pushes to `master`

**Rule:** none of the deployment surface above is to be changed on `master` until the
first working version (v1) of the new v3 portfolio is ready. All v3 work stays on this
branch. Scheduled workflows only run on the default branch, so building here does **not**
trigger any auto-deploy — the live profile is unaffected.

## Status

- [x] All current code shifted onto the v3 dev branch
- [x] Deployment surface on `master` left untouched
- [ ] v3 build (stack + design TBD)
- [ ] v3 v1 ready → then wire up deployment
