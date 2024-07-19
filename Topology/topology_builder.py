import meraki
import os
from dotenv import load_dotenv
from pyvis.network import Network
from pprint import pprint
import subprocess


load_dotenv('venv/.env')
API_KEY = os.getenv('MERAKI_API_KEY')  # Get the Meraki API key from environment variable

#Home Network 
ORGANISATION_ID = os.getenv('ORGANISATION_ID') # Get the Organisation ID from environment variable
NETWORK_ID = os.getenv('NETWORK_ID') # Get the Organisation ID from environment variable

net = Network(notebook=True, cdn_resources="remote", height="750px", width="100%", bgcolor="#222222", font_color="white", filter_menu=True, select_menu=True)

##Empty Lists and Dictionaries
nodelist = []
derived_id_list=[]
node_vis = {}


def meraki_session():
    dashboard = meraki.DashboardAPI(api_key=API_KEY, suppress_logging=True)
    return dashboard

### This function pulls the network topology data required by 
### the main "topology_builder" function as a dictionary
### This function then passes that information directly 
### to the "topology_builder" funciton. 
def network_topology(network_id):
    dashboard = meraki_session()    
    networktopologydata = dashboard.networks.getNetworkTopologyLinkLayer(network_id)
    topology_builder(networktopologydata)

def get_device_name(mac_address):
    dashboard = meraki_session() 
    all_devices = dashboard.organizations.getOrganizationDevicesAvailabilities(ORGANISATION_ID, total_pages='all')
    for device in all_devices:
        if mac_address in device["mac"]:
            return device["name"]
        elif mac_address not in device["mac"]:
            return "Null"

### This function is a catch for any device that is
### currently unprofiled, this catch will print information
### about the node to screen for further script enhancement
def unknown_node_prebuilder(node_info):
    #print (node_info)
    unpb_label = node_info["derivedId"]
    derived_id_list.append(node_info["derivedId"])
    node_vis[node_info["derivedId"]] = unpb_label
    net.add_node(unpb_label, 
                 label=unpb_label, 
                 shape="circle",
                 title="This Device is UNKNOWN")

### This function is a catch for any devices that do not
### include the "device" element within the returned 
### "network_topology" request function
def other_node_prebuilder(node_info):
    onpb_device_mac = node_info["mac"]
    nodelist.append(onpb_device_mac)  
    onpb_root_query = node_info["root"]
    onpb_label = get_device_name(onpb_device_mac)
    if onpb_label == "Null":
        onpb_label = node_info["derivedId"]
    if onpb_root_query == True:
        onpb_root = "Yes"
    else:
        onpb_root = "No"
    derived_id_list.append(onpb_label)
    node_vis[node_info["derivedId"]] = onpb_label
    onpb_caption = f"Device MAC address: {onpb_device_mac}\n Is root:{onpb_root}"
    onpb_icon = "Topology/Cisco-Meraki-Topology-Icons/unknown.png"
    meraki_node_builder(onpb_label, onpb_icon, onpb_caption)

### This function gathers all the information required to 
### create all nodes that have provide standard "device"
### information from the "network_topology" function
def meraki_node_prebuilder(node_info):
    node_mac = node_info["mac"]
    nodelist.append(node_mac)
    derived_id_list.append(node_info["derivedId"])
    mnpb_device_information = node_info["device"]
    mnpb_label   = mnpb_device_information.get("name")
    mnpb_model   = mnpb_device_information.get("model")
    mnpb_product = mnpb_device_information.get("productType")
    mnpb_serial  = mnpb_device_information.get("serial")
    mnpb_status  = mnpb_device_information.get("status")
    mnpb_client  = mnpb_device_information.get("clients", {}).get("counts",{}).get("total")
    node_vis[node_info["derivedId"]] = mnpb_label
    mnpb_caption = f"This is a {mnpb_model} device\nSerial Number:{mnpb_serial}\nStatus:{mnpb_status}\nTotal Clients (last 24hrs):{mnpb_client}" 
    if mnpb_product == "wireless":
        mnpb_device_icon = "Topology/Cisco-Meraki-Topology-Icons/topology-icon-mr-indoor-medium.png"
        meraki_node_builder(mnpb_label,mnpb_device_icon,mnpb_caption)
        meraki_wireless_client_prebuilder(mnpb_serial, mnpb_label)
    elif mnpb_product =="camera":
        mnpb_device_icon = "Topology/Cisco-Meraki-Topology-Icons/topology-icon-mv21-medium.png"
        meraki_node_builder(mnpb_label,mnpb_device_icon,mnpb_caption)
    elif mnpb_product == "appliance":
        mnpb_device_icon = "Topology/Cisco-Meraki-Topology-Icons/topology-icon-mx-medium.png"
        meraki_node_builder(mnpb_label,mnpb_device_icon,mnpb_caption)
    elif mnpb_product == "switch":
        mnpb_device_icon = "Topology/Cisco-Meraki-Topology-Icons/topology-icon-ms-layer2-stack-medium.png"
        meraki_node_builder(mnpb_label,mnpb_device_icon,mnpb_caption)
        #meraki_switched_client_prebuilder(mnpb_serial, mnpb_label)

