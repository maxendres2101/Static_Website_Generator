class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError


    def props_to_html(self):
        res = ""
        if not self.props:
            return ""
        for key in self.props:
            res += f' {key}="{self.props[key]}"'

        return res 
    
    def __repr__(self):
        return f"Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props}"




class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None, ):
        super().__init__(tag = tag, value = value, props = props)
        self.tag = tag
        self.value = value
        self.props = props

    def to_html(self):
        if self.value == None:
            raise ValueError("Invalid Html: no value")

        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, {self.props})'



class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag = tag, children = children, props = props)
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: ParentNode needs tag")
        elif self.children is None or len(self.children) == 0 :
            raise ValueError("Invalid HTML: ParentNode needs children")

        children_html = ''
        for child in self.children: 
            children_html += child.to_html()

        return f"<{self.tag}>{children_html}</{self.tag}>"