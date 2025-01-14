# Sagy

Sagy is a Python-based AI tool that is designed to be the Apple Intelligence missing in Windows-Systems. It's main purpose is to provide people the ability to improve their spelling.

## Installation

### Binaries

You can download the latest binaries from the [Releases](https://github.com/FujiwaraChoki/sagy/releases) page.


### Manual Installation

1. Clone

```bash
git clone git@github.com:FujiwaraChoki:sagy.git
cd sagy
```

2. Install dependencies

```bash
uv venv venv
source venv/Scripts/activate
uv pip install -r requirements.txt
```

3. Run

```bash
uv run main.py
```

This will launch the initial setup window, and then exit from the App. To start using Sagy, simply re-run the App.


## Building from Source

Once you installed all the dependencies, you can build the App using the following command:

```bash
chmod +x bin/build.sh
./bin/build.sh
```

Alternatively, just execute the commands in `bin/build.sh` manually (if you don't have git bash installed).
