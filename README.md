# Bayer to RGB Conversion

This project provides a Python implementation for converting Bayer pattern images to RGB images. The main function `bayer_to_rgb` supports various Bayer patterns (RGGB, BGGR, GRBG, GBRG) and offers an option for interpolation to upscale the image or decimation for downsampling. This is typically useful in image processing and computational photography where Bayer sensors are used.

## Features

-   Support for Bayer patterns:
    -   `RGGB` (Red, Green, Green, Blue)
    -   `BGGR` (Blue, Green, Green, Red)
    -   `GRBG` (Green, Red, Blue, Green)
    -   `GBRG` (Green, Blue, Red, Green)
-   Interpolation for upscaling or decimation for downsampling
-   Efficient handling of Bayer data using NumPy
-   Flexible input and output for integration with other projects

## Installation

To get started with this project, make sure you have Python 3.x installed. Then, install the required dependencies using `pip`:

`pip install numpy`

## Dependencies

-   `numpy`: A package for numerical operations and handling of arrays.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

This project was inspired by common image processing techniques for converting Bayer pattern images into full-color images using either decimation or interpolation methods. These techniques are widely used in image sensors, photography, and computational imaging.

## Author

Zdravko Brdarovski
