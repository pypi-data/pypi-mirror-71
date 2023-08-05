import csv
import re
import shutil
import tempfile


from collections import OrderedDict
from pathlib import Path, PosixPath
from typing import Union


class Anonymize:

    def __init__(
            self, 
            substitution_dict: Union[dict, Path],
            pattern: str=None,
            use_word_boundaries=False,
            zip_format: str='zip'
        ):

        # if there is no substitution dictionary then convert the csv 
        # substitution table into a dictionary
        if type(substitution_dict) is dict:
            self.substitution_dict = substitution_dict
        else:
            self.substitution_dict = self.__convert_csv_to_dict(
                substitution_dict
            )

        # using word boundaries around pattern or dict keys, avoids
        # substring-matching
        self.use_word_boundaries = use_word_boundaries

        # the regular expression to locate id numbers
        if pattern != None:
            if self.use_word_boundaries == True:
                pattern = r'\b{}\b'.format(pattern)
            self.pattern = re.compile(pattern)
        else:
            self.pattern = False
            # re-order the OrderedDict such that the longest
            # keys are first: ensures that shorter versions of keys
            # will not be substituted first if bigger substitutions 
            # are possible
            self.__reorder_dict()
            # add word boundaries if requested
            if self.use_word_boundaries == True:
                self.substitution_dict = dict([
                    (r'\b{}\b'.format(key), value)
                    for key, value in self.substitution_dict.items()
                ])




        # this is for processed zip archives
        self.zip_format = zip_format

        # Are we going to make a copy?
        self.copy = False



    def __convert_csv_to_dict(self, path_to_csv: str):
        '''Converts 2-column csv file into dictionary. Left
        column contains ids, right column contains substitutions.
        '''
        # read csv file
        reader = csv.DictReader(open(path_to_csv))
        # convert ordered dict into a plain dict, strip any white space
        data = [
            tuple([item.strip() for item in key_value_pair.values()]) 
            for key_value_pair in reader
        ]
        return OrderedDict(data)


    def __reorder_dict(self):
        '''Re-order the substitution dictionary such that longest keys 
        are first'''
        new_dict = sorted(
            self.substitution_dict.items(), 
            key=lambda t: len(t[0]), 
            reverse=True
        )
        self.substitution_dict = OrderedDict(new_dict)


    def substitute(self, 
        source_path: Union[str, Path], 
        target_path: Union[str, Path]=None
        ):

        # ensure source_path is a Path object
        if type(source_path) is str:
            source_path = Path(source_path)

        # ensure we have a target Path
        if target_path == None:
            # no target path, target is parent of source
            target_path = source_path.parent
        else:
            # convert to Path if necessary
            if type(target_path) is str:
                target_path = Path(target_path)
            # we will produce a copy
            self.copy = True

        self.__traverse_tree(source_path, target_path)


    def __traverse_tree(self, 
        source: Path,
        target: Path
        ):

        if source.is_file():
            self.__process_file(source, target)
        else:

            # this is a folder, rename/create if necessary
            (source, target) = self.__process_folder(source, target)

            for child in source.iterdir():
                self.__traverse_tree(child, target)

    
    def __process_folder(self, 
        source: Path,
        target: Path
        ) -> Path:

        result = None

        # process target
        target = self.__process_target(source, target)

        if self.copy == True:
            # we are making a copy, create this folder in target
            self.__make_dir(target)
            result = (source, target)
        else:
            # we are only doing a substitution, rename
            self.__rename_file_or_folder(source, target)
            result = (target, target)

        return result
            

    def __process_file(self, 
        source: Path,
        target: Path
        ):

        # process target
        target = self.__process_target(source, target)

        extension = source.suffix

        if extension in ['.txt', '.csv', '.html', '.json']:
            self.__process_txt_based_file(source, target)
        elif extension in ['.zip', '.gzip', '.gz']:
            self.__process_zip_file(source, target, extension)
        else:
            self.__process_unknown_file_type(source, target)


    def __process_target(self,
        source: Path,
        target: Path
        ):
        substituted_name = self.__substitute_ids(source.name)
        return target / substituted_name


    def __process_txt_based_file(self,
        source: Path,
        target: Path
        ):

        # read contents
        contents = self.__read_file(source)
        # substitute
        substituted_contents = [self.__substitute_ids(line) for line in contents]
        if self.copy == False:
            # remove the original file
            self.__remove_file(source)
        # write processed file
        self.__write_file(target, substituted_contents)


    def __process_unknown_file_type(self,
        source: Path,
        target: Path
        ):

        if self.copy == False:
            # just rename the file
            self.__rename_file_or_folder(source, target)
        else:
            # copy source into target
            self.__copy_file(source, target)


    def __process_zip_file(self, 
        source: Path,
        target: Path,
        extension: str
        ):

        # create a temp folder to extract to
        with tempfile.TemporaryDirectory() as tmp_folder:
            # extract our archive
            shutil.unpack_archive(source, tmp_folder)
            # this is hacky, but inevitable: I want an in-place
            # processing, maybe we were copying, I have to switch it
            # off and on again
            copy = self.copy
            self.copy = False
            # perform the substitution
            self.substitute(Path(tmp_folder))
            # zip up the substitution
            shutil.make_archive(
                target.parent / target.with_suffix(''),
                self.zip_format,
                tmp_folder
            )
            # restore the copy feature
            self.copy = copy
            # remove original zipfile if we are not producing a copy
            if self.copy == False:
                self.__remove_file(source)


    def __substitute_ids(self, string: str):
        '''Heart of this class: all matches of the regular expression will be
        substituted for the corresponding value in the id-dictionary'''
        if self.pattern == False:
            #
            # This might be more efficient:
            # https://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_algorithm
            #
            # loop over dict keys, try to find them in string and replace them 
            # with their values
            for key, value in self.substitution_dict.items():
                string = re.sub(key, value, string, flags=re.IGNORECASE)
        else:
            # identify patterns and substitute them with appropriate substitute
            string = self.pattern.sub(
                lambda match: self.substitution_dict.get(
                    match.group(),
                    match.group()
                ),
                string
            )
        return string


    # FILE OPERATIONS, OVERRIDE THESE IF APPLICABLE


    def __make_dir(self, path: Path):
        path.mkdir(exist_ok=True)


    def __read_file(self, source: Path):
        f = open(source, 'r', encoding='utf-8')
        contents = list(f)
        f.close()
        return contents


    def __write_file(self, path: Path, contents: str):
        f = open(path, 'w', encoding='utf-8')
        f.writelines(contents)
        f.close()


    def __remove_file(self, path: Path):
        path.unlink()

    
    def __remove_folder(self, path: Path):
        shutil.rmtree(path)


    def __rename_file_or_folder(self, source: Path, target: Path):
        source.replace(target)


    def __copy_file(self, source: Path, target: Path):
        if source != target:
            shutil.copy(source, target)



