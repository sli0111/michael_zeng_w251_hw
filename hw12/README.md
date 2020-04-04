# Homework: Part 1 - Installing GPFS FPO

# Submission

* VSI

```
ibmcloud sl vs create --datacenter=wdc07  --hostname=gpfs1 --domain=W251-zengm71.cloud --cpu=2 --memory=4 --os=CENTOS_7_64 --disk=25 --disk=100 --network 1000 --key=1545088 --san
ibmcloud sl vs create --datacenter=wdc07  --hostname=gpfs2 --domain=W251-zengm71.cloud --cpu=2 --memory=4 --os=CENTOS_7_64 --disk=25 --disk=100 --network 1000 --key=1545088 --san
ibmcloud sl vs create --datacenter=wdc07  --hostname=gpfs3 --domain=W251-zengm71.cloud --cpu=2 --memory=4 --os=CENTOS_7_64 --disk=25 --disk=100 --network 1000 --key=1545088 --san
```
`scp -i michael_zeng_ssh michael_zeng_ssh root@52.117.98.188:/root/.ssh/id_rsa` to copy SSH key over.
`scp -i michael_zeng_ssh /Users/zengm71/Documents/Berkeley/W251/michael_zeng_w251_hw/hw12/downloader_reddit_002.py root@52.117.98.188:/gpfs/gpfsfpo/`
`ssh-keygen -p` to remove the passphrase, otherwise it won't work. 
* Ansers
1. How much disk space is used after step 4?
    I downloaded all three dataset and saw 31G in use. 
    ```
    [root@gpfs1 download_reddit]# df -h .
    Filesystem      Size  Used Avail Use% Mounted on
    gpfsfpo         300G   31G  270G  11% /gpfs/gpfsfpo 
    ```
2. Did you parallelize the crawlers in step 4? If so, how?
    Yes, there are two layers of parallelizations:
    * across machines: `devider.sh` is run under `reddit_urls` so that the txt files containing the urls can be placed equally into three folders. `downloader_reddit_001.py` and such were run on each machine, each on an individual folder. 
    * multiprocessing: every time `downloader_reddit_001.py` is run, 40 processes were kicked off simultaneously and each downloading one txt file
    
    For the US one, I first splited the file `us_gutenberg.urls` into 40 txt files by `split -d us_gutenberg.urls -n 40 us_url_folders/us_url_part- --additional-suffix=.txt`, then carried out similar steps, see `downloader_US.py`
3. Describe the steps to de-duplicate the web pages you crawled.
    There are two steps for de-duplications and they are coded in `dedup.py`:
    * each url txt was processed by `lazynlp.dedup_lines` searching for duplicated urls within the files
    * the first url txt file after step 1 was put in a separate folder. Then every url coming out of step 1 later, was du-deduped against all the exisiting urls in the folder using `lazynlp.dedup_lines_from_new_file`.

4. Submit the list of files you that your LazyNLP spiders crawled (ls -la).
    ```
    [root@gpfs3 gpfsfpo]# ls -la
    total 878865
    drwxr-xr-x. 9 root root    262144 Apr  4 00:56 .
    drwxr-xr-x. 4 root root      4096 Mar 31 18:09 ..
    -rw-rw-r--. 1 root root    181290 Feb 27  2019 aus_gut.urls
    -rw-r--r--. 1 root root     11721 Apr  4 00:53 aus_gut.urls.zip
    -rw-r--r--. 1 root root       565 Apr  4 00:16 dedup.py
    -rw-r--r--. 1 root root       116 Apr  4 00:17 devider.sh
    drwxr-xr-x. 2 root root    262144 Apr  4 04:58 download_aus
    -rw-r--r--. 1 root root       524 Apr  4 00:16 downloader_reddit_001.py
    -rw-r--r--. 1 root root       525 Apr  1 00:49 downloader_reddit_002.py
    -rw-r--r--. 1 root root       525 Apr  1 00:50 downloader_reddit_003.py
    -rw-r--r--. 1 root root       553 Apr  4 00:51 downloader_US.py
    drwxr-xr-x. 2 root root  67108864 Apr  4 16:56 download_reddit
    drwxr-xr-x. 2 root root   4194304 Apr  4 03:43 download_us
    drwxr-xr-x. 4 root root      4096 Mar 31 18:11 lazynlp
    drwxrwxr-x. 5 root root     16384 Mar 31 18:19 reddit_urls
    -rw-r--r--. 1 root root 824545924 Mar 31 18:16 reddit_urls.zip
    dr-xr-xr-x. 2 root root      8192 Dec 31  1969 .snapshots
    -rw-rw-r--. 1 root root   3023162 Feb 28  2019 us_gutenberg.urls
    -rw-r--r--. 1 root root    313831 Apr  4 00:17 us_gutenberg.urls.zip
    drwxr-xr-x. 2 root root      4096 Apr  4 00:44 us_url_folders
    drwxrwx---. 2 root root      4096 Mar 31 18:14 wikitext-103
    ```
    The folders `download_aus`, `download_reddit` and `download_us` are the three datasets respectively. 


