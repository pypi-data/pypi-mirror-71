"""
This module contains the PXDataset class and its associated methods,
which are the foundation of the ppx package.
"""
import xml.etree.ElementTree as ET
import urllib.request
import logging
import os
import shutil
import time


class PXDataset:
    """Retrieve information about a ProteomeXchange project.

    Parameters
    ----------
    pxid : str
        A ProteomeXchange identifier, such as "PXD000001".

    Attributes
    ----------
    name : str
    description : str
    taxonomies : list of str
    references : list of str
    url : str
    return_id : str
    query_id : str
    data : xml.etree.ElementTree.ElementTree
    """
    def __init__(self, pxid):
        """Instantiate a PXDataset object."""

        if not isinstance(pxid, str):
            raise TypeError("'pxid' must be a string (str).")

        pxid = pxid.upper()
        pxid_conditions = [len(pxid) == 9,
                           pxid[0:3] == "PXD" or pxid[0:3] == "PRD",
                           pxid[3:9].isdigit()]

        if not all(pxid_conditions):
            raise ValueError("Malformed ProteomeXchange identifier.")

        url = (f"http://proteomecentral.proteomexchange.org/cgi/GetDataset?ID="
               f"{pxid}&outputMode=XML&test=no")

        logging.debug("ProteomeXchange URL is %s", url)

        xml = ET.parse(_openurl(url))
        root = xml.getroot()

        self._format_version = root.attrib["formatVersion"]
        self._return_id = root.attrib["id"]
        self._query_id = pxid
        self._data = xml

        if self._return_id != pxid:
            logging.warning("The identifier, %s, was not found. Retrieved "
                            "%s instead.", pxid, self._return_id)

    @property
    def return_id(self):
        """
        The ProteomeXchange identifier returned by the server. There
        are cases where this may differ from the query identifier.
        """
        return self._return_id

    @property
    def query_id(self):
        """The queried ProteomeXchange identifier."""
        return self._query_id

    @property
    def data(self):
        """The parsed XML data returned by the ProteomeXchange server."""
        return self._data

    @property
    def url(self):
        """The URL of the FTP server associated with the project."""
        links = _getnodes(self.data,
                          ".//cvParam[@name='Dataset FTP location']")

        if not links:
            raise ValueError(f"No FTP URL found for {self.return_id}.")

        link = links[0]

        # This fixes an annoying bug caused by PRIDE URL changes.
        # See https://github.com/lgatto/rpx/issues/5 for details.
        if (link.startswith("ftp://ftp.pride.ebi")
                and "pride/data/archive" not in link):
            link = link.replace("ebi.ac.uk/", "ebi.ac.uk/pride/data/archive/")

        return link

    @property
    def taxonomies(self):
        """The species and other taxonomies provided for the project."""
        tax = _getnodes(self.data, ".//cvParam[@accession='MS:1001469']")
        if not tax:
            logging.warning("No taxonomies reported for %s.", self.return_id)
            tax = None

        return tax

    @property
    def references(self):
        """Bibliographic information for the project."""
        curr_ref = _getnodes(self.data,
                             ".//cvParam[@accession='PRIDE:0000400']")
        pend_ref = _getnodes(self.data,
                             ".//cvParam[@accession='PRIDE:0000432']")

        all_ref = curr_ref + pend_ref
        if not all_ref:
            logging.warning("No references reported for %s.", self.return_id)
            all_ref = None

        return all_ref

    @property
    def description(self):
        """A description of the project."""
        desc = self.data.getroot().find(".//Description")
        if desc is None:
            return None

        return desc.text

    @property
    def name(self):
        """The name of the project."""
        name = self.data.getroot().find(".//RepositoryRecord")
        if name is None:
            return None

        return name.attrib["name"]

    def list_dirs(self, path=None):
        """
        List available directories on the FTP server.

        Parameters
        ----------
        path : str or list of str, optional
            The subdirectory on the FTP server to look in. A list
            will be concatenated into a single URL.

        Returns
        -------
        list of str
             The directories available on the FTP server.
        """
        if isinstance(path, str):
            path = [path]

        if path is not None:
            url = "/".join([self.url] + path)
        else:
            url = self.url

        _, dirs = _parse_ftp(url)
        if not dirs:
            logging.warning("No directories were found at %s.", url)
            dirs = None

        return dirs

    def list_files(self, path=None):
        """
        List available files on the FTP server.

        Parameters
        ----------
        path : str or list of str, optional
            The subdirectory on the FTP server to look in. A list
            will be concatenated into a single URL.

        Returns
        -------
        list of str
            The available files on the FTP server.
        """
        if isinstance(path, str):
            path = [path]

        if path is not None:
            url = "/".join([self.url] + path)
        else:
            url = self.url

        files, _ = _parse_ftp(url)
        if not files:
            logging.warning("No files were found at %s.", url)
            files = None

        return files

    def download(self, files=None, dest_dir=".", force_=False):
        """
        Download PXDataset files from the PRIDE FTP location.

        By default, it will not download files that have a file
        with a matching name in the destination directory, `dest_dir`.

        Parameters
        ----------
        files : str or tuple of str, optional
            Specifies the files to be downloaded. The default, None,
            downloads all files found with PXDataset.list_files().
        dest_dir : str, optional
            Specifies the directory to download files into. If the
            directory does not exist, it will be created. The default
            is the current working directory.
        force_ : bool, optional
            When False, files with matching name is dest_dir will not be
            downloaded again. True overides this, overwriting the
            matching file.

        Returns
        -------
        list of str
            A list of the downloaded files.
        """
        if files is None:
            files = self.list_files()
        elif isinstance(files, str):
            files = [files]

        out_files = [os.path.join(dest_dir, f) for f in files]
        all_exist = all([os.path.isfile(f) for f in out_files])

        if all_exist and not force_:
            return out_files

        os.makedirs(dest_dir, exist_ok=True)
        for in_file, out_file in zip(files, out_files):
            if os.path.isfile(out_file) and not force_:
                continue

            logging.info("Downloading %s...", in_file)

            with _openurl(f"{self.url}/{in_file}") as dat, \
                    open(out_file, "wb") as fout:
                shutil.copyfileobj(dat, fout)

        return out_files

    # Depricated methods:
    def pxref(self):
        """Deprecated"""
        logging.warning("'PXDataset.pxref()' is deprecated. Use "
                        "'PXDataset.references' instead.")
        return self.references

    def pxurl(self):
        """Deprecated"""
        logging.warning("'PXDataset.pxurl()' is deprecated. Use "
                        "'PXDataset.url' instead.")
        return self.url

    def pxtax(self):
        """Deprecated"""
        logging.warning("'PXDataset.pxtax()' is deprecated. Use "
                        "'PXDataset.taxonomies' instead.")
        return self.references

    def pxfiles(self):
        """Deprecated"""
        logging.warning("'PXDataset.pxfiles()' is deprecated. Use "
                        "'PXDataset.list_files()' instead.")
        return self.list_files()

    def pxget(self, files, dest_dir="."):
        """Deprecated"""
        logging.warning("'PXDataset.pxget()' is deprecated. Use "
                        "'PXDataset.download()' instead.")
        _ = self.download(files, dest_dir)


