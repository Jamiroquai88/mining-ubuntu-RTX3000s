# mining-ubuntu-RTX3000s
In this repo I am trying to summarize how to successfully mine ETH (and possibly other coins) under Ubuntu 18.04. I like to do all of this stuff myself, not relying on some existing mining operating systems, but I am not saying, that they are bad, this is just a preffered option for me.

## Installation
Install ubuntu server, I am using 18.04 but I would expect others to work as well.
This setup is focused on [vast.ai](www.vast.ai) hosting, but might be easily adapted also to other setups.

## Steps
1.  Follow [this tutorial](https://gist.github.com/streslab/c51e09ca0e44c79910a4bd26b924eccd) up to overclocking step.
2.  Do the same as in the repo above with a few modification

Start an X server and push it into the background:
```bash
sudo xinit &
export DISPLAY=:0.0
```

Enable persistence mode on the GPUs:
```bash
sudo nvidia-smi -pm 1
```
Set GPU 0 power level to 280W
```bash
sudo nvidia-smi -i 0 -pl 100
```
Enable GPU 0 manual fan control and set to 50%
```bash
nvidia-settings -a '[gpu:0]/GPUFanControlState=1' -a '[fan:0]/GPUTargetFanSpeed=50'
```
Increase GPU 0 memory clock by 1000 (note \[4\] just before =, for 2/3 it won't work) 
```bash
nvidia-settings -a '[gpu:0]/GPUMemoryTransferRateOffset[4]=1000'
```
Increase (or usually decrease) GPU 0 core clock by 100 (note \[4\] just before =, for 2/3 it won't work):
```bash
nvidia-settings -a '[gpu:{gpu_idx}]/GPUGraphicsClockOffset[4]=-100'
```

Eventually, you can use this [automated script](https://github.com/Jamiroquai88/mining-ubuntu-RTX3000s/blob/main/tune_hr.py) to tune your parameters automatically. It iterates over possible values and computes hashrate/watt ratio, then the user can pick desired settings. It is optimized for RTX 3090, please do not use it blindly, but try to understand what it is doing. 


