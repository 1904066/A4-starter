"""
docustring
"""
# Profile.py
# PRIYANKAA NIGAM
# PNNIGAM@UCI.EDU
# 50285154
#
# ICS 32
# Assignment #2: Journal
#
# Author: Mark S. Baldwin, modified by Alberto Krone-Martins
#
# v0.1.9

# You should review this code to identify what features you need to support
# in your program for assignment 2.
#
# YOU DO NOT NEED TO READ OR UNDERSTAND THE JSON SERIALIZATION ASPECTS
# OF THIS CODE
# RIGHT NOW, though can you certainly take a
# look at it if you are curious since we
# already covered a bit of the JSON format in class.
#
import json
import time
from pathlib import Path


# """
# DsuFileError is a custom exception handler that you should catch in
# your own code. It
# is raised when attempting to load or save Profile objects to file
# the system.

# """


class DsuFileError(Exception):
    """
    docustring
    """
    # pass


# """
# DsuProfileError is a custom exception handler that you should catch
# in your own code. It
# is raised when attempting to deserialize a
# dsu file to a Profile object.

# """


class DsuProfileError(Exception):
    """
    docustring
    """
    # pass


class Post(dict):
    """

    The Post class is responsible for
    working with individual
    user posts. It currently
    supports two features: A timestamp property
    that is set upon instantiation and
    when the entry object is set and an entry
    property that stores the post message.

    """
    def __init__(self, entry: str = None, timestamp: float = 0,
                 friend: str = None):
        self._timestamp = timestamp
        self.set_entry(entry)
        self.set_friend(friend)

        # Subclass dict to expose Post properties for serialization
        # Don't worry about this!
        dict.__init__(self, entry=self._entry, timestamp=self._timestamp,
                      friend=self._friend)

    def set_entry(self, entry):
        """
         docustring
        """
        self._entry = entry
        dict.__setitem__(self, 'entry', entry)

        # If timestamp has not been set, generate a new from time module
        if self._timestamp == 0:
            self._timestamp = time.time()

    def set_friend(self, friend):
        """
        docustring
        """
        self._friend = friend
        dict.__setitem__(self, 'friend', friend)

    def get_entry(self):
        """
        docustring
        """
        return self._entry

    def set_time(self, time_):
        """
        docustring
        """
        self._timestamp = time_
        dict.__setitem__(self, 'timestamp', time_)

    def get_time(self):
        """
        docustring
        """
        return self._timestamp

    # """

    # The property method is used to support get
    # and set capability for entry and
    # time values. When the value for
    # entry is changed, or set, the
    # timestamp field is
    # updated to the current time.

    # """
    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)


class Profile:
    """
    The Profile class exposes the properties
    required to join an ICS 32 DSU server. You
    will need to use this class to manage
    the information provided by each new user
    created within your program for
    a2. Pay close attention to the properties
    and functions in this class as you
    will need to make use of each
    of them in your program.

    When creating your program you will need
    to collect user input for the properties
    exposed by this class.
    A Profile class should ensure
    that a username and password
    are set, but contains no conventions
    to do so. You should make sure that your code
    verifies that required properties are set.

    """

    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver  # REQUIRED
        self.username = username  # REQUIRED
        self.password = password  # REQUIRED
        self.bio = ''             # OPTIONAL
        self._posts = []          # OPTIONAL

    # """

    # add_post accepts a Post object as parameter
    # and appends it to the posts list. Posts
    # are stored in a list object in the
    # order they are added. So if multiple
    # Posts objects
    # are created, but added to the Profile
    # in a different order, it is possible for the
    # list to not be sorted by the Post.
    # timestamp property. So take caution as to how you
    # implement your add_post code.

    # """

    def add_post(self, post: Post) -> None:
        """
        docustring
        """
        self._posts.append(post)

    # """

    # del_post removes a Post at a given index and returns
    # True if successful and False if
    # an invalid index was supplied.

    # To determine which post to delete you must
    # implement your own search operation on
    # the posts returned from the get_posts
    # function to find the correct index.

    # """

    def del_post(self, index: int) -> bool:
        """
        docustring
        """
        try:
            del self._posts[index]
            return True
        except IndexError:
            return False

    # """

    # get_posts returns the list
    # object containing all posts
    # that have been added to the
    # Profile object

    # """
    def get_posts(self) -> list[Post]:
        """
        docustring
        """
        return self._posts

    # """

    # save_profile accepts an existing
    # dsu file to save the current
    # instance of Profile
    # to the file system.

    # Example usage:

    # profile = Profile()
    # profile.save_profile('/path/to/file.dsu')

    # Raises DsuFileError

    # """
    def save_profile(self, path: str) -> None:
        """
        docustring
        """
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                with open(p, 'w', encoding='utf-8') as f:
                    json.dump(self.__dict__, f)
            except Exception as ex:
                raise DsuFileError("Error "
                                   "while attempting to"
                                   " process the DSU file."
                                   ) from ex
        else:
            raise DsuFileError("Invalid DSU file path or type")

    # """

    # load_profile will populate the
    # current instance of Profile
    # with data stored in a
    # DSU file.

    # Example usage:

    # profile = Profile()
    # profile.load_profile('/path/to/file.dsu')

    # Raises DsuProfileError, DsuFileError

    # """
    def load_profile(self, path: str) -> None:
        """
        docustring
        """
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                for post_obj in obj['_posts']:
                    post = Post(post_obj['entry'],
                                post_obj['timestamp'],
                                post_obj['friend'])
                    self._posts.append(post)
                f.close()
            except Exception as ex:
                raise DsuProfileError("Error "
                                      "while loading"
                                      " DSU profile.")from ex
        else:
            raise DsuFileError()
