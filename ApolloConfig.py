from xml.etree import ElementTree

# Config
class Config:
    # __init__
    def __init__(self):
        # XML tree and root
        self.config_file = None
        self.xml_tree = None
        self.xml_root = None

        # paramters parsed from configuration
        self.streams_source = None
        self.records_source = None
        self.oldest_source = None

        # discord channel ids
        self.notifs_channel = None
        self.records_channel = None
        self.test_channel = None

        # dictionary of commands
        self.commands = dict()

    # parse
    def parse(self, config_file):
        self.config_file = config_file
        self.xml_tree = ElementTree.parse(config_file)
        self.xml_root = self.xml_tree.getroot()

        self.download_path_rel = self.parse_from_subtree(self.xml_root, "DownloadPathRel").text.strip()

        print("DownloadPathRel:", self.download_path_rel)
        print("")
        self.parse_commands(self.xml_root)