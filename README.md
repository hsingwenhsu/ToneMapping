# Project 1 README
## Programming Language
- Python: 3.9.2

## Dependencies
- OpenCV: 4.5.1
- NumPy: 1.20.1

## How to run the code
### Getting the hdr image
- In directory `code/`
    ```
    $ python3 hdr.py ../data
    ``` 
    - Note: Should make sure that `filenames.csv` and `speed.csv` are in `code/`
### Getting the tone-mapped image
- In directory `code/`
    ```
    $ python3 tonemapping.py ../data/hdr.hdr
    ```
    - Note: Should make sure that the hdr image is already generated

### Result
![Alt text](result.png?raw=true "Title")
