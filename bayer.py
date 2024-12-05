import numpy as np

def bayer_to_rgb(image_bayer, pattern, interpolation=False):
    # RGGB pattern implementation
    if pattern == 'RGGB':
        # If interpolation is not required, perform decimation (downsampling)
        if not interpolation:
            return decimation_rggb(image_bayer)
        # If interpolation is required, perform interpolation (upscaling)
        if interpolation:
            return interpolation_rggb(image_bayer)

    # BGGR pattern implementation
    if pattern == 'BGGR':
        # If interpolation is not required
        if not interpolation:
            # Flip the Bayer image horizontally (left-right flip)
            img = np.fliplr(image_bayer)
            # Flip the image vertically (up-down flip)
            i = np.flipud(img)
            # Apply decimation on the flipped image
            result = decimation_rggb(i)
            # Flip the result vertically to restore original orientation
            r = np.flipud(result)
            # Flip it back horizontally to restore the original orientation
            return np.fliplr(r)
        # If interpolation is required
        if interpolation:
            # Flip the Bayer image horizontally
            img = np.fliplr(image_bayer)
            # Flip the image vertically
            i = np.flipud(img)
            # Apply interpolation on the flipped image
            result = interpolation_rggb(i)
            # Flip the result vertically and then horizontally to restore the original orientation
            r = np.flipud(result)
            return np.fliplr(r)

    # GRBG pattern implementation
    if pattern == 'GRBG':
        # If interpolation is not required
        if not interpolation:
            # Flip the Bayer image horizontally
            img = np.fliplr(image_bayer)
            # Apply decimation on the flipped image
            result = decimation_rggb(img)
            # Flip the result horizontally to restore the original orientation
            return np.fliplr(result)
        # If interpolation is required
        if interpolation:
            # Flip the Bayer image horizontally
            img = np.fliplr(image_bayer)
            # Apply interpolation on the flipped image
            result = interpolation_rggb(img)
            # Flip the result horizontally to restore the original orientation
            return np.fliplr(result)

    # GBRG pattern implementation
    if pattern == 'GBRG':
        # If interpolation is not required
        if not interpolation:
            # Flip the Bayer image vertically
            img = np.flipud(image_bayer)
            # Apply decimation on the flipped image
            result = decimation_rggb(img)
            # Flip the result vertically to restore the original orientation
            return np.flipud(result)
        # If interpolation is required
        if interpolation:
            # Flip the Bayer image vertically
            img = np.flipud(image_bayer)
            # Apply interpolation on the flipped image
            result = interpolation_rggb(img)
            # Flip the result vertically to restore the original orientation
            return np.flipud(result)

def decimation_rggb(image_bayer):
    # Get the half dimensions of the image
    x = int((image_bayer.shape[0]) / 2)  # Half of the height
    y = int((image_bayer.shape[1]) / 2)  # Half of the width

    # Create an empty array with half the dimensions of the input image, and 3 channels for RGB
    result = np.zeros((x, y) + (3,))

    # Extract the red channel from every alternate pixel starting from (0, 0)
    result[::, ::, 0] = image_bayer[::2, ::2]

    # Extract the green channel from alternating pixels in a checkerboard pattern
    g01 = image_bayer[::2, 1::2]  # Green channel for even rows, odd columns
    g10 = image_bayer[1::2, ::2]  # Green channel for odd rows, even columns

    # Average the two green channels to get the final green channel
    result[::, ::, 1] = (1. * g01 + 1. * g10) / 2

    # Extract the blue channel from every alternate pixel starting from (1, 1)
    result[::, ::, 2] = image_bayer[1::2, 1::2]

    # Return the final image as an unsigned 8-bit integer array
    return np.uint8(result)

