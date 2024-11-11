# Data Compression Tool

## Project Overview

This Data Compression Tool, implemented in Python, employs Huffman encoding to achieve efficient file compression. By analyzing the frequency of each byte in a file, this tool constructs an optimal binary tree for encoding, thereby reducing the file size. The project demonstrates both my understanding of data structures like heaps and trees and my ability to implement complex algorithms to solve practical problems.

## Features

- **Frequency Analysis:** Calculates and maps each byte’s frequency in the file for optimal compression.
- **Huffman Tree Generation:** Constructs a binary tree using Huffman encoding to minimize the overall file size.
- **Compression and Decompression:** Encodes the file into a compressed binary format and provides a function to revert to the original file.

## Technologies Used

- **Language:** Python

## Installation

To run the Data Compression Tool locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/cristiarazvan/DataCompressionTool.git
    ```

2. Navigate to the project directory:
    ```bash
    cd DataCompressionTool
    ```

3. Run the main script:
    ```bash
    python main.py
    ```

## Usage

- **Compression:** Enter the name of the file you wish to compress when prompted. The tool will generate a compressed `.bin` file in the same directory.
- **Decompression:** The tool can also decompress the `.bin` file, restoring the original file content.
