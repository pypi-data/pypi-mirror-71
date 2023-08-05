
import xml.etree.ElementTree as ET
import uuid

context = None

def init(context_):
    global context
    context = context_


# 将数据服务作为一个可以扩展的扩展点
# 可能有通过文件存储项目，也可能通过数据库存储项目，还可能通过网络存储项目

# 基础数据节点接口
class DataNode:
    def __init__(self):
        pass
    def __str__(self):
        pass
    def get_name(self):
        pass
    def set_name(self, name):
        pass
    def get_id(self):
        pass
    def get_kind(self):
        pass
    def get_props(self):
        pass
    def get_prop(self, key):
        pass
    def set_prop(self, key, value):
        pass
    def parent(self):
        pass
    def set_parent(self, parent):
        pass
    def add_child(self, child):
        pass
    def insert_child(self, child, pos_child):
        pass
    def get_children(self):
        pass
    def get_children_by_kind(self, kind):
        pass
    def get_allchildren_by_kind(self, kind):
        pass
    def remove_child(self, child):
        pass
    def delete(self):
        pass
    def get_child_kinds(self):
        pass
    def load(self, service, node):
        pass
    def save(self, parent_node):
        pass


class DataNodeBase(DataNode):
    def __init__(self, kind = None, name = None):
        self._kind_ = kind
        self._name_ = name
        self._props_ = {}
        self._parent_ = None
        self._child_ = []
        self._id_ = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(uuid.uuid1())+str(uuid.uuid4())))
    def __str__(self):
        return self._name_
    def get_name(self):
        return self._name_
    def set_name(self, name):
        old_name = self._name_
        self._name_ = name
        context.fire('event::DataNode::Modify::Name', self, old_name)
    def get_id(self):
        return self._id_
    def get_kind(self):
        return self._kind_
    def get_props(self):
        return self._props_
    def get_prop(self, key):
        if key in self._props_:
            return self._props_[key]
        else:
            return ""
    def set_prop(self, key, value):
        if key in self._props_:
            old_value = self._props_[key]
            if value == old_value:
                return 
        else:
            old_value = ""
        self._props_[key] = value

        context.fire('event::DataNode::Modify::Prop', self, key, old_value)
    def parent(self):
        return self._parent_
    def set_parent(self, parent):
        self._parent_ = parent
    def add_child(self, child):
        self._child_.append(child)
        child.set_parent(self)

        context.fire('event::DataNode::Modify::AddChild', self, child)

    def insert_child(self, child, pos_child):
        for i in range(0, len(self._child_)):
            if self._child_[i] == pos_child:
                self._child_.insert(i, child)
                child.set_parent(self)

        context.fire('event::DataNode::Modify::AddChild', self, child)

    
    def get_children(self):
        return self._child_
    def get_children_by_kind(self, kind):
        return [child for child in self._child_ if child.get_kind()==kind ]
    def get_allchildren_by_kind(self, kind):
        result = []
        stack = []
        stack.append(self)

        while len(stack)>0:
            node = stack.pop(-1)
            if node.get_kind() == kind:
                result.append(node)
            
            for c in node.get_children():
                stack.append(c)
        
        return result

    def remove_child(self, child):
        self._child_.remove(child)

        context.fire('event::DataNode::Modify::RemoveChild', self, child)
    def delete(self):
        # delete all child
        for child in self._child_:
            child.delete()
        if self._parent_:
            self._parent_.remove_child(self)
        context.fire('event::DataNode::Delete', self)
    def get_child_kinds(self):
        children = self._xml_.findall('./children/Node')
        kinds = []
        for child in children:
            kinds.append(child.attrib['kind'])
        return kinds


class DataNodeXML(DataNodeBase):
    def __init__(self, xml_node = None, kind = None, name = None):
        super().__init__(kind, name)

        self._xml_ = xml_node
        if xml_node:
            props = self._xml_.findall('./Props/Prop')
            for prop in props:
                self._props_[prop.attrib['key']] = prop.attrib['default']

    def load(self, service, node):
        self._name_ = node.attrib['name']
        self._kind_ = node.attrib['kind']

        if 'id' in node.attrib:
            self._id_ = node.attrib['id']

        print("Load Node", self._name_, self._kind_)

        props = node.findall('./Props/Prop')
        for prop in props:
            self._props_[prop.attrib['key']] = prop.attrib['value']
        
        children = node.findall('./Children/Node')
        for child in children:
            cnode = DataNodeXML()
            cnode.load(service, child)
            self._child_.append(cnode)
            cnode.set_parent(self)
        self._xml_ = service._map_node_[self._kind_]

    def save(self, parent_node):
        element = ET.Element('Node')
        element.set('kind', self._kind_)
        element.set('name', self._name_)
        element.set('id', self._id_)
        props = ET.Element('Props')
        element.append(props)
        for prop in self._props_:
            propn = ET.Element('Prop')
            propn.set('key', prop)
            propn.set('value', self._props_[prop])
            props.append(propn)
        children = ET.Element("Children")
        element.append(children)
        for child in self._child_:
            child.save(children)
        parent_node.append(element)