# Private functions -----------------------------------------------------------
def _parse_ftp(url):
    """
    Parse the FTP server response.

    Parameters
    ----------
    url : str
        The url of the FTP server.

    Returns
    -------
    files : list of str
    directories : list of str
    """
    if not url.endswith("/"):
        url += "/"

    lines = _openurl(url).read().decode("UTF-8").splitlines()
    files = []
    dirs = []
    for line in lines:
        line = line.split(maxsplit=8)
        if line[0].startswith("d"):
            dirs.append(line[-1])
        else:
            files.append(line[-1])

    return files, dirs


def _getnodes(xml, xpath):
    """Retreive the 'value' attribute from a set of XML nodes.

    Parameters
    ----------
    xml : xml.etree.ElementTree.ElementTree
        XML data in the PXDataset.data attribute.

    XPath : str
        An XPath string used to the define the nodes of interest.

    Returns
    -------
    list of str
        A list containing the 'value' attribute for each node found

    """
    return [node.attrib["value"] for node in xml.getroot().findall(xpath)]


def _openurl(url):
    """
    Open a URL using the ppx user-agent. If an URLError is raised,
    such as by a timeout, the request will retry up to 5 times.

    Parameters
    ----------
    url : str
        The URL to open.

    Return
    ------
    Whatever urllib.request.urlopen() would return.
    """
    req = urllib.request.Request(url)
    req.add_header("user-agent", "ppx (https://pypi.org/project/ppx/)")

    # Retries were added after Travic-CI build failures. These seem to
    # have been necessary due to connectivity issues on Travis servers.
    # Retries may not be needed in normal settings.
    max_retry = 5
    retries = 0
    success = False
    while not success:
        retries += 1
        try:
            dat = urllib.request.urlopen(req, timeout=100)
            success = True
        except urllib.error.URLError:
            logging.debug("Attempt %s  download failed...", retries)
            if retries <= (max_retry - 1):
                time.sleep(3)
            else:
                raise

    return dat
