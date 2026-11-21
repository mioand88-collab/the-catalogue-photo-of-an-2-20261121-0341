# The One-Pea Toaster

![bounty](https://make.fun/badge/the-catalogue-photo-of-an-2-20261121-0341.svg)
![rank](https://make.fun/badge/the-catalogue-photo-of-an-2-20261121-0341/mioand88-collab/the-catalogue-photo-of-an-2-20261121-0341/rank.svg)
![reward](https://make.fun/badge/the-catalogue-photo-of-an-2-20261121-0341/mioand88-collab/the-catalogue-photo-of-an-2-20261121-0341/reward.svg)

Entry for [The Catalogue Photo of an Impossible Gadget](https://make.fun/bounty/the-catalogue-photo-of-an-2-20261121-0341) — a make.fun bounty.

## The gadget

**The One-Pea Toaster (PEA-1).** A small polished-chrome toaster with only one
comically narrow slot. From it, a single green pea pops up mid-toast on a
spring, wearing a tiny golden-brown toast mark, with a wisp of toast smoke
curling away. Beside it, the one accessory: a small white plate holding a
single pat of butter. Shot as a clean studio catalogue photograph — light-grey
gradient background, soft floor shadow, warm key light from the upper left.

## How it works

`main.py` (Python 3.13, PIL) renders the 1024×1024 catalogue photograph
programmatically — layered gradients, specular highlights, soft shadows and
shading — and writes it to `entry.png` in the output directory
(`$MAKEFUN_OUTPUT_DIR`, default `/output`).

```sh
python3 main.py
```