def interpolation_rggb(image_bayer):
    # Create an empty result array with an additional channel for RGB values
    result = np.zeros(image_bayer.shape + (3,))

    # Interpolate values for the first pixel (top-left corner)
    # r00 (Red)
    result[0, 0, 0] = image_bayer[0, 0]

    # g01 (Green - first row, second column)
    g01 = image_bayer[0, 1]
    # g10 (Green - second row, first column)
    g10 = image_bayer[1, 0]
    
    # Average the two green values (g01 and g10) to get the green channel for the top-left pixel
    result[0, 0, 1] = (1. * g01 + 1. * g10) / 2

    # b11 (Blue - second row, second column)
    result[0, 0, 2] = image_bayer[1, 1]

    # Interpolation for Green channel (g01) along the first row
    # r00 (Red - first row, odd columns)
    r00 = image_bayer[0, :-2:2]
    # r02 (Red - first row, even columns)
    r02 = image_bayer[0, 2::2]

    # Average red values (r00 and r02) for green channel
    result[0, 1:-1:2, 0] = (1. * r00 + 1. * r02) / 2

    # g01 (Green - first row, odd columns)
    result[0, 1::2, 1] = image_bayer[0, 1::2]

    # b11 (Blue - second row, odd columns)
    result[0, 1::2, 2] = image_bayer[1, 1::2]

    # Interpolation for Red and Green channels in the second row
    # r02 (Red - first row, even columns)
    result[0, 2:-1:2, 0] = image_bayer[0, 2:-1:2]

    # g01 (Green - first row, odd columns) and g03 (Green - first row, even columns after the third)
    g01 = image_bayer[0, 1:-1:2]
    g03 = image_bayer[0, 3::2]
    # g12 (Green - second row, even columns after the second)
    g12 = image_bayer[1, 2::2]

    # Average three green values (g01, g03, and g12) for the second row
    result[0, 2::2, 1] = (1. * g01 + 1. * g03 + 1. * g12) / 3

    # b11 (Blue - second row, odd columns) and b13 (Blue - second row, even columns after the third)
    b11 = image_bayer[1, 1:-1:2]
    b13 = image_bayer[1, 3::2]

    # Average blue values (b11 and b13) for the second row
    result[0, 2:-1:2, 2] = (1. * b11 + 1. * b13) / 2

    # Interpolation for last pixel in the row (g03)
    result[0, -1, 0] = image_bayer[0, -2]
    result[0, -1, 1] = image_bayer[0, -1]
    result[0, -1, 2] = image_bayer[1, -1]

    # Interpolation for the first column (g10)
    # r00 (Red - odd rows, first column)
    r00 = image_bayer[:-2:2, 0]
    # r20 (Red - even rows, first column)
    r20 = image_bayer[2::2, 0]

    # Average red values (r00 and r20) for the first column
    result[1:-1:2, 0, 0] = (1. * r00 + 1. * r20) / 2

    # g10 (Green - odd rows, first column)
    result[1::2, 0, 1] = image_bayer[1::2, 0]

    # b11 (Blue - odd rows, first column) 
    result[1::2, 0, 2] = image_bayer[1::2, 1]

    # Interpolation for the blue channel (b11)
    # r00, r02, r20, and r22 are the red channel values from the neighboring pixels
    r00 = image_bayer[:-2:2, :-2:2]
    r02 = image_bayer[:-2:2, 2::2]
    r20 = image_bayer[2::2, :-2:2]
    r22 = image_bayer[2::2, 2::2]

    # Average the red values from the surrounding pixels to compute the blue channel for the middle block
    result[1:-1:2, 1:-1:2, 0] = (1. * r00 + 1. * r02 + 1. * r20 + 1. * r22) / 4

    # g01, g10, g12, and g21 are the green channel values from the neighboring pixels
    g01 = image_bayer[:-2:2, 1:-1:2]
    g10 = image_bayer[1:-1:2, :-2:2]
    g12 = image_bayer[1:-1:2, 2::2]
    g21 = image_bayer[2::2, 1:-1:2]

    # Average the green values from the surrounding pixels for the middle block
    result[1:-1:2, 1:-1:2, 1] = (1. * g01 + 1. * g10 + 1. * g12 + 1. * g21) / 4

    # Assign the existing green values from the Bayer pattern to the result
    result[1::2, 1::2, 2] = image_bayer[1::2, 1::2]

    # Interpolation for the green channel (g12)
    # r02 and r22 are the red channel values from the neighboring pixels
    r02 = image_bayer[:-2:2, 2:-1:2]
    r22 = image_bayer[2::2, 2:-1:2]

    # Average the red values from the neighboring pixels for the green channel
    result[1:-1:2, 2:-1:2, 0] = (1. * r02 + 1. * r22) / 2

    # Assign the existing green values from the Bayer pattern to the result
    result[1::2, 2:-1:2, 1] = image_bayer[1::2, 2:-1:2]

    # b11 and b13 are the blue channel values from the Bayer pattern
    b11 = image_bayer[1::2, 1:-1:2]
    b13 = image_bayer[1::2, 3::2]

    # Average the blue values (b11 and b13) for the green channel
    result[1::2, 2:-1:2, 2] = (1. * b11 + 1. * b13) / 2

    # Interpolation for the blue channel (b13)
    # r02 and r22 are the red channel values from the neighboring pixels
    r02 = image_bayer[0:-2:2, -2]
    r22 = image_bayer[2::2, -2]

    # Average the red values from the neighboring pixels for the blue channel
    result[1:-1:2, -1, 0] = (1. * r02 + 1. * r22) / 2

    # g03, g12, and g23 are the green channel values from the neighboring pixels
    g03 = image_bayer[0:-2:2, -1::2]
    g12 = image_bayer[1:-1:2, -2::2]
    g23 = image_bayer[2::2, -1::2]

    # Average the green values from the neighboring pixels for the blue channel
    result[1:-1:2, -1::2, 1] = (1. * g03 + 1. * g12 + 1. * g23) / 3

    # Assign the existing blue values from the Bayer pattern to the result
    result[1::2, -1::2, 2] = image_bayer[1::2, -1::2]

    # Interpolation for the red channel (r20)
    # Assign the red values from the Bayer pattern for the lower rows in the first column
    result[2:-1:2, 0, 0] = image_bayer[2:-1:2, 0]

    # g10, g21, and g30 are the green channel values from the neighboring pixels
    g10 = image_bayer[1:-1:2, 0]
    g21 = image_bayer[2:-1:2, 1]
    g30 = image_bayer[3::2, 0]

    # Average the green values from the surrounding pixels for the red channel
    result[2:-1:2, 0, 1] = (1. * g10 + 1. * g21 + 1. * g30) / 3

    # b11 and b31 are the blue channel values from the neighboring pixels
    b11 = image_bayer[1:-1:2, 1]
    b31 = image_bayer[3::2, 1]

    # Average the blue values (b11 and b31) for the red channel
    result[2:-1:2, 0, 2] = (1. * b11 + 1. * b31) / 2

    # g21 (Green channel interpolation for the pixels around the middle block)
    # r20 and r22 are the red channel values from the neighboring pixels
    r20 = image_bayer[2:-1:2, :-2:2]
    r22 = image_bayer[2:-1:2, 2::2]

    # Average the red values from the surrounding pixels for the green channel
    result[2:-1:2, 1:-1:2, 0] = (1. * r20 + 1. * r22) / 2

    # Assign the existing green values from the Bayer pattern to the result
    result[2:-1:2, 1::2, 1] = image_bayer[2:-1:2, 1::2]

    # b11 and b31 are the blue channel values from the Bayer pattern
    b11 = image_bayer[1:-1:2, 1::2]
    b31 = image_bayer[3::2, 1::2]

    # Average the blue values (b11 and b31) for the green channel
    result[2:-1:2, 1::2, 2] = (1. * b11 + 1. * b31) / 2

    # r22 (Red channel interpolation for the lower rows and middle block)
    # Assign the red values from the Bayer pattern for the lower rows in the second column
    result[2:-1:2, 2:-1:2, 0] = image_bayer[2:-1:2, 2:-1:2]

    # g12, g21, g23, and g32 are the green channel values from the neighboring pixels
    g12 = image_bayer[1:-1:2, 2:-1:2]
    g21 = image_bayer[2:-1:2, 1:-1:2]
    g23 = image_bayer[2:-1:2, 3::2]
    g32 = image_bayer[3::2, 2:-1:2]

    # Average the green values from the surrounding pixels for the red channel
    result[2:-1:2, 2:-1:2, 1] = (1. * g12 + 1. * g21 + 1. * g23 + 1. * g32) / 4

    # b11, b13, b31, and b33 are the blue channel values from the Bayer pattern
    b11 = image_bayer[1:-1:2, 1:-1:2]
    b13 = image_bayer[1:-1:2, 3::2]
    b31 = image_bayer[3::2, 1:-1:2]
    b33 = image_bayer[3::2, 3::2]

    # Average the blue values (b11, b13, b31, and b33) for the red channel
    result[2:-1:2, 2:-1:2, 2] = (1. * b11 + 1. * b13 + 1. * b31 + 1. * b33) / 4

    # g23 (Green channel interpolation for the right-most column)
    # Assign the red values from the neighboring pixels for the last column
    result[2::2, -1, 0] = image_bayer[2::2, -2]

    # Assign the existing green values from the Bayer pattern to the result for the last column
    result[2::2, -1, 1] = image_bayer[2::2, -1]

    # b13 and b33 are the blue channel values from the Bayer pattern for the last column
    b13 = image_bayer[1:-1:2, -1]
    b33 = image_bayer[3::2, -1]

    # Average the blue values (b13 and b33) for the green channel in the last column
    result[2::2, -1, 2] = (1. * b13 + 1. * b33) / 2

    # g30 (Green channel interpolation for the bottom-right corner)
    # Assign the red, green, and blue values from the Bayer pattern to the last row and column
    result[-1, 0, 0] = image_bayer[-2, 0]
    result[-1, 0, 1] = image_bayer[-1, 0]
    result[-1, 0, 2] = image_bayer[-1, 1]

    # b31 (Blue channel interpolation for the last row)
    # r20 and r22 are the red channel values from the neighboring pixels
    r20 = image_bayer[-2, :-2:2]
    r22 = image_bayer[-2, 2::2]

    # Average the red values (r20 and r22) for the blue channel in the last row
    result[-1, 1:-1:2, 0] = (1. * r20 + 1. * r22) / 2

    # g21, g30, and g32 are the green channel values from the neighboring pixels
    g21 = image_bayer[-2, 1:-1:2]
    g30 = image_bayer[-1, :-2:2]
    g32 = image_bayer[-1, 2:-1:2]

    # Average the green values (g21, g30, and g32) for the blue channel in the last row
    result[-1, 1:-1:2, 1] = (1. * g21 + 1. * g30 + 1. * g32) / 3

    # Assign the existing blue values from the Bayer pattern to the result for the last row
    result[-1, 1::2, 2] = image_bayer[-1, 1::2]

    # g32 (Green channel interpolation for the bottom-right pixel)
    # Assign the red, green, and blue values for the bottom-right corner
    result[-1, 2::2, 0] = image_bayer[-2, -2]
    result[-1, 2::2, 1] = image_bayer[-1, 2]

    # b31 and b33 are the blue channel values for the bottom-right corner
    b31 = image_bayer[-1, 1:-1:2]
    b33 = image_bayer[-1, 3::2]

    # Average the blue values (b31 and b33) for the bottom-right corner
    result[-1, 2::2, 2] = (1. * b31 + 1. * b33) / 2

    # b33 (Blue channel interpolation for the very last pixel)
    # Assign the red, green, and blue values for the very last pixel in the bottom-right corner
    result[-1, -1, 0] = image_bayer[-2, -2]
    g23 = image_bayer[-2, -1]
    g32 = image_bayer[-1, -2]

    # Average the green values (g23 and g32) for the very last pixel
    result[-1, -1, 1] = (1. * g23 + 1. * g32) / 2

    # Assign the blue value from the Bayer pattern to the very last pixel
    result[-1, -1, 2] = image_bayer[-1, -1]

    # Return the final result as an 8-bit image
    return np.uint8(result)

