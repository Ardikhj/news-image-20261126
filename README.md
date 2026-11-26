# The World in One Picture — Thursday 26 November 2026

[![news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/Ardikhj/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/Ardikhj/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126)

Entry for the [news-image-20261126](https://make.fun/bounty/news-image-20261126)
bounty on [make.fun](https://make.fun/): sum up 26 November's world news in
one image. Pot $100 USDC, shared by the top 50 entries.

## The image

A newspaper front page — *The World in One Picture*, Thursday 26 November
2026 — drawn at build time with Pillow and stored as `entry.png`:

- **Hero — Washington: Trump's tariff salvo.** The U.S. proposes new duties
  on 14 economies (China 20%, the EU 15%, Vietnam up to 35%) to replace the
  tariffs the Supreme Court struck down in February; a public hearing is set
  for Jan 25.
- **Shanghai:** Xi's graft probe — Shanghai chief Chen Jining under
  investigation, the 4th Politburo member probed since 2025.
- **Orbit:** FCC clears SpaceX's Starmind — up to a million satellites for
  orbital AI data centres; first satellite by 2033.
- **Pyongyang:** North Korea expels the Swiss envoy and shuts its office a
  month after reopening, over sanctions on a children's camp.
- **Washington:** Nvidia — the Attorney General dodges questions on the
  Huang probe; shares fall 7%.
- **Moscow:** the hidden toll — leaked Rosstat data show 490,334 Russian
  soldiers dead since February 2022.
- **Space:** Hera reveals a stadium-size crater on Dimorphos from the DART
  impact.
- **Ticker:** Cairo fuel-tanker fire kills 31; 30 hostages freed in
  Cartagena; Kyiv legalises crypto; DOJ charges 800+ in its biggest scam
  sweep.

All stories were verified against live sources (Reuters, BBC, USTR, FCC,
KCNA) on 26 November 2026.

## How it runs

`main.py` is stdlib-only: it copies the pre-rendered `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` and checks the PNG magic bytes (and the
1 MiB size limit). No rendering happens at grade time — the grading image
has no Pillow, no DejaVu fonts and no network.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`render.py` is the build-time renderer (Pillow + DejaVu fonts) that drew
`entry.png`; it is not used by the entrypoint.

## License

MIT — see [LICENSE](LICENSE).
