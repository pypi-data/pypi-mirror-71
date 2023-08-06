============================
Mercurial Fingerprint Plugin
============================

The `hg-fingerprint` mercurial plugin does two things:

1. Enhances the `archive` command with options to control
   the ``.hg_archival.txt`` file in the following ways:

   * Allow multiple fingerprint files to be specified,
   * Adjust the file name(s) thereof,
   * Change the file format(s), and
   * Add a timestamp for when the archive was generated.

2. Provides the `fingerprint` command to output the archive
   fingerprint file without having to actually do the archive.


Project
=======

* Homepage: https://bitbucket.org/metagriffin/hg-fingerprint
* Bugs: https://bitbucket.org/metagriffin/hg-fingerprint/issues


Supported Formats
=================

The following formats are supported:

* ``text`` (the default):

  .. code:: text

    repo: dca7d15bf04445e0a3136d5ce5cfa034e5cfa034
    node: 6d881282ad46412ead8ad83e074ce451074ce451
    branch: default
    latesttag: blue
    latesttag: moon
    latesttagdistance: 7
    timestamp: 2009-02-13T23:31:30Z

* ``json`` (whitespace added for clarity):

  .. code:: json

    {
      "repo": "dca7d15bf04445e0a3136d5ce5cfa034e5cfa034",
      "node": "6d881282ad46412ead8ad83e074ce451074ce451",
      "branch": "default",
      "latesttags": ["blue", "moon"],
      "latesttagdistance": 7,
      "timestamp": "2009-02-13T23:31:30Z"
    }

* ``yaml``:

  .. code:: yaml

    repo: dca7d15bf04445e0a3136d5ce5cfa034e5cfa034
    node: 6d881282ad46412ead8ad83e074ce451074ce451
    branch: default
    latesttags: [blue, moon]
    latesttagdistance: 7
    timestamp: '2009-02-13T23:31:30Z'

* ``xml`` (whitespace added for clarity):

  .. code:: xml

    <?xml version='1.0' encoding='UTF-8'?>
    <fingerprint>
      <repo>dca7d15bf04445e0a3136d5ce5cfa034e5cfa034</repo>
      <node>6d881282ad46412ead8ad83e074ce451074ce451</node>
      <branch>default</branch>
      <latesttag>blue</latesttag>
      <latesttag>moon</latesttag>
      <latesttagdistance>7</latesttagdistance>
      <timestamp>2009-02-13T23:31:30Z</timestamp>
    </fingerprint>


Options
=======

The `fingerprint` plugin adds the following new configuration section:

.. code:: ini

  [fingeprint]

  path                    = .hg_archival.txt
  format                  = text
  timestamp               = true


* ``path`` : ( str | list(str) ), default: '.hg_archival.txt'

  The path, within the archive, to store the fingerprint in. The
  results are undefined if the path already exists. The path may
  specify multiple locations (separated and escaped using shell
  escape syntax).

* ``format`` : ( str | list(str) ), default: 'auto'

  The file format to store the fingerprint in. Can be any of the above
  listed formats, plus the special value ``auto``, which specifies
  that the mime-type (based on extension) of the `path` should be
  used. If the `path` specifies multiple locations, then format can
  also be a list. If there are more paths than formats, the last
  format is used.

* ``timestamp`` : bool, default: true

  Whether or not to store the archive generation timestamp in the
  fingerprint in ISO 8601 date-time format. Note that this is the
  only value whose default alters the standard way the `archive`
  command works -- this is because it is *additive*, and should
  therefore have no, or at most minimal, impact.

