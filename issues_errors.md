# Issues and Mitigations

- Need to create backup script for rolling back everything --> waiting for beta rollout
- Need to work on /etc/yp.conf this contains ypservers which is not there in the excel
- fine tune NFS share autofind with Filesystem name --< very important --< Completed
- if there is no data in some tabs need to check how the script behaves --< in Progress
- if usergroup alone need to be executed then it should be independent on other configs --< Completed
- if we execute the Config bot from second time it should not again repeat the configuration if the config exists --< In-Progress
- "boot|root|tmp|swap|snap|udev|sda" this for ubuntu alone but for environment its just "root|swap|tmpfs|boot|<migration NFS>"
- "sda" should be added to egrep by default --< Completed
- appvg is default here I am using app1vg please change to appvg based on your projects
- filesystem format should be xfs as by default Redhat latest version allows xfs only --< completed
- very important ==> lvm_full_scan_template() under filesystem_manager.py command3 egrep option should not have appvg while releasing to production --< Need to check
