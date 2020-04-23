"""
All python is targetting python 3.7. Questions have been designed so that good solutions are
possible with only the standard library. You may use external packages if you wish but any
extra requirements should be well justified and documented

A system for storing arbitrary binary data files ("Datablobs") uses a directory tree on a file system.

The system uses a single json file ("metadata.json") in each folder to describe the binary blobs in each folder.

There can be one or more blobs in a folder, and each blob will have an entry in the metadata.json file.

An example of this filesystem in practice is given in the `data/Question*` directory.

The metadata is to be represented in python by the "Datablob" class below.

Tests and example data are provided for some questions, but should not be considered comprehensive. You may add to the test
functions if you desire.

You may assume any metadata.json file will be valid json.

Leave comments regarding
- any assumptions you made
- any tradeoffs you made between readability/development cost vs runtime performance

"""


from pathlib import Path
from typing import List, Tuple

class Datablob:
    def __init__(self, path: Path, owner: str):
        self.path: Path = path  # the location of the blob on the filesystem, populated by the "path" field in json
        self.owner: str = owner  # the owner of the data, populated by the "owner" field in json

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.path == other.path and self.owner == other.owner
        else:
            return False

DATA_DIR = Path(__file__).parent / "data"


####################
# QUESTION 1 #
####################
"""
complete the function collect_datablobs() below, that given a base directory,
will search that directory (and all recursive subdirectories) for multiple metadata.json files,
read the files, parse each file content into a Datablob, and return a list of all Datablobs found in the directory tree.

The order of the returned list is unimportant.

hint: The `pathlib.Path.glob()` function and json module might be helpful here.
You may use the test function below to develop your solution
"""

def collect_datablobs(base_directory: Path) -> List[Datablob]:
    ...



def test_collect_datablobs():
    test_data = DATA_DIR / "Question1-3"
    blobs = collect_datablobs(test_data)
    assert len(blobs) == 3
    ...


####################
# QUESTION 2 #
####################
"""
Some users have been incorrectly specifying the owner field in their metadata,
for example writing "john" instead of "john@tesla.com", or using a non-string json type.
Complete the funciton below that checks if that a "owner_input" is
a string containing a valid tesla.com address, return `True` if valid, `False` in any other case.

For this exercise, a valid email address is one that that meets the following requirements:
R1: ends in @tesla.com
R2: does not contain any other "@" symbols except for the one in the trailing "@tesla.com"
R3: contains at least one alphanumeric character before the @ symbol (alphanumeric is defined as a-z, A-Z, 0-9)
R4: does not contain any spaces

You may like to develop Question 3 at the same time as Question 2.
"""

def validate_owner(owner_input) -> bool:
    ...

####################
# QUESTION 3 #
####################
"""
write a comprehensive set of test cases for the "validate_owner" function, inside the test_validate_owner() function.
The "test_validate_owner()" function should throw an `AssertionError` if the function does not pass any of the test cases.
"""

def test_validate_owner():
    ...


####################
# QUESTION 4 #
####################
"""
use your "validate_owner" function create a new function, "collect_datablobs_with_validation".
This function is similar to the function in Q1, but instead returns a tuple of lists.
The first item in the tuple is the list of the Datablobs that passed validation, the second is the
list of Datablobs that failed validation.
"""
def collect_datablobs_with_validation(base_directory: Path) -> Tuple[List[Datablob], List[Datablob]]:
    ...


def test_collect_datablobs_with_validation():
    test_data = DATA_DIR / "Question4"
    good_blobs, bad_blobs = collect_datablobs_with_validation(test_data)
    assert len(good_blobs) == 2
    assert len(bad_blobs) == 1
    ...


####################
# QUESTION 5 #
####################
"""
Your users have been complaining that they are tired of writing out the "owner" field for every metadata.json,
so you decide to implement a system where you can specify a  "default_owner" field in one metadata.json,
and it will propogate to all Datablobs in its directory and subdirectories.

The schema for metadata.json has now changed, so that:
- base level structure is an object, not a list
- there is an optional "default_owner" field
- list of blob items are now contained within the "blob" key

See Question5/metadata.json for an example.

Your solution should meet the following requirements:

- If a blob does not have a owner specified, it inherits the owner from the metadata.json in the following order:
   1) the default_owner field in the current metadata.json file
   2) the default_owner field in any parent directory metadata.json, all the way up to the base search directory
- All blobs must have an owner (whether valid or invalid as defined in Q3). If any blobs do not have
    an owner specified, a ValueError exception should be thrown
- Function must be named "collect_datablobs_with_owner_hierarchy" with return type Tuple[List[Datablob], List[Datablob]] as in Q4
- Your solution should be capible of parsing the old json schema (Q1-4) without default_owners,
    and the new schema (Q5), however schemas will not be mixed within one directory tree.


Complete the collect_datablobs_with_owner_hierarchy(...) function to return a list of good and bad Datablobs,
using the validin Q1

You may define the parameters for this function, and any other helper functions you need

You may use the test below and the data in the Question5 directory to check your solution.

"""

# Your solution here
...


def test_collect_datablobs_with_owner_hierarchy():
    test_data = DATA_DIR / "Question5"
    good_blobs, bad_blobs = collect_datablobs_with_owner_hierarchy(test_data)
    ...


if __name__ == "__main__":
    test_collect_datablobs()
    test_validate_owner()
    test_collect_datablobs_with_validation()
    test_collect_datablobs_with_owner_hierarchy()