class DataService:
    def __init__(self, config):
        self._xml_ = ET.ElementTree(file=config)
        self._map_node_ = {}

        root = self._xml_.getroot()
        self._map_node_[root.attrib['kind']] = root

        nodes = self._xml_.findall('.//Node')
        for node in nodes:
            kind = node.attrib['kind']
            if not kind in self._map_node_:
                self._map_node_[kind] = node
                #print(node.attrib['kind'])

        self._root_node_ = None
        self._file_ = None
    def project_file(self):
        return self._file_
    def project_file_des(self):
        return {
            "des":"获取项目文件", 
            "name": "project_file",
            "return": "项目保存文件"
        }

    def root_node(self):
        return self._root_node_
    def root_node_des(self):
        return {
            "des":"获取根节点", 
            "name": "root_node",
            "return": "项目根节点"
        }

    def create_rootnode(self, name):
        root = self._xml_.getroot()

        if self._root_node_:
            return None

        self._root_node_ = DataNodeXML(root, root.attrib['kind'], name)

        context.fire('event::NewRootDataNode', self._root_node_)
        return self._root_node_
    def create_rootnode_des(self):
        return {
            "des":"创建根节点", 
            "name": "create_rootnode",
            "return": "项目根节点",
            'paras':[
                {
                    'name': 'name',
                    'des': '根节点名称'
                }
            ]
        }

    def create_node(self, kind, name):
        if not kind in self._map_node_:
            print("Not exist kind!!")
            return None
        xml = self._map_node_[kind]
        node = DataNodeXML(xml, kind, name)

        context.fire('event::NewDataNode', node)
        return node
    def create_node_des(self):
        return {
            "des":"创建节点", 
            "name": "create_node",
            "return": "创建节点",
            'paras':[
                {
                    'name': 'kind',
                    'des': '节点类型'
                },
                {
                    'name': 'name',
                    'des': '节点名称'
                }
            ]
        }
    
    def load(self, file_):
        tree = ET.parse(file_)
        root = tree.getroot()

        children = root.findall('./Node')
        if len(children) != 1:
            return 

        self._file_ = file_        
        pnode = children[0]
        cnode = DataNodeXML()
        cnode.load(self, pnode)
        self._root_node_ = cnode

        context.fire('event::Project::Open', self._root_node_)

        return ""
    def load_des(self):
        return {
            "des":"加载项目", 
            "name": "load",
            "return": "",
            'paras':[
                {
                    'name': 'file_',
                    'des': '项目文件'
                }
            ]
        }

    def save(self, file_):
        root = ET.Element('Root')      
        tree = ET.ElementTree(root)    

        if self._root_node_:
            self._root_node_.save(root)
        
        self.__indent(root)
        tree.write(file_, encoding='utf-8', xml_declaration=True)

        self._file_ = file_
        return ""
    def save_des(self):
        return {
            "des": "保存项目", 
            "name": "save",
            "return": "",
            'paras':[
                {
                    'name': 'file_',
                    'des': '项目保存结果文件'
                }
            ]
        }

    def __indent(self, elem, level=0):
        i = "\n" + level*"\t"
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "\t"
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.__indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

_g_dataservice_ = DataService("./configs/dataservice_config.xml")
_g_config_ = None

def dataservice_declare():
    decl = []
    for fun in dir(_g_dataservice_):
        if type(fun) != type(''):
            continue

        if fun+"_des" in dir(_g_dataservice_):
            decl.append(eval('_g_dataservice_.'+fun+'_des()'))
    
    return decl

# TODO
# 如果数据服务可以被扩展，那么如何确保在服务确定之前就有扩展实现？
# 数据服务应该要在所有扩展完成后，通过配置才能确定激活哪一个数据服务扩展

config = {
    'pluginid': 'Core::AppData',
    "services" : [
        {
            "name": "DataService",
            "define": _g_dataservice_,
            'declare': dataservice_declare()
        }
    ],
    'events' : [
        {
            'name': 'event::NewRootDataNode',
            'value1': 'DataNode'
        },
        {
            'name': 'event::Project::Open',
            'value1': 'DataNode'
        },
        {
            'name': 'event::NewDataNode',
            'value1': 'DataNode'
        },
        {
            'name': 'event::DataNode::Delete',
            'value1': 'DataNode'
        },
        {
            'name': 'event::DataNode::Modify::Name',
            'value1': 'DataNode',
            'value2': 'string'    # old name

        },
        {
            'name': 'event::DataNode::Modify::Prop',
            'value1': 'DataNode',
            'value2': 'string',  # prop key
            'value3': 'string'   # old prop value
        },
        {
            'name': 'event::DataNode::Modify::AddChild',
            'value1': 'DataNode',
            'value2': 'DataNode'  # child
        },
        {
            'name': 'event::DataNode::Modify::RemoveChild',
            'value1': 'DataNode',
            'value2': 'DataNode'  # child
        },
        {
            'name': 'event::DataNode::Select',
            'value1': 'DataNode'
        },
    ]
}