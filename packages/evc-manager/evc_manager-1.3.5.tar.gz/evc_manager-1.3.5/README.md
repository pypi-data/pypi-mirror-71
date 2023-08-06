# AmLight Ethernet Virtual Circuit (EVC) Manager

The AmLight EVC Manager is a command line tool to help SDN operators in 
managing Ethernet Virtual Circuits (EVC), such as
creating/deleting/changing multiple EVCs at a time. It was created to
help AmLight network engineers in the daily operation of the AmLight SDN
network, which currently has more than one thousands flows and more than
ten OpenFlow switches in North and South America.

The AmLight EVC\_Manager requires Python 3.6+

# Features

The EVC Manager was created with the following major goals:

>   - Supporting multiple backends, such as OESS and Kytos E-Line.
>   - Supporting exporting EVCs to YAML or JSON files
>   - Supporting creating/changing/deleting multiple EVCs via YAML files
>   - Supporting moving EVCs out a specific link (or NNI)
>   - Supporting forcing circuit reprovisioning
>   - Supporting changing EVCs' paths
>   - Supporting exporting monitoring data using Zabbix LLD format for
>     integration with Zabbix
>   - Supporting multiple queries:
>       - Get VLANs in use in a specific UNI or NNI
>       - Get EVCs using a specific UNI or NNI
>       - Get EVC utilization
>       - Get list of EVCs with under-provisioned paths
>       - Get EVCs using backup paths
>       - Get list of devices and links
>       - Compare and report two EVC dumps

# Current Version

The current EVC Manager is 0.3. The following major features are supported:

>   - Supporting for OESS 1.0.9 backend
>   - Supporting exporting all EVCs to YAML or JSON files
>   - Supporting creating/changing/deleting multiple EVCs via YAML files
>   - Supporting for EVC creation using VLAN ranges
>   - Supporting moving EVC out a specific link (or NNI)
>   - Supporting changing EVCs' paths
>   - Supporting multiple queries:
>       - Get EVC using a specific UNI
>       - Get EVC using a specific NNI
>       - Get EVC using backup paths

Version 0.4 is scheduled for March 2020 with the following features:

>   - Supporting exporting monitoring data using Zabbix LLD format for
>     integration with Zabbix
>   - Supporting for Kytos MEF E-Line backend
>   - Supporting forcing EVC reprovisioning
>   - Supporting multiple queries:
>       - Get VLANs in use in a specific UNI
>       - Get circuit utilization
>       - Get circuit with under-provisioned paths
>       - Get list of devices and links

# Using the evc manager

The EVC Manager should run as a Python module and installed directly from pip repository.
Before using the EVC Manager, make sure you have Python3 and PIP for your environment. 
Then, prepare the environment using the following steps:

Create a Python virtual environment:

    python3 -m venv py3-evc_manager
    source py3-evc_manager/bin/activate
    
Install git. Then, close the repo and install all requirements

    pip install evc_manager

There are two options to run EVC Manager. As a script at the Shell or as a module in your
application.