# Original README
## Overview

These instructions are a subset of the official instructions linked to from here: [IBM Spectrum Scale Resources - GPFS](https://www.ibm.com/support/knowledgecenter/en/STXKQY_5.0.1/com.ibm.spectrum.scale.v5r01.doc/bl1ins_manuallyinstallingonlinux_packages.htm).


We will install GPFS FPO with no replication (replication=1) and local write affinity.  This means that if you are on one of the nodes and are writing a file in GPFS, the file will end up on your local node unless your local node is out of space.

A. __Get three virtual servers provisioned__, 2 vCPUs, 4G RAM, CENTOS_7_64, __two local disks__ 25G and 100G each, in any datacenter. __Make sure__ you attach a keypair.  Pick intuitive names such as gpfs1, gpfs2, gpfs3.  Note their internal (10.x.x.x) ip addresses.

B. __Set up each one of your nodes as follows:__

Add to /root/.bash\_profile the following line in the end:

    export PATH=$PATH:/usr/lpp/mmfs/bin

Make sure the nodes can talk to each other without a password.  When you created the VMs, you specified a keypair.  Copy it to /root/.ssh/id\_rsa (copy paste or scp works).  Set its permissions:

    chmod 600 /root/.ssh/id_rsa

Set up the hosts file (/etc/hosts) for your cluster by adding the __PRIVATE__ IP addresses you noted earlier and names for each node in the cluster.  __Also__ you should remove the entry containing the fully qualified node name for your headnode / gpfs1.sftlyr.ws (otherwise it will trip up some of the GPFS tools since it likely does not resolve). For instance, your hosts file might look like this:

    127.0.0.1 		localhost.localdomain localhost
    10.122.6.68		gpfs1
    10.122.6.70		gpfs2
    10.122.6.71		gpfs3

Create a nodefile.  Edit /root/nodefile and add the names of your nodes.  This is a very simple example with just one quorum node:

    gpfs1:quorum:
    gpfs2::
    gpfs3::

C. __Install and configure GPFS FPO on each node:__
Install pre-requisites
```
#update the kernel & install some pre-reqs
yum install -y kernel-devel g++ gcc cpp kernel-headers gcc-c++ 
yum update
#reboot to use the latest kernel
reboot
#install more pre-reqs
yum install -y ksh perl libaio m4 net-tools

```
Then install S3 API client and GPFS with:

S3 Client
```
curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip"
yum install unzip
unzip awscli-bundle.zip
sudo ./awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws
aws configure
Access Key ID:
A1XGdUexhlIdyusn16Jh
Secret Access Key:
vImKKsEPfYQuzovEuPZjabeAViRhdQ9P85RQJEt1
aws --endpoint-url=https://s3-api.us-geo.objectstorage.softlayer.net  s3 cp s3://homework12/Spectrum_Scale_Advanced-5.0.3.2-x86_64-Linux-install Spectrum_Scale_Advanced-5.0.3.2-x86_64-Linux-install

```

GPFS installation (node that we are adding nodes using the node names, be sure to update the hosts file on each VM)
```
chmod +x Spectrum_Scale_Advanced-5.0.3.2-x86_64-Linux-install
./Spectrum_Scale_Advanced-5.0.3.2-x86_64-Linux-install --silent  (this command needs to be run on every node)
/usr/lpp/mmfs/5.0.3.2/installer/spectrumscale node add gpfs1  (this command needs to be run just gpfs1)
/usr/lpp/mmfs/5.0.3.2/installer/spectrumscale node add gpfs2  (this command needs to be run just gpfs1)
/usr/lpp/mmfs/5.0.3.2/installer/spectrumscale node add gpfs3  (this command needs to be run just gpfs1)

```


D. __Create the cluster.  Do these steps only on one node (gpfs1 in my example).__
```
/usr/lpp/mmfs/5.0.3.2/installer/spectrumscale setup -s IP-OF-GPFS1  (this command needs to be run just gpfs1)
/usr/lpp/mmfs/5.0.3.2/installer/spectrumscale callhome disable   (this command needs to be run just gpfs1)
/usr/lpp/mmfs/5.0.3.2/installer/spectrumscale install  (this command needs to be run just gpfs1)
```
Now the cluster is installed, let's work the details.

Now, you must accept the license:

    mmchlicense server -N all (this command needs to be run just gpfs1)
    # (say yes)

Now, start GPFS:

    mmstartup -a (this command needs to be run just gpfs1)

All nodes should be up ("GPFS state" column shows "active"):

    mmgetstate -a (this command needs to be run just gpfs1)

Nodes may reflect "arbitrating" state briefly before "active".  If one or more nodes are down, you will need to go back and see what you might have missed. If some node shows a DOWN state, log into the node and run the command  mmstartup. The main GPFS log file is `/var/adm/ras/mmfs.log.latest`; look for errors there.

You could get more details on your cluster:

    mmlscluster (this command needs to be run just gpfs1)

Now we need to define our disks. Do this to print the paths and sizes of disks on your machine:

    fdisk -l (this command and the rest until the file creation command (touch aa) needs to be run just gpfs1)

Note the names of your 100G disks. Here's what I see:

    [root@gpfs1 ras]# fdisk -l |grep Disk |grep bytes
    Disk /dev/xvdc: 100 GiB, 107374182400 bytes, 209715200 sectors
    Disk /dev/xvdb: 2 GiB, 2147483648 bytes, 4194304 sectors
    Disk /dev/xvda: 25 GiB, 26843701248 bytes, 52429104 sectors

Now inspect the mount location of the root filesystem on your boxes:

    [root@gpfs1 ras]# mount | grep ' \/ '
    /dev/xvda2 on / type ext3 (rw,noatime)

Disk /dev/xvda (partition 2) is where my operating system is installed, so I'm going to leave it alone.  In my case, __xvdc__ is my 100 disk.  In your case, it could be /dev/xvdb, so __please be careful here__.  Assuming your second disk is `/dev/xvdc` then add these lines to `/root/diskfile.fpo`:

    %pool:
    pool=system
    allowWriteAffinity=yes
    writeAffinityDepth=1

    %nsd:
    device=/dev/xvdc
    servers=gpfs1
    usage=dataAndMetadata
    pool=system
    failureGroup=1

    %nsd:
    device=/dev/xvdc
    servers=gpfs2
    usage=dataAndMetadata
    pool=system
    failureGroup=2

    %nsd:
    device=/dev/xvdc
    servers=gpfs3
    usage=dataAndMetadata
    pool=system
    failureGroup=3

Now run:

    mmcrnsd -F /root/diskfile.fpo

You should see your disks now:

    mmlsnsd -m

Let’s create the file system.  We are using the replication factor 1 for the data:

    mmcrfs gpfsfpo -F /root/diskfile.fpo -A yes -Q no -r 1 -R 1

Let’s check that the file system is created:

    mmlsfs all

Mounting the distributed FS (be sure to pass -a so that the filesystem is mounted on all nodes):

    mmmount all -a

All done.  Now you should be able to go to the mounted FS:

    cd /gpfs/gpfsfpo

.. and see that there's 300 G there:

    [root@gpfs1 gpfsfpo]# df -h .
    Filesystem      Size  Used Avail Use% Mounted on
    /dev/gpfsfpo     300G  678M   300G   1% /gpfs/gpfsfpo

Make sure you can write, e.g.

    touch aa

If the file was created, you are all set:

    ls -l /gpfs/gpfsfpo
    ssh gpfs2 'ls -l /gpfs/gpfsfpo'
    ssh gpfs3 'ls -l /gpfs/gpfsfpo'


# Part 2 - LazyNLP [Crawler library](https://github.com/MIDS-scaling-up/v2/blob/master/week12/hw/dataset.md)
