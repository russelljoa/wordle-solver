# Wordle Solver

An automated solver for the Wordle game that uses letter positioning and elimination strategies to determine the correct word.

## Overview

This project implements an intelligent word solver that tracks letter positions and guesses strategically to minimize the number of attempts needed to solve a Wordle puzzle. The solver maintains state across guesses using color-coded feedback (green, yellow, grey) to narrow down possible solutions.

## Features

- **Letter Tracking**: Maintains lists of correctly placed (green), misplaced (yellow), and eliminated (grey) letters
- **Word Filtering**: Dynamically filters possible words based on letter constraints
- **Strategic Guessing**: Recommends words based on remaining possibilities and letter frequency
- **Configurable Modes**: Support for different solving strategies (prioritize speed vs. minimize guesses)
- **Comprehensive Word List**: Utilizes an extensive dictionary for valid Wordle words
- **Test Suite**: Includes automated testing framework for validation

## Project Structure

```
main.py                # Core solver implementation
words_dict.py          # Dictionary of valid Wordle words
data_populate.py       # Utility to generate optimized data structures
data.json              # Pre-computed word position data
testSuite/             # Automated testing and validation
  solver.py            # Test solver implementation
  tester.py            # Test runner
```

## Setup

1. Ensure the word list and data files are generated:
   ```bash
   python data_populate.py
   ```

2. The solver is now ready to use in `main.py`

## Usage

```python
from main import Solver

solver = Solver(data)
# Process game feedback and get recommended guesses
```

## Testing

Run the test suite to validate solver performance:
```bash
python testSuite/tester.py
```

## Technical Details

The solver uses a data structure that indexes all valid words by letter position, enabling efficient filtering of candidates. By tracking which letters have been tested and their results, the solver progressively eliminates impossible words until the solution is found.

## Performance

The solver achieves efficient word elimination by leveraging pre-computed data structures that organize the word list by letter position, reducing the search space with each guess.
