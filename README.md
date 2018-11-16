# Very Good Semantic Segmentation Labeling App

![screenshot](https://user-images.githubusercontent.com/2184469/48598236-89d16d00-e927-11e8-880a-44986a732b90.png)

## Installation

To install required modules:

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
| `0`, ..., `9` | Set the opacity of the semantic segmentation overlay
| `S`           | Save the image
| `ESC`         | Save the image and close the application
