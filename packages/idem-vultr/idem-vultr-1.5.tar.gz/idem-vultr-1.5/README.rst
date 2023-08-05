==========
IDEM_VULTR
==========
Vultr Cloud Provider for Idem

============
INSTALLATION
============

The vultr idem provider can be installed via pip:
`pip install idem-vultr`

============================
INSTALLATION FOR DEVELOPMENT
============================

1. Clone the `idem_provider_vultr` repository and install with pip:
`pip install -r requirements.txt`
2. Run `pip install -e <path to provider>` from your project's root directory

You are now fully set up to begin developing additional functionality for this provider.

=========
EXECUTION
=========

After installation the Vultr Idem Provider execution and state modules will be accessible to the hub.

To authenticate, first create a profile set up like so::

    vultr:
        default:
            api_key: XXXXXXXXXXXXXXXXXXXX
            location: New Jersey

encrypt this file using the `acct` plugin::

    acct acct_profile.yml

It will create a file called acct_profile.yml.fernet and give you a key for decrypting it.
Put these in the appropriate environment variables::

    export ACCT_FILE="vultr.yml.fernet"
    export ACCT_key="gAAAAAAbjlkjsdkj_lkjlkfsjoj023h_jiosajdf="

You can now safely delete the plaintext file containing your api key.
idem knows how to get the credentials it needs.

The following example uses an vultr state module to ensure the existence of a resource group::

    VM exists:
      vultr.server.vm.present:
        - name: instance_name
        - vps_plan: 16384 MB RAM,320 GB SSD,5.00 TB BW
        - os: Ubuntu 20.04 x64

Use the command line to run vultr specific execution modules::

    idem exec vultr.list full=True