To run EVC Manager as a script, just run using the syntax below:

    python3.6 -m evc_manager [-h] (-L | -A | -R | -C | -D | -M | -X)
                   [--move-from-nni MOVE_FROM_NNI] [-f SOURCE_FILE]
                   [-F DESTINATION_FILE] [--has-uni-device HAS_UNI_DEVICE]
                   [--has-uni-interface HAS_UNI_INTERFACE]
                   [--has-uni-tag-value HAS_UNI_TAG_VALUE]
                   [--has-nni-name HAS_NNI_NAME]
                   [--has-nni-name-primary HAS_NNI_NAME_PRIMARY]
                   [--has-nni-name-backup HAS_NNI_NAME_BACKUP] [-u USER]
                   [-t TENANT] [-p PASSWORD | -P] [-O OESS_URL | -K KYTOS_URL]
                   [-V] [-v {info,warning,debug}] [-q]
                   [-y | -Y | -j | -z | -n] [-T TO_TABLE]
                   [-s GEN_STATS_PER_NNI] [-S SHORTCUT_FILE]

    optional arguments:
      -h, --help            show this help message and exit
      -L, --list-evc        List all EVCs and output them using YAML
      -A, --add-evc         Add EVCs provided in the YAML file
      -R, --add-range-evcs  Add a range of EVCs provided in the YAML file
      -C, --change-evc      Change EVCs provided in the YAML file
      -D, --delete-evc      Delete all EVCs provided in the YAML file
      -M, --move-evc        Move one or all EVCs out the NNI provided.
      -X, --template        Create a template folder with YAML files to help.
      --move-from-nni MOVE_FROM_NNI
                            Move out of the provided NNI
      -f SOURCE_FILE, --source-file SOURCE_FILE
                            Source YAML file used by options -A or -D
      -F DESTINATION_FILE, --destination-file DESTINATION_FILE
                            Destination YAML file used by options -L
      -p PASSWORD, --password PASSWORD
                            Provide pass for authentication
      -P, --prompt_password
                            Prompt pass for authentication
      -O OESS_URL, --oess-url OESS_URL
                            Use OESS backend. Provide OESS's URL
      -K KYTOS_URL, --kytos-url KYTOS_URL
                            Use Kytos E-Line backend's URL.
      -V, --version         show program's version number and exit
      -v {info,warning,debug}, --verbose {info,warning,debug}
                            Set Verbose Level (info|warning|debug)
      -q, --quiet           Set Quiet Mode
      -y, --to-yaml         Print using YAML.
      -Y, --to-yaml-minimal
                            Print using YAML but only the smallest set of
                            mandatory attrs.
      -j, --to-json         Print using JSON.
      -z, --to_zabbix       Converts output to Zabbix LLD format
      -n, --to-screen       Print EVC's names to screen instead of to files
      -T TO_TABLE, --to_table TO_TABLE
                            Converts output to a table format. Use Syntax:
                            Primary|Backup|Any:Circuit_Name
      -s GEN_STATS_PER_NNI, --gen_stats_per_nni GEN_STATS_PER_NNI
                            List number of EVCs per NNI-s Any: list all NNIs To
                            filter use -s NNI[:JSON]
      -S SHORTCUT_FILE, --shortcut-file SHORTCUT_FILE
                            Use a provided shortcut file. Default is .evc_manager
    
    filters:
      --has-uni-device HAS_UNI_DEVICE
                            Filter output based on the UNI's device
      --has-uni-interface HAS_UNI_INTERFACE
                            Filter output based on the UNI's interface
      --has-uni-tag-value HAS_UNI_TAG_VALUE
                            Filter output based on the UNI's tag value (VLAN ID)
      --has-nni-name HAS_NNI_NAME
                            Filter output based on the NNI's name
      --has-nni-name-primary HAS_NNI_NAME_PRIMARY
                            Filter output when NNI's name is in primary path
      --has-nni-name-backup HAS_NNI_NAME_BACKUP
                            Filter output when NNI's name is in backup path
    
    authentication:
      -u USER, --user USER  Backend user for authentication
      -t TENANT, --tenant TENANT
                            Backend user group for authentication

To use EVC_Manager as a Python module, follow these steps. The INPUT is just an example and
represents the input you mean to submit to the evc_manager (use option -h to discover all options):

    from evc_manager import EvcManager, get_cli
    INPUT = ['-u', 'admin',
         '-t', 'admin',
         '-p', 'sparc123',
         '-O', 'https://192.168.56.10/oess/',
         '-v', 'info',
         '-q',
         '-f', './add_evcs.yaml',
         '-A']
    evc_mgr = EvcManager(get_cli(INPUT))
    final_result = evc_mgr.run()
    print(final_result)

Attention: Avoid using option --password with admin accounts. Your password might be stored 
in your Bash history\!\!


# EVC data modeling

To help modeling EVCs, the following data model was created:

    version: 1.0
    name: Circuit Name
    unis: List of User-to-Network Interfaces
      - device: network device's name
        interface_name: network device's interface_name
        interface_description: network device's interface_description
        mac_addresses: list of MAC addresses connected to the network interface
          -
        tag: interface TAG type
          type: Type could be MPLS or VLAN
          value: VLAN ID or MPLS tag or [start, end] for VLAN ranges.
    metrics: Circuit required metrics
      min_bw: minimum bandwidth
      max_delay: maximum delay acceptable in milliseconds
      max_hops: max number of hops
      avoid_shared: if circuit should avoid shared links
    provisioning_time: when the circuit should be created
    decommissioning_time: when the circuit should be terminated
    requested_paths: list of paths, in a priority list. 'Any' if no physical path is required.
    tenant: group name
    priority: circuit priority
    external_id: any external ID if needed
    monitoring: monitoring requirements
      dataplane:
        trace: if data plane path tracing is required
          active: True or False
          interval: interval between tests
      controlplane:
        trace: if control plane path tracing is enough
          active: True or False
          interval: interval between tests
    notification: notification requirements
      slack_channel:
        - workgroup1
          channel1
        - workgroup2
          channel2
      emails:
        - user1@email
        - user2@email
    current_config: Current configuration
      backend: backend or technology being used
      current_path: # list of links being used
      is_backup: is it using a backup path?
      is_optimized: is it using under-provisioned links? (not enough BW, delay higher that required, etc.)
      to_provisioned:
      is_expired:
      is_up:
      is_active: True if between provisioning time and decommissioning time

Data models are provided on folder libs.models.