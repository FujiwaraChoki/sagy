# Windows Intelligence

Windows Intelligence is a Python-based AI tool that is designed to be the Apple Intelligence missing in Windows-Systems. It's main purpose is to provide people the ability to improve their spelling.

## Installation

### Binaries

You can download the latest binaries from the [Releases](https://github.com/FujiwaraChoki/windows-intelligence/releases) page.


### Manual Installation

1. Clone

```bash
git clone git@github.com:FujiwaraChoki/windows-intelligence.git
cd windows-intelligence
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

This will launch the initial setup window, and then exit from the App. To start using Windows Intelligence, simply re-run the App.


## Building from Source

Once you installed all the dependencies, you can build the App using the following command:

```bash
pyinstaller --onefile --noconsole --add-data "assets:assets" --add-data "ui:ui" main.py
```

This will create a `dist` folder with the executable file.

## Usage

Windows Intelligence is a simple tool that runs in the background and listens to your keyboard inputs.

In order to first set it up, press `Ctrl + Space` to open the setup window.

After you're done configuring the settings, close the window, and re-open the file.

Now select some text and press `Ctrl + Space` again, to start using Windows Intelligence.

## Contributing

If you want to contribute to this project, feel free to fork it and submit a pull request.

Please make sure to follow common sense and coding standards.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
