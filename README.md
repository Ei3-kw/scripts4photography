# scripts4photography
 
## PRE REQ
- install `wand` python binding (https://docs.wand-py.org/en/latest/index.html)
- Environment set up
	- `export MAGICK_HOME=/opt/homebrew/opt/imagemagick`
	- `export PATH=$MAGICK_HOME/bin:$PATH`

## USER MANUAL

### `startrace.py`
- 1: lighten blend
	- 1: generate all images for timelapse
	- else: stack into one img
- 2: foreground & background stack
	- provide a mask - fg black, bg white (NO GREY AREA)
	- select foregrounds
	- select backgrounds

### `panorama.py`
- 1: split panaroma
	- (optional) merge the split imgs vertically
- 2: merge vertically
- 3: split n photos into n parts and glue horizontally
	- 1: cyclicly
	- else: derangedly

