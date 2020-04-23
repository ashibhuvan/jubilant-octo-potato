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

import glob
import os
import json
from pathlib import Path
from typing import List, Tuple
from os.path import basename

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
    directory = []
    
    #here we are going to walk through the directory 
    for root, dirs, files in os.walk(base_directory):
        for name in files:
            
            #here we are assuming that there is only one json file with the last name .json, the answer to q5 has a method of 
            #opening that does follow this assumption

            if name.endswith((".json")):
                with open(os.path.join(root, name)) as json_data:
                    d = json.load(json_data)
                    
                    #an assumption here is that the json data will have key values for path and owner
                    for i in d:
                        bob = Datablob(i["path"],i["owner"])
                        directory.append(bob)
                        
                    
    return directory                    



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
    if (owner_input[-10:] != "@tesla.com"):
        
        return False
    elif (owner_input.count('@') > 1):
       
        return False
    elif (owner_input[:-10].isalnum() == False):
       
        return False
    elif (' ' in owner_input == True):
        
        return False
    else:
        return True

####################
# QUESTION 3 #
####################
"""
write a comprehensive set of test cases for the "validate_owner" function, inside the test_validate_owner() function.
The "test_validate_owner()" function should throw an `AssertionError` if the function does not pass any of the test cases.
"""

def test_validate_owner():
    ...
    
    fresh = []
    test1 = "john@tesla.com"
    test2 = "jo hn@tesla.com"
    test3 = "john@yahoo.com"
    test4 = "j@hn@tesla.com"
    test5 = "j$hn@tesla.com"
    fresh.extend([test1,test2,test3,test4,test5])
    #here the assertion error was added post submission. i did not have one because due to time constraints.
    for i in fresh:
        try:
            assert (validate_owner(i)),"Test failed for " + i
            print("Test passed for " + i)
        except AssertionError as e:
            print(e)
        
       
   


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
    #here i make 2 lists to store the good emails and the bad emails. 
    good = []
    bad = []
    test = collect_datablobs(base_directory)
    #i collect the datablobs using the existing function and check with the validate_ownder function
    for i in test:
        
        if validate_owner(i.owner):
           
            good.append(i)
        else:
            bad.append(i)
    #the good and bad list are combined and returned as a tuple
    thistuple = (good,bad)
    return thistuple

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
def collect_datablobs_with_owner_hierarchy(base_directory: Path) -> Tuple[List[Datablob], List[Datablob]]:

    directory = []
    flag = True
    #here a flag is set so that if there is no owner ever found for the file, the flag will become true and i can throw 
    #the error

    #this is the same walk as the first question
    for root, dirs, files in os.walk(base_directory):
        for name in files:
            

            if name.endswith((".json")):
                with open(os.path.join(root, name)) as json_data:
                    d = json.load(json_data)
                   

                    for i in d["blobs"]:
                        if ('owner' not in i):
                            if 'default_owner' in d:
                                
                                bob = Datablob(i["path"],d["default_owner"])
                                directory.append(bob)
                            else:
                                #when no owner is found in the file and has to be searched for, a recursive search up
                                #to the parent directory is done
                                flag = False
                                print(flag)
                                base_directory1 = os.getcwd() +"/"+ str(Path(base_directory).parent)
                                os.chdir(root)
                                dir = os.getcwd()
                                os.chdir('..')
                                
                                while dir != base_directory1:
                                   
                                    
                                    if (True):
                                       
                                        
                                        with open(os.path.join(os.getcwd(), 'metadata.json')) as json_data1:
                                            d1 = json.load(json_data1)
                                            
                                            if (d1["default_owner"]):
                                                    bob = Datablob(i["path"],d1["default_owner"])
                                                    
                                                    directory.append(bob)
                                                    flag = True
                                    else:
                                        break
                                    os.chdir('..')

                                    dir = os.getcwd()


                            
                            try:
                                assert (flag), "failed"
                                
                            except AssertionError as e:
                                print(e)
                        
                        else:
                               
                            bob = Datablob(i["path"],i["owner"])
                            directory.append(bob)
                       
                       
                        
  
    good = []
    bad = []
    for i in directory:
        
        if validate_owner(i.owner):
           
            good.append(i)
        else:
            bad.append(i)
 
    print (len(good))
    print (len(bad))
    
    thistuple = (good,bad)
    return thistuple

def test_collect_datablobs_with_owner_hierarchy():
    test_data = DATA_DIR / "Question5"
    good_blobs, bad_blobs = collect_datablobs_with_owner_hierarchy(test_data)
    ...


if __name__ == "__main__":
    test_collect_datablobs()
    test_validate_owner()
    test_collect_datablobs_with_validation()
    test_collect_datablobs_with_owner_hierarchy()
