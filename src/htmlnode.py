class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
       raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if not self.props:
            return ""

        result = ""
        for key, value in self.props.items():
            result += f" {key}='{value}'"
        return result
    
    def __repr__(self):
        return f"HTMLNode({self.tag!r}, {self.value!r}, {self.children!r}, {self.props!r})"

    class LeafNode:
        def __init__(self, tag, value, props=None):
            self.tag = tag
            self.value = value
            self.props = props
        
        def to_html(self):
            if self.value is None:
                raise ValueError("No value")
            if self.tag is None:
                return f"{self.value}"
            return f"<{self.tag} {self.props}>{self.value}</{self.tag}>"

        def __repr__(self):
            return f"LeafNode({self.tag!r}, {self.value!r}, {self.props!r})"