### This function will build the node within the PyVis topology,
### the information passed in to this function will be 
### the node label, image/icon, and the desired caption
def meraki_node_builder(mnb_label, mnb_icon, mnb_caption):
    net.add_node(mnb_label, 
                 label=mnb_label,
                 title=mnb_caption, 
                 shape="image", 
                 image=mnb_icon)

### This function gathers all the information required to 
### create all wireless clients as PyVis nodes
### This also passed the connected network device label     
def meraki_wireless_client_prebuilder(mwcpb_serial, mwcpb_connected_node_label):
    dashboard = meraki_session()
    mwcpb_wireless_clients = dashboard.devices.getDeviceClients(mwcpb_serial, timespan=300) 
    for mwcpb_client in mwcpb_wireless_clients:
        mwcpb_client_label = mwcpb_client["description"]
        if mwcpb_client["description"] == None:
            mwcpb_client_label = "unknown"
        mwcpb_mac = mwcpb_client["mac"]
        mwcpb_ip = mwcpb_client["ip"]
        mwcpb_vlan = mwcpb_client["vlan"]
        mwcpb_caption = (f"Mac Address:{mwcpb_mac}\nIP Address:{mwcpb_ip}\nVLAN:{mwcpb_vlan}")
        mwcpb_icon = "Topology/Cisco-Meraki-Topology-Icons/topology-icon-laptop-user-medium.png"
        meraki_client_builder(mwcpb_caption, mwcpb_icon, mwcpb_client_label, mwcpb_connected_node_label, mwcpb_ip)
        nodelist.append(mwcpb_mac)

### This function will build the client node within
### the PyVis topology, in addition this creates the 
### PyVis edge connection, connecting client to AP
def meraki_client_builder(mcb_caption, mcb_icon, mcb_client_label, mcp_connected_node_label, mcp_ip):
    net.add_node(mcb_client_label,
                  label=mcp_ip,
                  title=mcb_caption,
                  shape="image",
                  image=mcb_icon) 
    net.add_edge(mcp_connected_node_label,mcb_client_label, title= "Wireless Connection", color="green")

#image=mcb_icon

### This function gathers all the information required to 
### create all switched wired clients as PyVis nodes
### CURRENTLY NOT IN USE
def meraki_switched_client_prebuilder(mscpb_serial, mscpb_connected_node_label):
    dashboard = meraki_session()
    mscpb_switch_clients = dashboard.devices.getDeviceClients(mscpb_serial)
    for mscpb_switch_client in mscpb_switch_clients:
        mscpb_mac = mscpb_switch_client["mac"]
        if mscpb_mac not in nodelist:
            mscpb_client_label = mscpb_switch_client["description"]
            mscpb_ip = mscpb_switch_client["ip"]
            mscpb_vlan = mscpb_switch_client["vlan"]
            mscpb_caption = (f"Mac Address:{mscpb_mac}\nIP Address:{mscpb_ip}\nVLAN:{mscpb_vlan}")
            mscpb_icon = "Topology/Cisco-Meraki-Topology-Icons/topology-icon-laptop-user-medium.png"
            meraki_client_builder(mscpb_caption, mscpb_icon, mscpb_client_label, mscpb_connected_node_label, mscpb_ip)
            nodelist.append(mscpb_mac)

def topology_builder(networkdata):  
    nodes = networkdata["nodes"] 
    for node in nodes:
        #print (node)
        if "device" in node:
            meraki_node_prebuilder(node)            
        elif 'device' not in node:
            other_node_prebuilder(node)
        else:
            unknown_node_prebuilder(node)
    connections = networkdata["links"] 
    for connection in connections:
        try:
            edge_title_a = connection["ends"][0]["discovered"]["cdp"]["portId"]
        except:
            edge_title_a = "portX"
        try:
            edge_title_b = connection["ends"][1]["discovered"]["cdp"]["portId"]
        except:
            edge_title_b = "portX"
        end_a = connection["ends"][0]["node"]["derivedId"]
        end_b = connection["ends"][1]["node"]["derivedId"]
        if end_a and end_b in node_vis:
            conn_a = node_vis[end_b]
            conn_b = node_vis[end_a]
        if edge_title_a == "none type" or edge_title_b == "none type":
            print("This edge will be skipped")
        edge_titles = (f"{end_a}\t - {edge_title_a}\n{end_b}\t - {edge_title_b}")   
        net.add_edge(conn_a,conn_b, title=edge_titles)
    net.show("nodes.html")
    html_file_path = "/home/mccube/M3-Github-Projects/Meraki/nodes.html"
    windows_file_path = html_file_path.replace("/","\\")
    subprocess.run(["/mnt/c/Windows/explorer.exe", windows_file_path])
        
network_topology(NETWORK_ID)
