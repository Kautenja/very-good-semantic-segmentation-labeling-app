# Very Good Semantic Segmentation Labeling App

<!-- header badges -->

[![build-status][]][ci-server]

<!-- screen shot of the app -->

![screenshot][]

[build-status]: https://travis-ci.com/Kautenja/semantic-segmentation-labeling-app.svg?branch=master
[ci-server]: https://travis-ci.com/Kautenja/semantic-segmentation-labeling-app
[screenshot]: https://user-images.githubusercontent.com/2184469/48687452-19c12200-eb87-11e8-94f7-cdae0e961e1d.png

## Installation

### MacOS

To install Python3 with TKinter support:

```shell
xcode-select --install
brew install tcl-tk
```

If you _dont_ have Python3 installed already:

```shell
brew install python3 --with-tcl-tk
```

If you _do_ have Python3 installe already:

```shell
brew reinstall python3 --with-tcl-tk
```

### Debian

To install TKinter support for Python3:

```shell
sudo apt-get install python3-tk
```

## Required Python Modules

To install required Python modules:

```shell
python3 -m pip install -r requirements.txt
```

## Usage

To launch the application:

```shell
python3 . --help
```

### Dummy Example

To launch the application with the dummy example:

```shell
python3 . -i dummy/x_1541528173117841344.png -s dummy/y_1541528173117841344.png -m dummy/metadata.csv
```

## Keyboard Controls

| Keyboard Keys | Description
|:--------------|:-----------------------
| `0` ... `9`   | Set the opacity of the semantic segmentation overlay
| `S`           | Save the image
| `ESC`         | Save the image and close the application

## Mouse Controls

| Mouse Button | Action             |
|:-------------|:-------------------|
| `Left`       | Paint              |
| `Right`      | Drag               |
| `Middle`     | Reset Zoom         |
| `Scroll`     | Zoom in / Zoom out |
