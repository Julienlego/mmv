### EXESOFT XML PARSER ###
# Coopyright David Barker 2010
#
# Python XML parser



class XMLNode:
    def __init__(self, parent, tag, meta, data, inside):
        self.tag = tag
        self.meta = meta
        self.data = data
        self.inside = inside
        self.parent = parent
        self.children = []
        self.parsed = False


class XMLParser:
    def __init__(self, data):
        self.data = data
        self.meta = {}
        self.root = None

    def ReadMeta(self):
        while "<?" in self.data:
            index = self.data.find("<?")  # Start of tag
            startindex = index + 2  # Start of tag inside
            endindex = self.data.find("?>", index)  # Tag end

            # Get the contents of the angular brackets and split into separate meta tags
            metaraw = self.data[startindex:endindex].strip()
            separated = metaraw.split("\" ")  # Split like so ('|' = split off):
            # thingy = "value|" |other = "whatever|" |third = "woo!"
            
            for splitraw in separated:
                split = splitraw.split("=")

                # Add it to the dictionary of meta data
                self.meta[split[0].strip()] = split[1].strip().strip('\"')

            # Remove this tag from the stored data
            before = self.data[:index]
            after = self.data[(endindex + 2):]
            self.data = "".join([before, after])

    def GetTagMeta(self, tag):
        meta = {}
        
        metastart = tag.find(" ") + 1
        metaraw = tag[metastart:]
        separated = metaraw.split("\" ")  # Split like so ('|' = split off):
        # thingy = "value|" |other = "whatever|" |third = "woo!"

        for splitraw in separated:
            split = splitraw.split("=")

            # Add it to the dictionary of meta data
            meta[split[0].strip()] = split[1].strip().strip('\"')

        return meta

    def StripXML(self):
        # Remove comments
        while "<!--" in self.data:
            index = self.data.find("<!--")
            endindex = self.data.find("-->", index)
            before = self.data[:index]
            after = self.data[(endindex + 3):]
            self.data = "".join([before, after])

        # Remove whitespace
        self.data = self.data.replace("\n", "").replace("\t", "")

    def GetChildren(self, node):
        pass

    def GetRoot(self):
        rootstart = self.data.find("<")
        rootstartclose = self.data.find(">", rootstart)
        roottagraw = self.data[(rootstart + 1):rootstartclose]
        
        rootmeta = {}
        if len(roottagraw.split("=")) > 1:
            rootmeta = self.GetTagMeta(roottagraw)
        
        roottag = roottagraw.strip()
        
        rootend = self.data.find("</%s" % roottag)
        rootendclose = self.data.find(">", rootend)
        rootdata = self.data[rootstart:(rootendclose + 1)].strip()
        rootinside = self.data[(rootstartclose + 1):rootend]

        self.root = XMLNode(parent = None, tag = roottag, meta = rootmeta, data = rootdata, inside = rootinside)

    def SearchNode(self, node):
        node.parsed = True
        
        tempdata = node.inside
        children = []
        
        while "<" in tempdata:
            start = tempdata.find("<")
            startclose = tempdata.find(">", start)
            tagraw = tempdata[(start + 1):startclose]

            meta = {}
            if "=" in tagraw:
                meta = self.GetTagMeta(tagraw)

            tag = tagraw.split(" ")[0]

            end = tempdata.find("</%s" % tag)
            endclose = tempdata.find(">", end)

            data = tempdata[start:(endclose + 1)].strip()
            inside = tempdata[(startclose + 1):end]

            newnode = XMLNode(node, tag, meta, data, inside)
            children.append(newnode)

            before = tempdata[:start]
            after = tempdata[(endclose + 1):]
            tempdata = "".join([before, after])

        node.children = children

        for child in node.children:
            self.SearchNode(child)

    def Parse(self):
        self.ReadMeta()
        self.StripXML()
        self.GetRoot()
        self.SearchNode(self.root)
        
        return self.root
