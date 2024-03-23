# Let's write the Python script based on the steps outlined.

def extract_errors(input_file, output_file):
    """
    Extracts lines containing 'ERROR' from the input_file and writes them to the output_file.

    Parameters:
    - input_file (str): Path to the input file to read from.
    - output_file (str): Path to the output file to write to.
    """
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                if 'ERROR' in line:
                    outfile.write(line)
        print(f"Lines containing 'ERROR' have been successfully extracted to {output_file}.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Uncomment the line below to run the function with your specific file paths
extract_errors('./node/debug_GSTREAMER.txt', './error.txt')
